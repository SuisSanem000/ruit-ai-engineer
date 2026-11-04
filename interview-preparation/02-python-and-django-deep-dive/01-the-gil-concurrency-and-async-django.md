# 01 — The GIL, Concurrency & Async Django Internals

> **Honest Context:** You know SQL, async web servers, and event loops deeply from Node.js, and you reviewed how Python handles the GIL and Django handles ASGI/ORM queries. Code examples are in [`python-django-labs/`](./python-django-labs/).

---

## 1. The GIL (Global Interpreter Lock) & Concurrency in Python

- **What is the GIL?**
  - A mutex in standard CPython that prevents multiple native threads from executing Python bytecode simultaneously.
  - Exists because CPython’s memory management uses reference counting, which is not thread-safe without synchronization.
- **I/O-Bound Work (Marketplace API Calls, DB Queries, Redis):**
  - Python automatically **releases the GIL** during system I/O calls.
  - A single `asyncio` event loop or multi-threaded worker handles thousands of concurrent HTTP requests efficiently.
- **CPU-Bound Work (Image Processing, Deep Parsing, Cryptography):**
  - Python threads **do not** give speedups because they fight for the same GIL.
  - Solution: Use **multiple processes** (`multiprocessing` or separate Celery worker processes) so each worker gets its own CPU core, memory space, and GIL.

---

## 2. WSGI vs. ASGI in Django

- **WSGI (Gunicorn):** Classic **synchronous** Django. One worker thread processes one HTTP request end-to-end and blocks while waiting.
- **ASGI (Uvicorn / Daphne):** Modern **asynchronous** Django. Runs an event loop supporting `async def` views, long-lived WebSockets (`Django Channels`), and high-concurrency external API requests.

---

## 3. How Async Works in Django (And 3 Classic Traps)

- **Trap 1 — Running Sync Code Directly in `async def` Views:**
  - Calling synchronous ORM queries or `requests.get()` inside an async view blocks the entire event loop.
  - Django throws a **`SynchronousOnlyOperation`** exception if sync ORM methods are called inside async contexts.
- **Trap 2 — Sync/Async Bridge Helpers:**
  - **`sync_to_async`:** Wraps synchronous functions (like heavy DB queries or transactions) so they can be awaited in async views by running in a thread pool.
  - **`async_to_sync`:** Wraps async functions (like async `httpx` client calls) so sync Celery workers or views can call them.
- **Trap 3 — Lazy Loading & Transactions:**
  - In Django, accessing `item.seller.name` triggers a hidden synchronous query if `seller` was not prefetched. In async views, this raises an error unless pre-loaded with `select_related("seller")`.
  - Database transactions (`transaction.atomic()`) cannot wrap `await` expressions directly. Encapsulate the transaction in a synchronous function and call it via `await sync_to_async(my_tx)()`.

---

## 4. Django ORM: Eliminating N+1 Queries

- **The N+1 Problem:** Querying 100 items (1 query), then looping to access `item.seller.name`, triggering 100 additional queries (101 total).
- **`select_related` (Single Relationships: `ForeignKey`, `OneToOne`):**
  - Executes a single SQL query using an **`INNER JOIN` / `LEFT JOIN`**.
  - Use when each item has exactly one parent (e.g., `Item` $\rightarrow$ `Seller`).
- **`prefetch_related` (Collections: `ManyToManyField`, Reverse `ForeignKey`):**
  - Executes **2 SQL queries** (Query 1: `SELECT * FROM items;` Query 2: `SELECT * FROM listings WHERE item_id IN (...);`) and joins them in Python memory.
  - Use when one item has many child records (e.g., `Item` $\rightarrow$ `MarketplaceListings`).
- **Atomic Math & Specific Updates:**
  - Use `F("retry_count") + 1` for database-level atomic increments without Python race conditions.
  - Always call `item.save(update_fields=["status"])` so Django updates only modified columns instead of overwriting the whole row.
