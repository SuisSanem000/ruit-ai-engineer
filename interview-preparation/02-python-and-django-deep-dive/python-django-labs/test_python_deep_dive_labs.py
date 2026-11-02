"""
Basic Runnable Labs for Module 2: Python Generators, Async, and Pydantic

What this file shows (in simple, basic Python):
1. How a generator function (`yield`) produces items one at a time without building a big list in RAM.
2. How `yield from` flattens a nested tree of marketplace categories.
3. How an `async` generator (`async for`) streams pages of items from an API on demand.
4. How a basic Pydantic model validates a product and checks that a discount is valid.

Run with:
    .venv/bin/pytest interview-preparation/02-python-and-django-deep-dive/python-django-labs/ -v
"""

import asyncio
from decimal import Decimal
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Tuple

import pytest
from django_concepts_examples import add_tag_safe, explain_django_orm_patterns
from pydantic import BaseModel, Field, field_validator, model_validator

# =====================================================================
# LAB 1: BASIC GENERATOR (`yield`) FOR BATCHING ITEMS
# Instead of loading 100,000 items into memory at once, we group them
# into small batches of `batch_size` one batch at a time.
# =====================================================================


def create_batches(items: List[int], batch_size: int) -> Iterator[List[int]]:
    """A basic generator that yields small lists of size `batch_size`."""
    current_batch: List[int] = []

    for item in items:
        current_batch.append(item)
        # When the batch reaches the target size, yield it and pause!
        if len(current_batch) == batch_size:
            yield current_batch
            # When the caller asks for the next batch, start a fresh list
            current_batch = []

    # If there are leftover items at the end, yield the final smaller batch
    if len(current_batch) > 0:
        yield current_batch


# =====================================================================
# LAB 2: USING `yield from` TO FLATTEN A CATEGORY TREE
# Marketplaces like Vinted and eBay have nested categories:
# Fashion -> Jackets -> Leather.
# =====================================================================


def flatten_category_tree(
    node: Dict[str, Any], parent_path: str = ""
) -> Iterator[Tuple[int, str]]:
    """Yields `(category_id, full_path_string)` for each category node."""
    if parent_path:
        current_path = f"{parent_path} > {node['name']}"
    else:
        current_path = node["name"]

    # Yield the current category first
    if "id" in node:
        yield (int(node["id"]), current_path)

    # Then recursively yield all child categories using `yield from`
    for child in node.get("children", []):
        yield from flatten_category_tree(child, current_path)


# =====================================================================
# LAB 3: ASYNC GENERATOR (`async def` + `yield`)
# Fetches pages one by one only when the `async for` loop needs more items.
# =====================================================================


async def stream_pages_lazily(
    pages: List[List[Dict[str, Any]]],
    fetched_page_indexes: List[int],
) -> AsyncIterator[Dict[str, Any]]:
    """Simulates fetching paginated API items one page at a time."""
    for page_index, page_items in enumerate(pages):
        # Simulate a tiny network wait for fetching this page
        await asyncio.sleep(0.001)
        fetched_page_indexes.append(page_index)

        # Yield each item on the page one by one
        for item in page_items:
            yield item


# =====================================================================
# LAB 4: BASIC PYDANTIC MODEL WITH FIELD & CROSS-FIELD VALIDATION
# =====================================================================


class ProductInput(BaseModel):
    """Validates a seller's product before sending it to marketplaces."""

    sku: str = Field(min_length=2)
    price_eur: Decimal = Field(gt=Decimal(0))
    discount_price_eur: Optional[Decimal] = None

    # Clean up strings like "50,00 €" before Pydantic parses the Decimal
    @field_validator("price_eur", mode="before")
    @classmethod
    def clean_euro_string(cls, value: Any) -> Decimal:
        if isinstance(value, str):
            value = value.replace("€", "").replace(",", ".").strip()
        return Decimal(str(value))

    # `@model_validator(mode="after")` checks rules that compare TWO fields together
    @model_validator(mode="after")
    def validate_discount_is_smaller_than_price(self) -> "ProductInput":
        if (
            self.discount_price_eur is not None
            and self.discount_price_eur >= self.price_eur
        ):
            raise ValueError("discount_price_eur must be lower than price_eur")
        return self


# =====================================================================
# PYTEST TESTS VERIFYING ALL EXAMPLES ABOVE
# =====================================================================


def test_generators_and_category_tree_flattener() -> None:
    # 1. Test batch generator
    batches = list(create_batches([1, 2, 3, 4, 5], batch_size=2))
    assert batches == [[1, 2], [3, 4], [5]]

    # 2. Test category tree flattener
    category_tree = {
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
    flat_list = list(flatten_category_tree(category_tree))
    assert flat_list == [
        (1, "Fashion"),
        (10, "Fashion > Jackets"),
        (101, "Fashion > Jackets > Leather"),
        (20, "Fashion > Shoes"),
    ]


def test_async_generator_stops_fetching_when_loop_breaks_early() -> None:
    pages = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}, {"id": 4}],
        [{"id": 5}, {"id": 6}],  # Page 2 should NEVER be fetched if we stop at id=3!
    ]
    fetched_pages: List[int] = []

    async def run_test() -> List[int]:
        collected_ids: List[int] = []
        async for item in stream_pages_lazily(pages, fetched_pages):
            collected_ids.append(item["id"])
            if item["id"] == 3:
                break
        return collected_ids

    result = asyncio.run(run_test())
    assert result == [1, 2, 3]
    # Because generators are lazy, page index 2 was never fetched!
    assert fetched_pages == [0, 1]


def test_pydantic_validation_and_safe_default_arguments() -> None:
    # 1. Test Pydantic cleaning "50,00 €"
    product = ProductInput(
        sku="JKT-01",
        price_eur="50,00 €",  # type: ignore[arg-type]
        discount_price_eur=Decimal("39.99"),
    )
    assert product.price_eur == Decimal("50.00")

    # 2. Test Pydantic rejecting a discount higher than the original price
    with pytest.raises(ValueError, match="lower than price_eur"):
        ProductInput(
            sku="JKT-02",
            price_eur=Decimal("20.00"),
            discount_price_eur=Decimal("25.00"),
        )

    # 3. Test safe default list function and Django ORM summary
    assert add_tag_safe("vintage") == ["vintage"]
    assert add_tag_safe("leather") == ["leather"]
    assert "select_related" in explain_django_orm_patterns()["single_foreign_key"]
