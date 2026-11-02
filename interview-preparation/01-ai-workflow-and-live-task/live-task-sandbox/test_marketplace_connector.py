"""Pytest suite for Ruit Live AI Task Sandbox."""

from __future__ import annotations

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


def test_normalized_listing_coerces_messy_prices_and_detects_drift() -> None:
    raw_vinted_payload = {
        "external_id": 987654,
        "title": "  Vintage Leather Jacket  ",
        "price_eur": {"amount": "45,50 €"},
        "currency": "EUR",
        "is_active": True,
        "new_undocumented_vinted_badge": "promoted_v2",
    }
    listing = NormalizedListing.model_validate(raw_vinted_payload)
    assert listing.external_id == "987654"
    assert listing.title == "Vintage Leather Jacket"
    assert listing.price_eur == Decimal("45.50")
    assert listing.detect_schema_drift() == {"new_undocumented_vinted_badge"}


def test_fetch_listing_retries_on_429_and_succeeds() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(429, headers={"Retry-After": "0.01"})
        return httpx.Response(
            200,
            json={
                "external_id": "wp-123",
                "title": "Retro Camera",
                "price_eur": "120.00",
            },
        )

    async def _run() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.wallapop.example"
        ) as http_client:
            client = ResilientMarketplaceClient(
                MarketplaceName.WALLAPOP, http_client, max_retries=2
            )
            listing = await client.fetch_listing("wp-123")
            assert listing.external_id == "wp-123"
            assert listing.price_eur == Decimal("120.00")
            assert attempts == 2

    asyncio.run(_run())


def test_fetch_listing_raises_auth_expired_immediately_without_retries() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(401, json={"error": "token_expired"})

    async def _run() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.vinted.example"
        ) as http_client:
            client = ResilientMarketplaceClient(
                MarketplaceName.VINTED, http_client, max_retries=3
            )
            with pytest.raises(SellerAuthExpiredError):
                await client.fetch_listing("v-1")
            assert attempts == 1  # Must not waste retries on 401!

    asyncio.run(_run())


def test_fetch_listing_raises_upstream_schema_breakage_on_corrupt_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        # Marketplace renamed 'price_eur' to 'cost' breaking required field contract
        return httpx.Response(200, json={"external_id": "v-1", "title": "Shoes"})

    async def _run() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://api.vinted.example"
        ) as http_client:
            client = ResilientMarketplaceClient(
                MarketplaceName.VINTED, http_client, max_retries=1
            )
            with pytest.raises(UpstreamSchemaBreakageError):
                await client.fetch_listing("v-1")

    asyncio.run(_run())


def test_delist_across_marketplaces_isolates_partial_failures() -> None:
    def ok_handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("Idempotency-Key") == "sold-tx-999"
        return httpx.Response(204)

    def failing_503_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503)

    async def _run() -> None:
        vinted_transport = httpx.MockTransport(ok_handler)
        ebay_transport = httpx.MockTransport(failing_503_handler)
        async with httpx.AsyncClient(
            transport=vinted_transport, base_url="https://vinted.example"
        ) as vinted_http, httpx.AsyncClient(
            transport=ebay_transport, base_url="https://ebay.example"
        ) as ebay_http:
            vinted_client = ResilientMarketplaceClient(
                MarketplaceName.VINTED, vinted_http, max_retries=1, base_backoff_sec=0.005
            )
            ebay_client = ResilientMarketplaceClient(
                MarketplaceName.EBAY, ebay_http, max_retries=1, base_backoff_sec=0.005
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

    asyncio.run(_run())
