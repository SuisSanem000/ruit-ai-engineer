"""
Basic Pytest Unit Tests for `marketplace_connector.py`

How these tests work:
- We use `httpx.MockTransport` to fake the marketplace HTTP responses in memory,
  so tests run in milliseconds without needing the internet.
- Run with: `.venv/bin/pytest interview-preparation/01-ai-workflow-and-live-task/live-task-sandbox/ -v`
"""

import asyncio
from decimal import Decimal

import httpx
import pytest
from marketplace_connector import (
    AuthExpiredError,
    ListingItem,
    SchemaBreakageError,
    delist_across_marketplaces,
    fetch_marketplace_listing,
)


def test_listing_item_cleans_messy_price_and_finds_extra_fields() -> None:
    """Test 1: Check that Pydantic converts integer IDs, cleans '45,50 €',
    and detects new undocumented fields sent by a marketplace.
    """
    raw_vinted_json = {
        "external_id": 987654,
        "title": "  Vintage Leather Jacket  ",
        "price_eur": {"amount": "45,50 €"},
        "currency": "EUR",
        "is_active": True,
        "new_vinted_field": "promoted_v2",
    }

    item = ListingItem.model_validate(raw_vinted_json)

    assert item.external_id == "987654"
    assert item.title == "Vintage Leather Jacket"
    assert item.price_eur == Decimal("45.50")
    assert item.get_unexpected_fields() == {"new_vinted_field"}


def test_fetch_listing_retries_on_429_rate_limit_and_succeeds() -> None:
    """Test 2: Simulate a marketplace returning HTTP 429 (Too Many Requests) on the 1st try,
    and HTTP 200 OK on the 2nd try. Our client should wait and succeed automatically.
    """
    call_count = 0

    def fake_server(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        # First call returns 429 with a tiny Retry-After header
        if call_count == 1:
            return httpx.Response(429, headers={"Retry-After": "0.01"})
        # Second call succeeds with 200 OK
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
        ) as client:
            item = await fetch_marketplace_listing(client, "wallapop", "wp-123")
            assert item.external_id == "wp-123"
            assert item.price_eur == Decimal("120.00")
            assert call_count == 2

    asyncio.run(run_test())


def test_fetch_listing_stops_immediately_on_401_unauthorized() -> None:
    """Test 3: If the seller's token is expired (HTTP 401), do NOT waste time retrying.
    Raise `AuthExpiredError` on the first attempt.
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
        ) as client:
            with pytest.raises(AuthExpiredError):
                await fetch_marketplace_listing(client, "vinted", "v-1", max_retries=3)
            # Must only call the server 1 time (zero retries on 401)
            assert call_count == 1

    asyncio.run(run_test())


def test_fetch_listing_raises_schema_breakage_when_required_field_missing() -> None:
    """Test 4: If the marketplace renames or removes `price_eur`, Pydantic validation fails
    and we raise `SchemaBreakageError` so engineers get alerted.
    """

    def fake_server(request: httpx.Request) -> httpx.Response:
        # Missing required `price_eur` field!
        return httpx.Response(200, json={"external_id": "v-1", "title": "Shoes"})

    async def run_test() -> None:
        transport = httpx.MockTransport(fake_server)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.vinted.example"
        ) as client:
            with pytest.raises(SchemaBreakageError):
                await fetch_marketplace_listing(client, "vinted", "v-1")

    asyncio.run(run_test())


def test_delist_across_marketplaces_handles_partial_failure() -> None:
    """Test 5: When delisting a sold item on Vinted and eBay at the same time,
    if Vinted returns 204 (success) and eBay returns 503 (server down),
    Vinted still succeeds and eBay is marked with `retryable=True`.
    """

    def vinted_ok_server(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("Idempotency-Key") == "sale-999"
        return httpx.Response(204)

    def ebay_failing_server(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503)

    async def run_test() -> None:
        vinted_transport = httpx.MockTransport(vinted_ok_server)
        ebay_transport = httpx.MockTransport(ebay_failing_server)

        async with httpx.AsyncClient(
            transport=vinted_transport, base_url="https://vinted.example"
        ) as vinted_client, httpx.AsyncClient(
            transport=ebay_transport, base_url="https://ebay.example"
        ) as ebay_client:
            targets = [
                {
                    "client": vinted_client,
                    "marketplace": "vinted",
                    "external_id": "v-100",
                },
                {
                    "client": ebay_client,
                    "marketplace": "ebay",
                    "external_id": "eb-200",
                },
            ]

            outcomes = await delist_across_marketplaces(
                targets=targets, idempotency_key="sale-999"
            )

            assert len(outcomes) == 2
            # Vinted succeeded
            assert outcomes[0]["marketplace"] == "vinted"
            assert outcomes[0]["success"] is True
            # eBay failed temporarily and is marked as retryable
            assert outcomes[1]["marketplace"] == "ebay"
            assert outcomes[1]["success"] is False
            assert outcomes[1]["retryable"] is True

    asyncio.run(run_test())
