"""Reference implementation for Ruit Live AI Task Sandbox.

Demonstrates:
1. Structural typing via `typing.Protocol`
2. Pydantic v2 validation + proactive schema-drift detection
3. Explicit error hierarchy (Retryable vs Auth vs Upstream Breakage)
4. Async HTTPX client with connection pooling, Retry-After, exponential backoff + jitter
5. Bounded concurrency (`asyncio.Semaphore`) & partial-failure isolation for cross-marketplace delisting
"""

from __future__ import annotations

import asyncio
import logging
import random
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Protocol

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

logger = logging.getLogger(__name__)


# ============================================================================
# 1. Explicit Error Hierarchy (Python + Rust Result Mindset)
# ============================================================================


class MarketplaceIntegrationError(Exception):
    """Base exception for all marketplace connector errors."""

    def __init__(self, marketplace: str, message: str) -> None:
        super().__init__(f"[{marketplace}] {message}")
        self.marketplace = marketplace


class RetryableMarketplaceError(MarketplaceIntegrationError):
    """Transient network, timeout, 429 rate-limit, or 5xx error (safe to retry)."""

    def __init__(
        self, marketplace: str, message: str, retry_after_seconds: float | None = None
    ) -> None:
        super().__init__(marketplace, message)
        self.retry_after_seconds = retry_after_seconds


class SellerAuthExpiredError(MarketplaceIntegrationError):
    """401/403 error indicating the seller's session/OAuth token must be refreshed."""


class UpstreamSchemaBreakageError(MarketplaceIntegrationError):
    """Marketplace changed its API contract in a breaking way; alert engineering immediately."""


# ============================================================================
# 2. Pydantic v2 Boundary Validation & Proactive Schema Drift Detection
# ============================================================================


class MarketplaceName(str, Enum):
    WALLAPOP = "wallapop"
    VINTED = "vinted"
    EBAY = "ebay"
    DEPOP = "depop"


class NormalizedListing(BaseModel):
    """Normalized Ruit listing parsed from heterogeneous marketplace payloads."""

    # Allow extra fields so we can inspect `__pydantic_extra__` for silent schema drift
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    external_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    price_eur: Decimal = Field(gt=Decimal(0))
    currency: str = Field(default="EUR", pattern=r"^[A-Z]{3}$")
    is_active: bool = True

    @field_validator("external_id", mode="before")
    @classmethod
    def coerce_int_id(cls, v: Any) -> str:
        if isinstance(v, int):
            return str(v)
        return v

    @field_validator("price_eur", mode="before")
    @classmethod
    def normalize_messy_price(cls, v: Any) -> Decimal:
        """Handles strings like '19,99 €', dicts like {'amount': '19.99'}, or numbers."""
        if isinstance(v, dict) and "amount" in v:
            v = v["amount"]
        if isinstance(v, str):
            cleaned = v.replace("€", "").replace("EUR", "").replace(",", ".").strip()
            return Decimal(cleaned)
        return Decimal(str(v))

    def detect_schema_drift(self, known_optional_fields: set[str] | None = None) -> set[str]:
        """Returns any unexpected extra keys sent by the marketplace API."""
        extra_keys = set((self.__pydantic_extra__ or {}).keys())
        if known_optional_fields:
            return extra_keys - known_optional_fields
        return extra_keys


# ============================================================================
# 3. Structural Interface (`typing.Protocol`) & Resilient Async Client
# ============================================================================


class MarketplaceClientProtocol(Protocol):
    marketplace: MarketplaceName

    async def fetch_listing(self, external_id: str) -> NormalizedListing: ...
    async def delist_item(self, external_id: str, idempotency_key: str) -> bool: ...


