# Async in Django & ORM Internals — Senior Deep Dive

> **Luis's Cheat Sheet Topic:** *"orms and sql ... gauge the extent of your Python and Django knowledge, especially around the GIL, async in Django..."*

---

## 1. WSGI vs ASGI: How Django Runs in Production

| Feature | WSGI (Web Server Gateway Interface) | ASGI (Asynchronous Server Gateway Interface) |
| :--- | :--- | :--- |
| **Servers** | `Gunicorn` (sync workers / `gthread`), `uWSGI` | `Uvicorn` (often managed by Gunicorn `UvicornWorker`), `Daphne`, `Hypercorn` |
| **Execution Model** | **Synchronous:** 1 HTTP request occupies 1 thread/worker from start to finish. | **Asynchronous Event Loop:** 1 worker handles hundreds of concurrent `async def` HTTP requests, WebSockets, and SSE streams. |
| **Long-Lived Connections** | Poor (WebSockets or long-polling quickly exhaust the worker pool). | Native support for **WebSockets (`Django Channels`)**, HTTP/2, and streaming responses. |
| **Entrypoint in Django** | `wsgi.py` (`get_wsgi_application()`) | `asgi.py` (`get_asgi_application()`) |

---

## 2. How Async Works in Django (And Its 4 Hidden Traps!)

Django evolved from a synchronous framework into a **hybrid sync/async framework** (Django 3.1 $\rightarrow$ 5.x). Luis will test whether you understand what happens *under the hood* when you write `async def` in Django.

### Trap 1: Calling Sync Code Directly Inside an `async def` View
If you write an `async def` view Running under `Uvicorn` (ASGI) and call a synchronous library (`requests.get()`, `time.sleep()`, or synchronous Django ORM `Item.objects.all()`), two bad things happen:
1. For synchronous HTTP calls (`requests.get`), **you block the entire event loop thread**—freezing all other concurrent requests on that worker!
2. For synchronous Django ORM calls inside an active event loop, Django actively detects the running event loop and raises **`django.core.exceptions.SynchronousOnlyOperation: You cannot call this from an async context - use a thread or sync_to_async`**!

### Trap 2: How `sync_to_async` and `async_to_sync` Actually Work (`asgiref.sync`)
Django uses `asgiref.sync` to bridge the two worlds:
- **`sync_to_async(func, thread_sensitive=True)`:**
  - Takes a synchronous blocking function and runs it in a background thread so the ASGI event loop isn't blocked.
  - **Why `thread_sensitive=True` is default (and critical!):** Django's database connections (`django.db.connections`) are stored in **thread-local storage** (`asgiref.local.Local`). With `thread_sensitive=True`, all sync functions within the same request run on the **same shared single thread** so they share the same DB connection and transaction state!
  - If you wrap an external CPU/network library that doesn't touch Django's DB connections, pass `thread_sensitive=False` so it runs in a parallel thread pool instead of queuing on the single DB thread.
- **`async_to_sync(coroutine_func)`:**
  - Used when you are inside a **synchronous context** (like a standard Celery task or Django management command) and want to run an `async` coroutine (such as your async `httpx` marketplace client).

### Trap 3: Django's Async ORM Methods (`aget`, `aiterator`, etc.) & `transaction.atomic()`
Django 4.1+ and 5.x provide `a`-prefixed async ORM methods:
```python
item = await Item.objects.select_related("seller").aget(id=item_id)
count = await Item.objects.filter(status="active").acount()

async for listing in Listing.objects.filter(marketplace="vinted").aiterator(chunk_size=1000):
    await process_listing(listing)
```
**What senior engineers know about Django's Async ORM:**
1. **Under the hood:** Most of Django's `a*` ORM methods are thin wrappers around `sync_to_async` calling the underlying synchronous SQL compiler and `psycopg` driver!
2. **Lazy ForeignKey Access Fails in Async Views:**
   ```python
   # BUG: Raises SynchronousOnlyOperation!
   item = await Item.objects.aget(id=1)
   print(item.seller.email)  # `item.seller` triggers a hidden synchronous SQL query!

   # FIX 1: Pre-load with select_related (SQL JOIN)
   item = await Item.objects.select_related("seller").aget(id=1)
   print(item.seller.email)  # Already in memory—zero DB queries!
   ```
