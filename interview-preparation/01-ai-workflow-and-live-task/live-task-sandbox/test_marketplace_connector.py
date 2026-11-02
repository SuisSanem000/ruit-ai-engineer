"""Basic Pytest Tests for `marketplace_connector.py`.

WHAT THIS FILE DOES:
Tests our marketplace connector completely offline using `httpx.MockTransport`
(which fakes HTTP responses in memory so we do not need real internet calls).

Run in terminal:
    .venv/bin/pytest interview-preparation/01-ai-workflow-and-live-task/live-task-sandbox/ -v
"""

import asyncio
from decimal import Decimal

import httpx
import pytest
from marketplace_connector import (
    MarketplaceName,
    NormalizedListing,
    ResilientMarketplaceClient,
    SellerAuthExpiredError,
    UpstreamSchemaBreakageError,
    delist_across_marketplaces,
)


def test_normalized_listing_cleans_prices_and_spots_new_fields() -> None:
    """Test 1: Checks that messy prices like `'45,50 €'` are cleaned into `Decimal('45.50')`
    and that unknown new fields from a marketplace are detected.
    """
    raw_vinted_json = {
        "external_id": 987654,
        "title": "  Vintage Leather Jacket  ",
        "price_eur": {"amount": "45,50 €"},
        "currency": "EUR",
        "is_active": True,
        "new_undocumented_vinted_badge": "promoted_v2",
    }

    listing = NormalizedListing.model_validate(raw_vinted_json)

    assert listing.external_id == "987654"
    assert listing.title == "Vintage Leather Jacket"
    assert listing.price_eur == Decimal("45.50")
    assert listing.detect_schema_drift() == {"new_undocumented_vinted_badge"}


def test_fetch_listing_retries_on_429_rate_limit_and_succeeds() -> None:
    """Test 2: Simulates Wallapop returning HTTP 429 (Too Many Requests) on the
    first try, and HTTP 200 OK on the second try.
    """
    call_count = 0

    def fake_server(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return httpx.Response(429, headers={"Retry-After": "0.01"})
        return httpx.Response(
            200,
            json={
                "external_id": "wp-123",
                "title": "Retro Camera",
                "price_eur": "120.00",
            },
        )

    async def run_test() -> None:
        transport = httpx.MockTransport(fake_server)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.wallapop.example"
        ) as http_client:
            client = ResilientMarketplaceClient(
                MarketplaceName.WALLAPOP, http_client, max_retries=2
            )
            listing = await client.fetch_listing("wp-123")

            assert listing.external_id == "wp-123"
            assert listing.price_eur == Decimal("120.00")
            assert call_count == 2

    asyncio.run(run_test())


def test_fetch_listing_stops_immediately_on_401_login_error() -> None:
    """Test 3: When a seller's login token expires (HTTP 401), the client must
    raise `SellerAuthExpiredError` on the first call and NOT waste retries.
    """
    call_count = 0

    def fake_server(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        return httpx.Response(401, json={"error": "token_expired"})

    async def run_test() -> None:
        transport = httpx.MockTransport(fake_server)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.vinted.example"
        ) as http_client:
            client = ResilientMarketplaceClient(
                MarketplaceName.VINTED, http_client, max_retries=3
            )
            with pytest.raises(SellerAuthExpiredError):
                await client.fetch_listing("v-1")

            # Confirm it only called the server once (no retries on 401)
            assert call_count == 1

    asyncio.run(run_test())


def test_fetch_listing_raises_breakage_error_when_required_field_is_missing() -> None:
    """Test 4: If a marketplace removes a required field (`price_eur`),
    raise `UpstreamSchemaBreakageError` so engineers get alerted.
    """

    def fake_server(request: httpx.Request) -> httpx.Response:
        # Missing `price_eur` field
        return httpx.Response(200, json={"external_id": "v-1", "title": "Shoes"})

    async def run_test() -> None:
        transport = httpx.MockTransport(fake_server)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.vinted.example"
        ) as http_client:
            client = ResilientMarketplaceClient(
                MarketplaceName.VINTED, http_client, max_retries=1
            )
            with pytest.raises(UpstreamSchemaBreakageError):
                await client.fetch_listing("v-1")

    asyncio.run(run_test())


def test_delist_across_marketplaces_succeeds_on_vinted_even_if_ebay_fails() -> None:
    """Test 5: When delisting an item across Vinted and eBay at the same time,
    if eBay returns 503 Server Error, Vinted still succeeds and eBay is marked
    as `retryable=True` for Celery to retry later.
    """

    def vinted_ok_server(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("Idempotency-Key") == "sold-tx-999"
        return httpx.Response(204)

    def ebay_failing_server(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503)

    async def run_test() -> None:
        vinted_transport = httpx.MockTransport(vinted_ok_server)
        ebay_transport = httpx.MockTransport(ebay_failing_server)

        async with httpx.AsyncClient(
            transport=vinted_transport, base_url="https://vinted.example"
        ) as vinted_http, httpx.AsyncClient(
            transport=ebay_transport, base_url="https://ebay.example"
        ) as ebay_http:
            vinted_client = ResilientMarketplaceClient(
                MarketplaceName.VINTED,
                vinted_http,
                max_retries=1,
                base_backoff_sec=0.005,
            )
            ebay_client = ResilientMarketplaceClient(
                MarketplaceName.EBAY,
                ebay_http,
                max_retries=1,
                base_backoff_sec=0.005,
            )

            outcomes = await delist_across_marketplaces(
                targets=[(vinted_client, "v-100"), (ebay_client, "eb-200")],
                idempotency_key="sold-tx-999",
            )

            assert len(outcomes) == 2
            assert outcomes[0].marketplace == MarketplaceName.VINTED
            assert outcomes[0].success is True

            assert outcomes[1].marketplace == MarketplaceName.EBAY
            assert outcomes[1].success is False
            assert outcomes[1].retryable is True

    asyncio.run(run_test())
