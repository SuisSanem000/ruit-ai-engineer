# Generators (`yield`) & Streaming in Python

> **Luis's Cheat Sheet:** *"gauge the extent of your Python and Django knowledge, especially around the GIL, async in Django, generators..."*

---

## 1. What Is a Generator?

- **Normal Function (`return`):**
  - Builds the **entire list** in memory first, then returns all items at once.
  - If there are 500,000 items, it uses hundreds of megabytes of RAM.
- **Generator Function (`yield`):**
  - Uses the **`yield`** keyword instead of `return`.
  - When you call a generator function, it does not run the code right away—it returns a **generator object** (an iterator).
  - Each time a `for` loop asks for the next item (`next()`), the function runs until it hits `yield`, gives back **that one item**, and **pauses** (saving its local variables right where it stopped).
  - On the next loop step, it wakes up from that exact line and continues until no items are left.

---

## 2. Why Generators Are Great for Ruit

- **Almost Zero Memory Use ($O(1)$ RAM):**
  - Just like when you worked on the Dadroit JSON Viewer for multi-GB files, you cannot load 100,000 seller listings into RAM all at once.
  - A generator processes **one item (or one small batch of 100 items) at a time**, keeping memory flat.
- **Faster Start Time:**
  - You start processing the first item immediately instead of waiting for all pages to download first.
- **Chaining Pipelines:**
  - You can connect generators together like Unix pipes:
    - Generator 1 reads raw lines from a file or API.
    - Generator 2 cleans and validates each item.
    - Generator 3 groups valid items into batches of 100 for database insert.

---

## 3. Useful Generator Features to Mention

- **Generator Expressions:**
  - Using `[x * 2 for x in items]` with square brackets creates a full list in memory.
  - Using `(x * 2 for x in items)` with parentheses creates a **lazy generator** that calculates values one by one using almost no memory.
- **`yield from`:**
  - A clean shortcut to yield all items from another generator or a recursive function (for example, flattening a nested tree of marketplace categories).
- **Async Generators (`async def` + `yield`):**
  - When fetching paginated items from an API using `async/await`, you can use `yield` inside an `async def` function and loop over it with **`async for`**.
  - It only fetches Page 2 after your loop finishes processing Page 1 (natural rate control!).

---

## 4. Simple Code Examples

- Open [test_python_deep_dive_labs.py](./python-django-labs/test_python_deep_dive_labs.py) to see basic, commented examples of `yield`, batching, `yield from`, and `async for`.
