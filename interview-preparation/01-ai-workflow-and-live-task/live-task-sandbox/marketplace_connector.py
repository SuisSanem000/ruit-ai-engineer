"""Basic Python Marketplace Connector for Ruit Live AI Task Practice.

WHAT THIS FILE DOES:
1. Defines simple custom error classes so we know if an error should be retried
   (like a 429 rate limit) or stopped immediately (like a 401 login error).
2. Uses a basic Pydantic model (`NormalizedListing`) to clean messy JSON from
   marketplaces (for example, turning `"45,50 €"` into `45.50`) and check if
   the marketplace added new unknown fields ("schema drift").
3. Uses an async HTTP client (`httpx.AsyncClient`) to fetch and delist items
   with automatic retries.
4. Runs delist calls across multiple marketplaces at the same time using
   `asyncio.gather` and `asyncio.Semaphore`.
"""

from __future__ import annotations

import asyncio
import logging
import random
from decimal import Decimal
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

logger = logging.getLogger(__name__)


# ============================================================================
# 1. Simple Custom Error Classes
# ============================================================================
# In Python, we create custom exceptions by inheriting from `Exception`.
# Grouping errors like this helps background workers (like Celery) decide
# whether to retry a failed job or stop immediately.


class MarketplaceIntegrationError(Exception):
    """Base error class for any marketplace problem."""

    def __init__(self, marketplace: str, message: str) -> None:
        super().__init__(f"[{marketplace}] {message}")
        self.marketplace = marketplace


