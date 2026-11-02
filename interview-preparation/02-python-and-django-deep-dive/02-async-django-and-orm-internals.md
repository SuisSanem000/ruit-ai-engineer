# Async in Django & ORM Concepts

> **Luis's Cheat Sheet:** *"orms and sql ... async in Django"*

---

## 1. WSGI vs ASGI (How Django Runs on a Server)

- **WSGI (e.g., `Gunicorn`):**
  - The classic synchronous way to run Django.
  - One worker thread handles one request at a time from start to finish.
- **ASGI (e.g., `Uvicorn` or `Daphne`):**
  - The modern asynchronous way to run Django.
  - Supports `async def` views, high-concurrency network calls, and **WebSockets (`Django Channels`)**.

---

## 2. How Async Works in Django (And the Main Traps)

- **Why Django is a hybrid framework:**
  - Django was originally built as a synchronous framework, and async support was added on top.
  - While views can be `async def`, parts of the database ORM are still synchronous under the hood.
- **Trap 1 — Calling sync code inside an `async def` view:**
  - If you call synchronous Django ORM queries directly inside an `async def` view, Django raises a **`SynchronousOnlyOperation` error** to protect you from freezing the event loop.
- **Trap 2 — Bridging Sync and Async (`sync_to_async` & `async_to_sync`):**
  - **`sync_to_async`:** Runs a synchronous function (like a DB transaction) safely in a background thread so you can `await` it inside an `async def` view.
  - **`async_to_sync`:** Lets synchronous code (like a standard Celery task) run an `async` function.
- **Trap 3 — Lazy Foreign Keys in Async Views:**
  - In Django, if you load an `item` and then access `item.seller.name`, Django secretly runs a synchronous database query if `seller` was not loaded yet.
  - Inside an `async def` view, that secret query will crash!
  - **Fix:** Always pre-load foreign keys upfront using **`select_related('seller')`**.
- **Trap 4 — Database Transactions (`transaction.atomic`):**
  - `transaction.atomic()` only works in synchronous code.
  - If you need a database transaction inside an `async def` view, put the whole transaction inside a normal `def` helper function and call it with `await sync_to_async(my_helper)()`.

---

## 3. Django ORM & SQL Optimization

- **The N+1 Query Problem:**
  - Loading 100 items in 1 query, then looping over them and running 100 extra queries to get each item's seller or listings.
- **`select_related` vs `prefetch_related` (Very Common Question!):**
  - **`select_related`:** Used for **single relationships** (`ForeignKey` or `OneToOne`). It uses a single SQL **`JOIN`** to fetch everything in **1 query**.
  - **`prefetch_related`:** Used for **lists of items** (`ManyToMany` or reverse `ForeignKey`, like all marketplace listings for an item). It runs **2 separate queries** (`SELECT ... WHERE item_id IN (...)`) and joins them in Python memory.
- **Atomic Database Updates (`F` expressions):**
  - Instead of reading a number into Python, adding 1, and saving it back (which causes race conditions), use Django's **`F()` expression** so PostgreSQL updates the counter atomically in SQL.
- **Saving Memory on Big Queries (`.iterator()`):**
  - Normally, `Item.objects.all()` loads and caches all rows in RAM.
  - For 100,000 rows, use **`.iterator(chunk_size=2000)`** so Django streams rows in small chunks without running out of memory.

---

## 4. Simple Code Examples

- Open [django_concepts_examples.py](./python-django-labs/django_concepts_examples.py) to see basic, commented examples of Django ORM queries, locks, and async views.