class ResilientMarketplaceClient:
    """Async HTTPX connector with retries, backoff+jitter, and drift telemetry."""

    def __init__(
        self,
        marketplace: MarketplaceName,
        client: httpx.AsyncClient,
        max_retries: int = 3,
        base_backoff_sec: float = 0.05,
        known_extra_fields: set[str] | None = None,
    ) -> None:
        self.marketplace = marketplace
        self._client = client
        self._max_retries = max_retries
        self._base_backoff_sec = base_backoff_sec
        self._known_extra_fields = known_extra_fields or set()

    async def _request_with_retry(
        self, method: str, url: str, **kwargs: Any
    ) -> httpx.Response:
        last_exc: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._client.request(method, url, **kwargs)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = RetryableMarketplaceError(
                    self.marketplace, f"Network/timeout error on {url}: {exc}"
                )
            else:
                if response.status_code in (200, 201, 204):
                    return response

                if response.status_code in (401, 403):
                    raise SellerAuthExpiredError(
                        self.marketplace,
                        f"Auth failed with HTTP {response.status_code} on {url}",
                    )

                if response.status_code == 429 or response.status_code >= 500:
                    retry_after_raw = response.headers.get("Retry-After")
                    retry_after = (
                        float(retry_after_raw)
                        if retry_after_raw and retry_after_raw.replace(".", "").isdigit()
                        else None
                    )
                    last_exc = RetryableMarketplaceError(
                        self.marketplace,
                        f"Transient HTTP {response.status_code} on {url}",
                        retry_after_seconds=retry_after,
                    )
                else:
                    raise UpstreamSchemaBreakageError(
                        self.marketplace,
                        f"Unexpected non-retryable HTTP {response.status_code}: {response.text[:200]}",
                    )

            if attempt < self._max_retries:
                # Respect Retry-After if present; otherwise exponential backoff + full jitter
                if (
                    isinstance(last_exc, RetryableMarketplaceError)
                    and last_exc.retry_after_seconds is not None
                ):
                    sleep_sec = last_exc.retry_after_seconds
                else:
                    cap = self._base_backoff_sec * (2**attempt)
                    sleep_sec = random.uniform(0, cap)
                await asyncio.sleep(sleep_sec)

        assert last_exc is not None
        raise last_exc

    async def fetch_listing(self, external_id: str) -> NormalizedListing:
        response = await self._request_with_retry("GET", f"/listings/{external_id}")
        try:
            raw_data = response.json()
            listing = NormalizedListing.model_validate(raw_data)
        except (ValueError, ValidationError) as exc:
            raise UpstreamSchemaBreakageError(
                self.marketplace,
                f"Contract breakage validating listing {external_id}: {exc}",
            ) from exc

        drifted_fields = listing.detect_schema_drift(self._known_extra_fields)
        if drifted_fields:
            logger.warning(
                "schema_drift_detected marketplace=%s external_id=%s unexpected_fields=%s",
                self.marketplace,
                external_id,
                sorted(drifted_fields),
            )
        return listing

    async def delist_item(self, external_id: str, idempotency_key: str) -> bool:
        await self._request_with_retry(
            "POST",
            f"/listings/{external_id}/delist",
            headers={"Idempotency-Key": idempotency_key},
        )
        return True


# ============================================================================
# 4. Concurrent Cross-Marketplace Delist Coordinator (Double-Sell Prevention)
# ============================================================================


@dataclass(frozen=True)
class DelistOutcome:
    marketplace: MarketplaceName
    external_id: str
    success: bool
    retryable: bool = False
    error_message: str | None = None


async def delist_across_marketplaces(
    targets: list[tuple[MarketplaceClientProtocol, str]],
    idempotency_key: str,
    max_concurrency: int = 5,
) -> list[DelistOutcome]:
    """Concurrently delists an item across connected marketplaces with failure isolation."""
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _delist_one(
        connector: MarketplaceClientProtocol, external_id: str
    ) -> DelistOutcome:
        async with semaphore:
            try:
                await connector.delist_item(external_id, idempotency_key=idempotency_key)
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

    return list(
        await asyncio.gather(
            *(_delist_one(conn, ext_id) for conn, ext_id in targets)
        )
    )