class RetryableMarketplaceError(MarketplaceIntegrationError):
    """Temporary error (network timeout, HTTP 429 rate limit, or HTTP 500/503).
    It is safe to wait a moment and try again.
    """

    def __init__(
        self,
        marketplace: str,
        message: str,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(marketplace, message)
        self.retry_after_seconds = retry_after_seconds


class SellerAuthExpiredError(MarketplaceIntegrationError):
    """HTTP 401 or 403 error. The seller's login token expired.
    Do NOT retry blindly—we need to refresh the token or ask the seller to log in.
    """


class UpstreamSchemaBreakageError(MarketplaceIntegrationError):
    """The marketplace changed its JSON format or returned an unexpected 400/422 error.
    Do NOT retry—alert the engineering team so we can update our parser.
    """


# ============================================================================
# 2. Marketplace Names (Simple Constants)
# ============================================================================


class MarketplaceName:
    """Simple string constants for marketplace names."""

    WALLAPOP = "wallapop"
    VINTED = "vinted"
    EBAY = "ebay"
    DEPOP = "depop"


# ============================================================================
# 3. Pydantic Model to Validate & Clean Marketplace JSON
# ============================================================================
# Pydantic is the Python equivalent of Zod / AJV in TypeScript.
# It checks data types at runtime when we receive JSON from an external API.


class NormalizedListing(BaseModel):
    """Clean, validated product listing inside Ruit."""

    # `extra="allow"` tells Pydantic not to crash if a marketplace sends new
    # unknown fields. Instead, it stores those extra fields in `__pydantic_extra__`
    # so we can log a warning and spot API changes early.
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    external_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    price_eur: Decimal = Field(gt=Decimal(0))
    currency: str = "EUR"
    is_active: bool = True

    @field_validator("external_id", mode="before")
    @classmethod
    def convert_int_id_to_string(cls, value: Any) -> str:
        """Some marketplaces send IDs as numbers (12345). Convert them to strings ('12345')."""
        if isinstance(value, int):
            return str(value)
        return value

    @field_validator("price_eur", mode="before")
    @classmethod
    def clean_messy_price(cls, value: Any) -> Decimal:
        """Marketplaces send prices in many messy formats:
        - A dictionary: `{"amount": "45,50 €"}`
        - A string with symbols: `"45,50 €"`
        - A number or string: `120.00` or `"120.00"`
        This function cleans the value before Pydantic checks that it is > 0.
        """
        if isinstance(value, dict) and "amount" in value:
            value = value["amount"]

        if isinstance(value, str):
            cleaned = (
                value.replace("€", "").replace("EUR", "").replace(",", ".").strip()
            )
            return Decimal(cleaned)

        return Decimal(str(value))

    def detect_schema_drift(
        self, known_optional_fields: set[str] | None = None
    ) -> set[str]:
        """Returns any unexpected extra field names that the marketplace sent."""
        extra_dict = self.__pydantic_extra__ or {}
        extra_keys = set(extra_dict.keys())
        if known_optional_fields:
            return extra_keys - known_optional_fields
        return extra_keys


# ============================================================================
# 4. Async API Client with Automatic Retries
# ============================================================================


class ResilientMarketplaceClient:
    """Makes async HTTP calls to a marketplace and retries temporary errors."""

    def __init__(
        self,
        marketplace: str,
        client: httpx.AsyncClient,
        max_retries: int = 3,
        base_backoff_sec: float = 0.05,
        known_extra_fields: set[str] | None = None,
    ) -> None:
        self.marketplace = marketplace
        self.client = client
        self.max_retries = max_retries
        self.base_backoff_sec = base_backoff_sec
        self.known_extra_fields = known_extra_fields or set()

    async def _request_with_retry(
        self, method: str, url: str, headers: dict[str, str] | None = None
    ) -> httpx.Response:
        """Helper method that sends an HTTP request and retries on 429/5xx or timeouts."""
        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(method, url, headers=headers)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                # Network timeout or dropped connection -> safe to retry
                last_error = RetryableMarketplaceError(
                    self.marketplace, f"Network timeout calling {url}: {exc}"
                )
            else:
                # 1. Success status codes (200 OK, 201 Created, 204 No Content)
                if response.status_code in (200, 201, 204):
                    return response

                # 2. Login / Token expired (401 Unauthorized, 403 Forbidden)
                # Raise immediately! Retrying with the same expired token is useless.
                if response.status_code in (401, 403):
                    raise SellerAuthExpiredError(
                        self.marketplace,
                        f"Seller login expired (HTTP {response.status_code}) on {url}",
                    )

                # 3. Rate limit (429) or Server error (500, 502, 503, 504) -> safe to retry
                if response.status_code == 429 or response.status_code >= 500:
                    retry_header = response.headers.get("Retry-After")
                    retry_seconds: float | None = None
                    if retry_header:
                        try:
                            retry_seconds = float(retry_header)
                        except ValueError:
                            retry_seconds = None

                    last_error = RetryableMarketplaceError(
                        self.marketplace,
                        f"Temporary HTTP {response.status_code} on {url}",
                        retry_after_seconds=retry_seconds,
                    )
                else:
                    # 4. Other client errors (like 400 Bad Request or 422) -> contract broke
                    raise UpstreamSchemaBreakageError(
                        self.marketplace,
                        f"Unexpected HTTP {response.status_code} on {url}",
                    )

            # If we have retries left, wait before trying again
            if attempt < self.max_retries:
                if (
                    isinstance(last_error, RetryableMarketplaceError)
                    and last_error.retry_after_seconds is not None
                ):
                    wait_time = last_error.retry_after_seconds
                else:
                    # Exponential backoff with random jitter (prevents all workers
                    # from hitting the marketplace at the exact same millisecond)
                    max_wait = self.base_backoff_sec * (2**attempt)
                    wait_time = random.uniform(0, max_wait)

                # IMPORTANT: Always use `await asyncio.sleep()` in async code,
                # never `time.sleep()` (which would freeze the whole event loop).
                await asyncio.sleep(wait_time)

        # If all retries failed, raise the last error
        assert last_error is not None
        raise last_error

    async def fetch_listing(self, external_id: str) -> NormalizedListing:
        """Fetches a listing's JSON and validates it with Pydantic."""
        response = await self._request_with_retry("GET", f"/listings/{external_id}")

        try:
            raw_data = response.json()
            listing = NormalizedListing.model_validate(raw_data)
        except (ValueError, ValidationError) as exc:
            # If the marketplace renamed or removed a required field (like `price_eur`),
            # Pydantic raises `ValidationError`, and we turn it into our breakage error.
            raise UpstreamSchemaBreakageError(
                self.marketplace,
                f"Marketplace JSON changed for listing {external_id}: {exc}",
            ) from exc

        # Check if the marketplace silently added any new fields
        new_fields = listing.detect_schema_drift(self.known_extra_fields)
        if new_fields:
            logger.warning(
                "Schema drift on %s: new fields %s",
                self.marketplace,
                sorted(new_fields),
            )

        return listing

    async def delist_item(self, external_id: str, idempotency_key: str) -> bool:
        """Removes a sold item from the marketplace.
        Sends an `Idempotency-Key` header so retrying never causes errors if already delisted.
        """
        await self._request_with_retry(
            "POST",
            f"/listings/{external_id}/delist",
            headers={"Idempotency-Key": idempotency_key},
        )
        return True


# ============================================================================
# 5. Delist Across Multiple Marketplaces at the Same Time
# ============================================================================


class DelistOutcome:
    """Simple class holding the result of delisting on one marketplace."""

    def __init__(
        self,
        marketplace: str,
        external_id: str,
        success: bool,
        retryable: bool = False,
        error_message: str | None = None,
    ) -> None:
        self.marketplace = marketplace
        self.external_id = external_id
        self.success = success
        self.retryable = retryable
        self.error_message = error_message


async def delist_across_marketplaces(
    targets: list[tuple[ResilientMarketplaceClient, str]],
    idempotency_key: str,
    max_concurrency: int = 5,
) -> list[DelistOutcome]:
    """Runs delist requests across multiple marketplaces concurrently.

    - Uses `asyncio.Semaphore(max_concurrency)` so we never open too many
      connections at the same time (like `p-limit` in Node.js).
    - Catches errors inside `_delist_single` so if eBay fails with a 503 error,
      Vinted and Wallapop still finish delisting cleanly!
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _delist_single(
        connector: ResilientMarketplaceClient, external_id: str
    ) -> DelistOutcome:
        async with semaphore:
            try:
                await connector.delist_item(external_id, idempotency_key)
                return DelistOutcome(
                    marketplace=connector.marketplace,
                    external_id=external_id,
                    success=True,
                )
            except RetryableMarketplaceError as exc:
                return DelistOutcome(
                    marketplace=connector.marketplace,
                    external_id=external_id,
                    success=False,
                    retryable=True,
                    error_message=str(exc),
                )
            except MarketplaceIntegrationError as exc:
                return DelistOutcome(
                    marketplace=connector.marketplace,
                    external_id=external_id,
                    success=False,
                    retryable=False,
                    error_message=str(exc),
                )

    # `asyncio.gather` is the Python equivalent of `Promise.all` in JavaScript.
    tasks = [_delist_single(conn, ext_id) for conn, ext_id in targets]
    results = await asyncio.gather(*tasks)
    return list(results)
