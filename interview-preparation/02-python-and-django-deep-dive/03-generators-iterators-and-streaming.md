# Generators, Iterators & Streaming Data in Python

> **Code examples with detailed comments:** [test_python_deep_dive_labs.py](./python-django-labs/test_python_deep_dive_labs.py)

---

## 1. What Is a Generator (`yield`)?

- **Normal Function (`return`):**
  - Builds the **entire list in memory (RAM)** first and returns it all at once.
  - If a seller has 200,000 items, building a full list in RAM uses hundreds of megabytes and can crash the worker (`OutOfMemory`).
- **Generator Function (`yield`):**
  - Uses the `yield` keyword instead of `return`.
  - Produces **one item at a time on demand** and pauses right at the `yield` line until the caller asks for the next item (`for item in my_generator():` or `next()`).
  - Keeps local variables saved while paused, and uses almost **zero extra RAM** whether you loop over 10 items or 10 million items.

---

## 2. Iterable vs Iterator vs Generator

- **Iterable:** Anything you can loop over with a `for` loop (like a `list`, `dict`, or `set`). You can loop over a `list` many times.
- **Iterator:** The object that tracks the current position during a loop using `__next__()` and raises `StopIteration` when finished.
- **Generator:** A simple way to create an **Iterator** just by writing a function with `yield` (or a generator expression like `(x * 2 for x in items)` with round brackets instead of square brackets).
- **Important Quirk:** A generator can only be looped over **once**! After it finishes, it is empty, so looping over the same generator variable a second time yields nothing.

---

## 3. Where Generators Are Useful at Ruit

- **Streaming Large JSON Files or Product Feeds:**
  - Just like in your multi-GB desktop JSON Viewer, you can read a huge product file line by line (`yield line`), validate each item, and group them into batches of 500 items for database insertion without ever loading the whole file into memory.
- **Walking Nested Category Trees (`yield from`):**
  - Marketplaces have deep category trees (e.g., `Fashion > Women > Jackets > Leather`).
  - `yield from` lets a recursive generator call itself on child categories cleanly without writing extra nested `for` loops.
- **Powering `with` Blocks (`@contextmanager`):**
  - In Python, you can turn a simple generator function into a `with` resource manager using `@contextlib.contextmanager`.
  - Setup code runs before `yield`, the caller's `with` block runs at `yield`, and cleanup code runs in a `finally` block after `yield`.
- **Async Generators (`async def` + `yield` $\rightarrow$ `async for`):**
  - When fetching paginated API results from Vinted or eBay (`page 1`, `page 2`, `page 3`...), an `async def` function that uses `yield` fetches the next page **only when the consumer finishes processing the current page** (natural backpressure).
