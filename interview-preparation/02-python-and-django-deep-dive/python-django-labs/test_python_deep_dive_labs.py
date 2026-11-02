"""Basic Python Practice Examples for Module 2 (Generators, Async, Pydantic & Gotchas).

WHAT THIS FILE DOES:
Shows simple, easy-to-read Python examples of the topics on Luis's cheat sheet:
1. Generators (`yield` and `yield from`) to process items lazily without using much RAM.
2. Context managers (`@contextmanager`) using `yield` for setup and cleanup.
3. Async generators (`async def` + `yield`) to stream API pages one by one.
4. Basic Pydantic validation to clean prices and check business rules.
5. How to avoid the classic Python "mutable default argument" bug.

Run in terminal:
    .venv/bin/pytest interview-preparation/02-python-and-django-deep-dive/python-django-labs/ -v
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterable, Iterator
from contextlib import contextmanager
from decimal import Decimal
from itertools import islice
from typing import Any, Optional

import pytest
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ============================================================================
# 1. Generators (`yield` and `yield from`)
# ============================================================================


def flatten_category_tree(
    node: dict[str, Any], parent_path: str = ""
) -> Iterator[tuple[int, str]]:
    """Walks a nested marketplace category dictionary and yields `(id, full_path)`
    one item at a time using `yield` and `yield from`.

    Why use `yield` here?
    Instead of building a big list in memory, `yield` pauses the function and
    hands back one category at a time to the caller.
    """
    current_path = f"{parent_path} > {node['name']}" if parent_path else node["name"]

    if "id" in node:
        yield (int(node["id"]), current_path)

    # `yield from` delegates to the recursive generator call cleanly
    for child in node.get("children", []):
        yield from flatten_category_tree(child, current_path)


def chunked_batches(items: Iterable[int], batch_size: int) -> Iterator[list[int]]:
    """Splits a large stream of items into small fixed-size lists (batches).

    Useful when reading 50,000 items from a file or generator and inserting
    them into the database 500 rows at a time.
    """
    iterator = iter(items)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch


# ============================================================================
# 2. Context Manager Using `yield` (`@contextmanager`)
# ============================================================================


@contextmanager
def tracked_sync_session(marketplace: str, log_list: list[str]) -> Iterator[str]:
    """Shows how `yield` powers a Python `with ... as ...:` block.
    1. Code before `yield` runs when entering the `with` block.
    2. `yield` hands the `session_id` to the caller's `with` block.
    3. The `finally:` block ALWAYS runs at the end, even if an error happened!
    """
    session_id = f"sess-{marketplace}-001"
    log_list.append(f"OPEN:{session_id}")
    try:
        yield session_id
    except Exception as exc:
        log_list.append(f"ERROR:{session_id}:{type(exc).__name__}")
        raise
    finally:
        log_list.append(f"CLOSE:{session_id}")


# ============================================================================
# 3. Async Generator (`async def` + `yield`)
# ============================================================================


async def stream_paginated_catalog(
    pages: list[list[dict[str, Any]]],
    fetched_page_indexes: list[int],
) -> AsyncIterator[dict[str, Any]]:
    """Simulates fetching paginated items from an API one page at a time.

    Because it uses `yield`, it only fetches Page 2 after the caller finishes
    looping through Page 1. If the caller stops early (`break`), later pages
    are never fetched at all!
    """
    for page_index, page_items in enumerate(pages):
        await asyncio.sleep(0.001)
        fetched_page_indexes.append(page_index)
        for item in page_items:
            yield item


# ============================================================================
# 4. Basic Pydantic Model for Product Validation
# ============================================================================


class CrossListingItem(BaseModel):
    """Validates a product before sending it to a marketplace."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    sku: str = Field(min_length=2)
    price_eur: Decimal = Field(gt=Decimal(0))
    discount_price_eur: Optional[Decimal] = None  # noqa: UP045

    @field_validator("price_eur", mode="before")
    @classmethod
    def clean_euro_string(cls, value: Any) -> Decimal:
        """Turns a messy string like `'50,00 €'` into `Decimal('50.00')`."""
        if isinstance(value, str):
            value = value.replace("€", "").replace(",", ".").strip()
        return Decimal(str(value))

    @model_validator(mode="after")
    def check_discount_is_cheaper_than_normal_price(self) -> CrossListingItem:
        """Checks a business rule that depends on two fields together."""
        if (
            self.discount_price_eur is not None
            and self.discount_price_eur >= self.price_eur
        ):
            raise ValueError("discount_price_eur must be lower than price_eur")
        return self

    def to_cents(self) -> int:
        """Returns the active price in integer euro cents (e.g. 39.99 -> 3999)."""
        final_price = (
            self.discount_price_eur
            if self.discount_price_eur is not None
            else self.price_eur
        )
        return int(final_price * 100)


# ============================================================================
# 5. Avoiding the Classic Python Mutable Default List Gotcha
# ============================================================================


def add_marketplace_tag_safely(
    tag: str, existing_tags: list[str] | None = None
) -> list[str]:
    """In Python, NEVER write `def add_tag(tag, existing_tags=[]):` because
    Python creates that default `[]` list only once and shares it across calls!
    Always default to `None` and create a fresh list inside the function.
    """
    tags = list(existing_tags) if existing_tags is not None else []
    tags.append(tag)
    return tags


# ============================================================================
# Pytest Tests
# ============================================================================


def test_generators_flatten_tree_and_chunk_batches() -> None:
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
    flattened = list(flatten_category_tree(tree))
    assert flattened == [
        (1, "Fashion"),
        (10, "Fashion > Jackets"),
        (101, "Fashion > Jackets > Leather"),
        (20, "Fashion > Shoes"),
    ]

    batches = list(chunked_batches(range(7), batch_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6]]


def test_contextmanager_always_closes_session_on_error() -> None:
    log_list: list[str] = []
    with pytest.raises(RuntimeError), tracked_sync_session(
        "wallapop", log_list
    ) as sess_id:
        assert sess_id == "sess-wallapop-001"
        raise RuntimeError("network lost")

    assert log_list == [
        "OPEN:sess-wallapop-001",
        "ERROR:sess-wallapop-001:RuntimeError",
        "CLOSE:sess-wallapop-001",
    ]


def test_async_generator_stops_fetching_pages_when_consumer_breaks() -> None:
    pages = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}, {"id": 4}],
        [{"id": 5}, {"id": 6}],  # Page index 2 should never be fetched!
    ]
    fetched_pages: list[int] = []

    async def run_test() -> list[int]:
        seen_ids: list[int] = []
        async for item in stream_paginated_catalog(pages, fetched_pages):
            seen_ids.append(item["id"])
            if item["id"] == 3:
                break
        return seen_ids

    result = asyncio.run(run_test())
    assert result == [1, 2, 3]
    assert fetched_pages == [0, 1]


def test_pydantic_validation_and_safe_default_arguments() -> None:
    raw_json = b'{"sku": "  VINT-01 ", "price_eur": "50,00 \xe2\x82\xac", "discount_price_eur": "39.99"}'
    item = CrossListingItem.model_validate_json(raw_json)

    assert item.sku == "VINT-01"
    assert item.to_cents() == 3999

    with pytest.raises(ValueError, match="lower than price_eur"):
        CrossListingItem(
            sku="VINT-02",
            price_eur=Decimal("20.00"),
            discount_price_eur=Decimal("25.00"),
        )

    # Confirm two separate calls do not share the same default list
    first_call = add_marketplace_tag_safely("vintage")
    second_call = add_marketplace_tag_safely("winter")
    assert first_call == ["vintage"]
    assert second_call == ["winter"]
