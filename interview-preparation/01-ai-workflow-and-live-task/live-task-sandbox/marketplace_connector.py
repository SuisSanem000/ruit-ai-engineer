"""
Basic Marketplace Connector Example (Written in Simple, Readable Python)

What this file does:
1. Defines simple custom error classes so we know WHY an API call failed
   (Should we retry? Did the seller's login expire? Did the marketplace change its JSON?).
2. Uses a basic Pydantic model (`ListingItem`) to validate JSON from a marketplace
   and clean up messy prices like "45,50 €".
3. Defines simple async functions using `httpx.AsyncClient` to fetch an item (with retries)
   and delist a sold item across multiple marketplaces.
"""

import asyncio
import logging
import random
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

# Set up a standard Python logger so we can log warnings if a marketplace changes its JSON
logger = logging.getLogger(__name__)


# =====================================================================
# 1. BASIC CUSTOM ERROR CLASSES
# In Python, we create custom errors by inheriting from `Exception`.
# This helps Celery or our caller know how to handle each failure.
# =====================================================================


class MarketplaceError(Exception):
    """Base error class for any marketplace problem."""

    def __init__(self, marketplace: str, message: str) -> None:
        # Call the parent Exception class with a clear message
        super().__init__(f"[{marketplace}] {message}")
        self.marketplace = marketplace


class RetryableError(MarketplaceError):
    """Error for temporary network issues, 429 rate limits, or 500 server errors.
    When Celery sees this error, it knows it is safe to retry later.
    """

    def __init__(
        self,
        marketplace: str,
        message: str,
        retry_after_seconds: Optional[float] = None,
    ) -> None:
        super().__init__(marketplace, message)
        self.retry_after_seconds = retry_after_seconds


class AuthExpiredError(MarketplaceError):
    """Error for HTTP 401 or 403.
    Do NOT retry this automatically—we need to refresh the seller's login token first.
    """


class SchemaBreakageError(MarketplaceError):
    """Error when the marketplace changed its JSON structure or returned bad data.
    We must alert engineers right away because the integration broke.
    """


# =====================================================================
# 2. PYDANTIC DATA VALIDATION MODEL
# Pydantic works like Zod or AJV in TypeScript/JavaScript.
# It checks that incoming JSON has the right fields and types at runtime.
# =====================================================================


