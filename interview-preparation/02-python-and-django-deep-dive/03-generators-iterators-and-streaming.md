# Generators, Iterators & Streaming Pipelines in Python

> **Luis's Cheat Sheet Topic:** *"gauge the extent of your Python and Django knowledge, especially around the GIL, async in Django, generators..."*

---

## 1. Iterables vs Iterators vs Generators

Understanding the exact protocol hierarchy lets you explain generators from first principles:

1. **Iterable:** Any object Implementing `__iter__()` which returns an **Iterator** (e.g., `list`, `dict`, `set`, Django `QuerySet`). You can loop over a `list` multiple times because each `iter(my_list)` creates a *fresh* iterator cursor.
2. **Iterator:** Any state-holding cursor object implementing both `__iter__()` (returns `self`) and **`__next__()`** (returns the next item or raises `StopIteration` when exhausted). **Iterators are single-pass**—once exhausted, calling `next()` raises `StopIteration` forever.
3. **Generator:** A special, concise **Iterator** created automatically by Python whenever a function contains the `yield` keyword (or via a generator expression `(x for x in data)`).

### What Happens in Memory When a Generator Runs?
When you call a regular function `def get_items():`, Python allocates a stack frame, executes the function to completion, returns the full list in RAM, and destroys the frame.  
When you call a generator function `def stream_items():`, **zero lines of the function body execute immediately**! Instead:
- Python returns a `<generator object>` whose stack frame (`gi_frame` with instruction pointer `f_lasti` and local variables `f_locals`) is allocated on the **heap**.
- Each call to `next(gen)` resumes execution right where it left off, runs until the next `yield val`, returns `val` to the caller, and **freezes the stack frame in place**.

---

## 2. Why Generators Are Essential at Ruit (Memory & Latency)

Imagine syncing a professional vintage store's catalog of **100,000 listings** with high-res metadata (5 KB per item):
- **Eager List Approach (`[parse(x) for x in raw]`):** Allocates ~500 MB+ of RAM per worker process, spikes garbage collection pauses, and nothing reaches the database until all 100,000 items finish parsing.
- **Lazy Generator Pipeline (`yield`):** Uses **$O(1)$ constant memory (~a few kilobytes)** regardless of whether the feed has 100 items or 100,000,000 items, and starts writing the first batch immediately!

### Composable Streaming Pipeline Pattern (Unix Pipes in Python)
You can chain generators together so data flows item-by-item through transformation stages with near-zero memory overhead:

```python
from collections.abc import Iterable, Iterator
from itertools import islice
from typing import TypeVar

T = TypeVar("T")


def read_ndjson_lines(file_path: str) -> Iterator[str]:
    """Stage 1: Lazily streams lines from a multi-GB file (like Simin's JSON Viewer!)."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                yield stripped


def chunked_batches(iterable: Iterable[T], batch_size: int = 500) -> Iterator[list[T]]:
    """Stage 2: Groups any lazy iterator into fixed-size batches for Django bulk_create."""
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch
```

---

## 3. Advanced Generator Features Luis May Ask About

### 3.1 `yield from` (Sub-Generator Delegation — PEP 380)
Instead of writing nested loops `for item in sub_generator(): yield item`, `yield from sub_generator()` delegates directly to the sub-generator, forwarding `.send()`, `.throw()`, and `.close()` signals automatically.

**Classic Use Case at Ruit:** Flattening recursive marketplace category trees (e.g., Vinted / eBay nested category hierarchies):
```python
from collections.abc import Iterator
from typing import Any


def flatten_category_tree(node: dict[str, Any], parent_path: str = "") -> Iterator[tuple[int, str]]:
    """Recursively yields (category_id, 'Women > Shoes > Boots') in O(depth) memory."""
    current_path = f"{parent_path} > {node['name']}" if parent_path else node["name"]
    if "id" in node:
        yield (node["id"], current_path)
    for child in node.get("children", []):
        yield from flatten_category_tree(child, current_path)
```

### 3.2 Generators Power Context Managers (`@contextlib.contextmanager`)
Every time you write `@contextmanager`, a single `yield` splits the function into `__enter__` (before `yield`) and `__exit__` (inside the `finally:` block after `yield`). If an exception happens inside the `with` block, Python injects that exception into the generator at the `yield` point via `gen.throw(exc)`!

```python
from contextlib import contextmanager
from collections.abc import Iterator
import time
import logging

logger = logging.getLogger(__name__)


@contextmanager
def measure_marketplace_latency(marketplace: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield  # Code inside the `with` block executes here!
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("marketplace=%s duration_ms=%.2f", marketplace, elapsed_ms)
```

### 3.3 Async Generators (`async def` + `yield` $\rightarrow$ `async for`)
When scraping or syncing paginated APIs asynchronously with `httpx.AsyncClient`, combine `async def` and `yield` to create an **`AsyncIterator`**:

```python
from collections.abc import AsyncIterator
import httpx


async def paginate_marketplace_listings(
    client: httpx.AsyncClient, seller_id: str
) -> AsyncIterator[dict]:
    """Lazily fetches pages only as fast as the consumer processes items (natural backpressure!)."""
    cursor: str | None = None
    while True:
        params = {"seller_id": seller_id, "limit": 100}
        if cursor:
            params["cursor"] = cursor

        resp = await client.get("/v2/listings", params=params)
        resp.raise_for_status()
        payload = resp.json()

        for item in payload.get("items", []):
            yield item

        cursor = payload.get("next_cursor")
        if not cursor:
            break
```
> **Why This Impresses Senior Interviewers:** Notice how an `AsyncGenerator` provides **automatic backpressure**! The next HTTP page is *only* fetched when the caller's `async for item in paginate_marketplace_listings(...):` finishes processing the current page's items.
