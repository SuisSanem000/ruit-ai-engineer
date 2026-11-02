"""Runnable code labs for Module 2: Python & Django Deep Dive.

Run with:
    .venv/bin/pytest interview-preparation/02-python-and-django-deep-dive/python-django-labs/ -v
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from decimal import Decimal
from itertools import islice
from typing import (
    Any,
    Generic,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

import pytest
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

T = TypeVar("T")
E = TypeVar("E")


# ============================================================================
# Lab 1: Generators, `yield from`, Lazy Batching & `@contextmanager`
# ============================================================================


def flatten_category_hierarchy(
    node: dict[str, Any], parent_path: str = ""
) -> Iterator[tuple[int, str]]:
    """Uses `yield from` to lazily flatten an arbitrarily nested marketplace category tree."""
    current_path = f"{parent_path} > {node['name']}" if parent_path else node["name"]
    if "id" in node:
        yield (int(node["id"]), current_path)
    for child in node.get("children", []):
        yield from flatten_category_hierarchy(child, current_path)


def lazy_chunks(iterable: Iterable[T], chunk_size: int) -> Iterator[list[T]]:
    """Streams an arbitrarily large iterable in fixed-size chunks with O(chunk_size) RAM."""
    it = iter(iterable)
    while batch := list(islice(it, chunk_size)):
        yield batch


@contextmanager
def tracked_sync_session(marketplace: str, audit_log: list[str]) -> Iterator[str]:
    """Demonstrates how a single `yield` powers __enter__ and __exit__ in context managers."""
    session_id = f"sess-{marketplace}-001"
    audit_log.append(f"OPEN:{session_id}")
    try:
        yield session_id
    except Exception as exc:
        audit_log.append(f"ERROR:{session_id}:{type(exc).__name__}")
        raise
    finally:
        audit_log.append(f"CLOSE:{session_id}")


# ============================================================================
# Lab 2: Async Generators (`async for`) with Natural Backpressure
# ============================================================================


async def stream_paginated_catalog(
    pages: list[list[dict[str, Any]]],
    fetch_log: list[int],
) -> AsyncIterator[dict[str, Any]]:
    """Simulates an async generator fetching pages on demand."""
    for page_idx, page_items in enumerate(pages):
        await asyncio.sleep(0.001)
        fetch_log.append(page_idx)
        for item in page_items:
            yield item


# ============================================================================
# Lab 3: Robust Python — `Protocol`, Rust-style `Result[T, E]`, & Pydantic v2
# ============================================================================


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    is_ok: Literal[True] = True


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E
    is_ok: Literal[False] = False


Result = Union[Ok[T], Err[E]]  # noqa: UP007


@runtime_checkable
class PriceNormalizerProtocol(Protocol):
    def to_cents(self) -> int: ...


class CrossListingItem(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    sku: str = Field(min_length=2)
    price_eur: Decimal = Field(gt=Decimal(0))
    discount_price_eur: Optional[Decimal] = None  # noqa: UP045

    @field_validator("price_eur", mode="before")
    @classmethod
    def parse_euro_string(cls, v: Any) -> Decimal:
        if isinstance(v, str):
            v = v.replace("€", "").replace(",", ".").strip()
        return Decimal(str(v))

    @model_validator(mode="after")
    def check_discount_is_lower_than_price(self) -> CrossListingItem:
        if (
            self.discount_price_eur is not None
            and self.discount_price_eur >= self.price_eur
        ):
            raise ValueError("discount_price_eur must be strictly less than price_eur")
        return self

    def to_cents(self) -> int:
        effective = (
            self.discount_price_eur
            if self.discount_price_eur is not None
            else self.price_eur
        )
        return int(effective * 100)


# ============================================================================
# Pytest Verification Suite
# ============================================================================


def test_yield_from_category_flattener_and_lazy_chunks() -> None:
    tree = {
        "id": 1,
        "name": "Fashion",
        "children": [
            {
                "id": 10,
                "name": "Jackets",
                "children": [{"id": 101, "name": "Leather"}],
            },
            {"id": 20, "name": "Shoes"},
        ],
    }
    flattened = list(flatten_category_hierarchy(tree))
    assert flattened == [
        (1, "Fashion"),
        (10, "Fashion > Jackets"),
        (101, "Fashion > Jackets > Leather"),
        (20, "Fashion > Shoes"),
    ]

    batches = list(lazy_chunks(range(7), chunk_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6]]


def test_contextmanager_cleanup_on_exception() -> None:
    audit_log: list[str] = []
    with pytest.raises(RuntimeError), tracked_sync_session(
        "wallapop", audit_log
    ) as sess_id:
        assert sess_id == "sess-wallapop-001"
        raise RuntimeError("socket reset")

    assert audit_log == [
        "OPEN:sess-wallapop-001",
        "ERROR:sess-wallapop-001:RuntimeError",
        "CLOSE:sess-wallapop-001",
    ]


def test_async_generator_backpressure_stops_fetching_early() -> None:
    pages = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}, {"id": 4}],
        [{"id": 5}, {"id": 6}],  # Should NEVER be fetched if consumer stops at id=3!
    ]
    fetch_log: list[int] = []

    async def _consume() -> list[int]:
        collected: list[int] = []
        async for item in stream_paginated_catalog(pages, fetch_log):
            collected.append(item["id"])
            if item["id"] == 3:
                break
        return collected

    result = asyncio.run(_consume())
    assert result == [1, 2, 3]
    assert fetch_log == [0, 1]  # Page 2 was never fetched thanks to lazy evaluation!


def test_pydantic_v2_and_protocol_structural_typing() -> None:
    raw_json = b'{"sku": "  VINT-01 ", "price_eur": "50,00 \xe2\x82\xac", "discount_price_eur": "39.99"}'
    item = CrossListingItem.model_validate_json(raw_json)

    assert isinstance(item, PriceNormalizerProtocol)
    assert item.sku == "VINT-01"
    assert item.to_cents() == 3999

    with pytest.raises(ValueError, match="strictly less than price_eur"):
        CrossListingItem(
            sku="VINT-02",
            price_eur=Decimal("20.00"),
            discount_price_eur=Decimal("25.00"),
        )