class ListingItem(BaseModel):
    """Represents a second-hand item fetched from a marketplace API."""

    # `extra="allow"` tells Pydantic: do not crash if the marketplace sends extra unknown fields.
    # Instead, keep them in `self.__pydantic_extra__` so we can check if their API changed!
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    # Required fields with basic validation rules
    external_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    price_eur: Decimal = Field(gt=Decimal(0))
    currency: str = "EUR"
    is_active: bool = True

    # `@field_validator(..., mode="before")` runs BEFORE Pydantic checks the type.
    # Here, if the marketplace sends an integer ID like `987654`, we convert it to `"987654"`.
    @field_validator("external_id", mode="before")
    @classmethod
    def convert_int_id_to_string(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        return value

    # Marketplaces send messy prices: `"45,50 €"`, `"120.00"`, or `{"amount": "45,50 €"}`.
    # This function cleans the value before converting it to a `Decimal` number.
    @field_validator("price_eur", mode="before")
    @classmethod
    def clean_messy_price(cls, value: Any) -> Decimal:
        # If the price is inside a dictionary like {"amount": "45,50 €"}, grab "amount"
        if isinstance(value, dict) and "amount" in value:
            value = value["amount"]

        # If it is a string, remove the Euro sign, change comma to dot, and trim spaces
        if isinstance(value, str):
            clean_text = (
                value.replace("€", "").replace("EUR", "").replace(",", ".").strip()
            )
            return Decimal(clean_text)

        # Otherwise convert numbers (int/float) to string first, then to Decimal
        return Decimal(str(value))

    def get_unexpected_fields(self) -> Set[str]:
        """Returns a set of any new/unknown JSON keys sent by the marketplace."""
        if not self.__pydantic_extra__:
            return set()
        return set(self.__pydantic_extra__.keys())


# =====================================================================
# 3. ASYNC HTTP CLIENT WITH RETRIES & BACKOFF
# Uses `httpx.AsyncClient` (similar to axios/fetch in Node.js).
# =====================================================================


async def request_with_retry(
    client: httpx.AsyncClient,
    marketplace: str,
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    max_retries: int = 2,
) -> httpx.Response:
    """Sends an HTTP request and retries on temporary errors (timeouts, 429, 5xx)."""
    last_error: Optional[Exception] = None

    # Loop from attempt 0 up to max_retries
    for attempt in range(max_retries + 1):
        try:
            response = await client.request(method, url, headers=headers)
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            # Network or timeout error -> safe to retry
            last_error = RetryableError(marketplace, f"Network timeout: {exc}")
        else:
            # 1. Success status codes (200 OK, 201 Created, 204 No Content)
            if response.status_code in (200, 201, 204):
                return response

            # 2. Auth error (401 Unauthorized or 403 Forbidden) -> Stop immediately!
            if response.status_code in (401, 403):
                raise AuthExpiredError(
                    marketplace, f"Login expired (HTTP {response.status_code})"
                )

            # 3. Rate limit (429) or Server error (500, 502, 503, 504) -> Safe to retry
            if response.status_code == 429 or response.status_code >= 500:
                retry_header = response.headers.get("Retry-After")
                retry_seconds: Optional[float] = None
                if retry_header is not None:
                    try:
                        retry_seconds = float(retry_header)
                    except ValueError:
                        retry_seconds = None

                last_error = RetryableError(
                    marketplace,
                    f"Temporary HTTP {response.status_code}",
                    retry_after_seconds=retry_seconds,
                )
            else:
                # 4. Other 4xx errors (like 400 Bad Request) -> API contract probably changed
                raise SchemaBreakageError(
                    marketplace, f"Unexpected HTTP {response.status_code}"
                )

        # If we have retries left, wait before trying again
        if attempt < max_retries:
            if (
                isinstance(last_error, RetryableError)
                and last_error.retry_after_seconds is not None
            ):
                wait_time = last_error.retry_after_seconds
            else:
                # Exponential backoff with random jitter so all workers don't retry at the exact same millisecond
                max_wait = 0.05 * (2**attempt)
                wait_time = random.uniform(0.01, max_wait)

            # IMPORTANT: Always use `await asyncio.sleep()` in async Python, NEVER `time.sleep()`!
            await asyncio.sleep(wait_time)

    # If all retries failed, raise the last error we saw
    assert last_error is not None
    raise last_error


async def fetch_marketplace_listing(
    client: httpx.AsyncClient,
    marketplace: str,
    external_id: str,
    max_retries: int = 2,
) -> ListingItem:
    """Fetches one listing from a marketplace API and validates its JSON with Pydantic."""
    response = await request_with_retry(
        client=client,
        marketplace=marketplace,
        method="GET",
        url=f"/listings/{external_id}",
        max_retries=max_retries,
    )

    # Try to parse the JSON and validate it with our Pydantic `ListingItem` model
    try:
        raw_json = response.json()
        item = ListingItem.model_validate(raw_json)
    except (ValueError, ValidationError) as exc:
        # If required fields are missing or invalid, raise SchemaBreakageError to alert engineers
        raise SchemaBreakageError(
            marketplace, f"JSON validation failed for {external_id}: {exc}"
        ) from exc

    # Check if the marketplace silently added new fields to their JSON response
    unexpected = item.get_unexpected_fields()
    if unexpected:
        logger.warning(
            "Marketplace %s sent new unexpected JSON fields: %s",
            marketplace,
            unexpected,
        )

    return item


# =====================================================================
# 4. DELISTING AN ITEM ACROSS MULTIPLE MARKETPLACES CONCURRENTLY
# When an item sells on one marketplace, we must delist it from the others.
# =====================================================================


async def delist_single_marketplace(
    client: httpx.AsyncClient,
    marketplace: str,
    external_id: str,
    idempotency_key: str,
    semaphore: asyncio.Semaphore,
) -> Dict[str, Any]:
    """Delists one item on one marketplace and returns a simple status dictionary.
    We catch errors inside this function so one failing marketplace does not crash the others.
    """
    # `async with semaphore:` limits how many requests run at the same time (like p-limit in JS)
    async with semaphore:
        try:
            await request_with_retry(
                client=client,
                marketplace=marketplace,
                method="POST",
                url=f"/listings/{external_id}/delist",
                headers={"Idempotency-Key": idempotency_key},
                max_retries=1,
            )
            return {
                "marketplace": marketplace,
                "external_id": external_id,
                "success": True,
                "retryable": False,
                "error": None,
            }
        except RetryableError as exc:
            # Failed due to temporary 503/timeout -> tell caller to retry this marketplace later
            return {
                "marketplace": marketplace,
                "external_id": external_id,
                "success": False,
                "retryable": True,
                "error": str(exc),
            }
        except MarketplaceError as exc:
            # Failed due to permanent error (like 401 auth expired)
            return {
                "marketplace": marketplace,
                "external_id": external_id,
                "success": False,
                "retryable": False,
                "error": str(exc),
            }


async def delist_across_marketplaces(
    targets: List[Dict[str, Any]],
    idempotency_key: str,
    max_concurrency: int = 5,
) -> List[Dict[str, Any]]:
    """Runs delist requests concurrently across a list of marketplaces.

    Each item in `targets` is a dict:
        {"client": httpx_client, "marketplace": "vinted", "external_id": "v-100"}
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    # Create a list of async tasks (like an array of Promises in JavaScript)
    tasks = []
    for target in targets:
        task = delist_single_marketplace(
            client=target["client"],
            marketplace=target["marketplace"],
            external_id=target["external_id"],
            idempotency_key=idempotency_key,
            semaphore=semaphore,
        )
        tasks.append(task)

    # `asyncio.gather(*tasks)` works just like `await Promise.all(tasks)` in JavaScript
    results = await asyncio.gather(*tasks)
    return list(results)