3. **`transaction.atomic()` Does NOT Support `async with` Directly:**
   Because database transactions are bound to a specific DB connection on a specific thread, you cannot interleave `await` statements across an open transaction safely in Django ORM yet.
   **The Production Pattern:** Put the entire transactional block inside a synchronous function and call it with `sync_to_async`:
   ```python
   from asgiref.sync import sync_to_async
   from django.db import transaction

   @sync_to_async
   def claim_and_lock_item(item_id: int) -> Item | None:
       with transaction.atomic():
           item = Item.objects.select_for_update(skip_locked=True).filter(id=item_id, status="active").first()
           if item:
               item.status = "processing"
               item.save(update_fields=["status"])
           return item
   ```

### Trap 4: Middleware Ping-Pong Penalty
If your `MIDDLEWARE` list alternates `[SyncMiddlewareA, AsyncMiddlewareB, SyncMiddlewareC]`, Django has to jump EventLoop $\rightarrow$ Thread $\rightarrow$ EventLoop $\rightarrow$ Thread on **every single request**, adding milliseconds of context-switch latency. Keep middleware all-async (using `@sync_and_async_middleware`) when running ASGI!

---

## 3. Mastering Django ORM & SQL Optimization

### 3.1 Solving the N+1 Problem: `select_related` vs `prefetch_related`
This is a guaranteed question in any Django interview:

| Method | Relationship Types | How It Works at the SQL Level | When to Use |
| :--- | :--- | :--- | :--- |
| **`select_related('seller', 'category')`** | `ForeignKey`, `OneToOneField` (single-valued forward relations) | Executes **1 single SQL query** using `INNER JOIN` / `LEFT OUTER JOIN`. | Always use when accessing parent/foreign-key objects in a loop or serializer. |
| **`prefetch_related('marketplace_listings', 'tags')`** | `ManyToManyField`, Reverse `ForeignKey` (`1-to-Many`) | Executes **2 separate SQL queries**: (1) fetches parent rows, (2) fetches child rows via `SELECT ... WHERE item_id IN (1, 2, 3...)`, and **joins them in Python memory**. | Use for collections (`1-to-N` or `M-to-N`) where a SQL JOIN would create a huge Cartesian product of duplicate parent columns. |

**Advanced `Prefetch` Object:**
You can filter or order the prefetched relation using `django.db.models.Prefetch`:
```python
from django.db.models import Prefetch

items = Item.objects.select_related("seller").prefetch_related(
    Prefetch(
        "listings",
        queryset=MarketplaceListing.objects.filter(is_active=True).only("id", "item_id", "marketplace", "external_url"),
        to_attr="active_listings",
    )
)
```

### 3.2 Atomic Updates (`F()` Expressions) & Conditional Queries (`Q()` Objects)
Never increment counters in Python memory (`item.views += 1; item.save()`), which suffers from **lost-update race conditions**:
```python
from django.db.models import F, Q

# Compiles to atomic SQL: UPDATE items SET retry_count = retry_count + 1 WHERE id = 42;
Item.objects.filter(id=42).update(retry_count=F("retry_count") + 1)

# Complex OR / NOT filtering with Q objects:
stale_items = Item.objects.filter(
    Q(status="error") | (Q(status="syncing") & Q(updated_at__lt=ten_mins_ago))
)
```

### 3.3 Preventing Memory Bloating: `.only()`, `.values_list()`, and `.iterator()`
- **`QuerySet` Caching Gotcha:** `for item in Item.objects.all():` loads and caches **every row into a Python list in RAM**! For 100,000 rows, this crashes the worker with `MemoryError` (OOM).
- **The Fix:** Use `.iterator(chunk_size=2000)` so PostgreSQL streams rows in chunks without caching them in the `QuerySet`.
- Always pass `update_fields=["status", "updated_at"]` to `item.save(...)` so Django doesn't overwrite columns modified concurrently by another worker!

