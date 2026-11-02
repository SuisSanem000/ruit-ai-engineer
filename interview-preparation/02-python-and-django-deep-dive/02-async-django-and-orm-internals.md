# Async in Django & Django ORM Basics

> **Honest Context:** Tell Luis you know SQL, Prisma/TypeORM, and async web servers deeply from Node.js, and you reviewed how Django handles ASGI and ORM queries.
> **Code Examples:** See [`django_concepts_examples.py`](./python-django-labs/django_concepts_examples.py) for commented Django ORM patterns.

---

## 1. WSGI vs ASGI in Django

- **WSGI (`Gunicorn`):**
  - The classic **synchronous** way to run Django.
  - One worker thread handles one HTTP request from start to finish and blocks until done.
- **ASGI (`Uvicorn` / `Daphne`):**
  - The modern **asynchronous** way to run Django.
  - Supports `async def` views, long-lived **WebSockets (`Django Channels`)**, and handling many slow HTTP requests at the same time on one event loop.

---

## 2. How Async Works in Django (And the 3 Common Mistakes)

- **Mistake 1 — Calling Sync Code Directly Inside an `async def` View:**
  - If you run normal synchronous Django database queries or `requests.get()` directly inside an `async def` view, it blocks the event loop.
  - Django actually stops you and throws a **`SynchronousOnlyOperation`** error if you call sync ORM code inside an async view.
- **Mistake 2 — Mixing Sync and Async Without Bridge Helpers:**
  - **`sync_to_async`:** Wraps a normal synchronous function (like a database transaction) so you can `await` it safely from an `async def` view (it runs the sync code in a background thread).
  - **`async_to_sync`:** Lets synchronous code (like a normal Celery worker task) call an `async def` function (like an async `httpx` marketplace client).
- **Mistake 3 — Lazy Foreign Keys & `transaction.atomic()` in Async:**
  - Django 4.1+ added async ORM methods with an `a` prefix: `aget()`, `acount()`, `acreate()`, `aiterator()`.
  - **Lazy Loading Trap:** In Django, accessing `item.seller.name` runs a hidden synchronous database query if `seller` was not already loaded. In an `async def` view, this throws an error unless you pre-load `seller` using **`select_related("seller")`**.
  - **Transactions Trap:** `transaction.atomic()` does not work directly with `await` steps inside it. Instead, put the whole database transaction inside a normal `def` function and call it with `await sync_to_async(my_tx_function)()`.

---

## 3. Django ORM & Fixing the N+1 Query Problem

- **What is the N+1 Problem?**
  - You fetch 100 items (`1 query`), and then loop through them to read `item.seller.email`, causing Django to run `100 separate SQL queries` (101 queries total).
- **`select_related` (For Single Relationships: `ForeignKey` / `OneToOne`):**
  - Uses a **SQL `JOIN`** to fetch the item and its seller in **1 single query**.
  - Use this when each item points to one parent object (e.g., `Item` $\rightarrow$ `Seller`).
- **`prefetch_related` (For Lists: `ManyToMany` / Reverse `ForeignKey`):**
  - Runs **2 separate SQL queries** (one for the items, and one `WHERE item_id IN (...)` for all their marketplace listings) and joins them together in Python memory.
  - Use this when one item has a list of many child objects (e.g., `Item` $\rightarrow$ `MarketplaceListings`).

---

## 4. Other Useful Django ORM Tips

- **Atomic Math Updates (`F()` expressions):**
  - Instead of reading a number in Python, adding 1, and saving (which causes race conditions), use Django's `F("retry_count") + 1` so Postgres does `SET retry_count = retry_count + 1` atomically in SQL.
- **Saving Only Changed Columns (`update_fields`):**
  - Always call `item.save(update_fields=["status"])` instead of bare `item.save()` so Django only updates the column that changed instead of overwriting every column in the row.
- **Streaming Large Tables (`.iterator()`):**
  - `Item.objects.all()` loads all rows into RAM at once. For large tables, use `.iterator(chunk_size=2000)` so database rows stream in small batches without running out of memory.
