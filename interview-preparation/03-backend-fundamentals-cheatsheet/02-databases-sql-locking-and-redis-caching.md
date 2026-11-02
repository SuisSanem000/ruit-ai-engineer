# Databases, SQL Locking & Redis Caching Internals

> **Luis's Cheat Sheet Topic:** *"orms and sql ... databases and cache"*

---

## 1. PostgreSQL Internals Every Senior Engineer Should Know

### 1.1 MVCC (Multi-Version Concurrency Control) & VACUUM
- **How MVCC works:** In PostgreSQL, **readers never block writers, and writers never block readers**. When you `UPDATE` a row in Postgres, it does *not* overwrite the bytes in place—it marks the old tuple with an `xmax` transaction ID and inserts a **brand-new physical row version (tuple)**!
- **Why this matters for high-churn tables (like `marketplace_sync_status`):**
  - Every `UPDATE` leaves behind a **dead tuple** (`bloat`) and updates **every index** on the table (unless it qualifies for a **HOT — Heap-Only Tuple** update where no indexed column changed!).
  - **Autovacuum** must periodically clean up dead tuples so the space can be reused and to prevent Transaction ID (`XID`) wraparound.
  - **Django Pro Tip:** Always pass `item.save(update_fields=["last_synced_at"])` instead of bare `item.save()`. Bare `item.save()` updates **every column** in the `UPDATE` statement, defeating Postgres HOT updates and causing unnecessary index bloat!

### 1.2 Indexing Strategies in PostgreSQL
| Index Type | When to Use at Ruit | Example |
| :--- | :--- | :--- |
| **B-Tree (Default)** | Equality (`=`) and range (`<`, `>`, `BETWEEN`, `ORDER BY`) queries on high-cardinality columns. | `(seller_id, status, updated_at DESC)` |
| **Composite Index Column Order** | **Left-most prefix rule:** Put equality columns first (`seller_id`, `status`) and range/sort columns second (`created_at`). An index on `(A, B)` speeds up `WHERE A = 1` and `WHERE A = 1 AND B = 2`, but rarely `WHERE B = 2` alone! | `Index(fields=["seller", "status", "-updated_at"])` |
| **Partial Index (`WHERE` clause)** | When 90% of rows are historical (`status = 'sold'` or `'archived'`) and queries almost always filter for active rows (`status = 'active'`). Makes the index 10x smaller and faster in RAM! | `Index(fields=["seller"], name="idx_active_items", condition=Q(status="active"))` |
| **GIN Index (Generalized Inverted Index)** | Indexing inside **`JSONB`** columns (e.g., marketplace-specific raw attributes like `{"brand_id": 42, "size": "M"}`) or full-text search arrays. | `GinIndex(fields=["marketplace_attributes"])` |

---

## 2. Concurrency Control: Pessimistic vs Optimistic Locking

**The Core Ruit Problem:** A vintage leather jacket is listed on **Vinted**, **Wallapop**, and **eBay** with `quantity = 1`. At `14:00:00.100`, a buyer purchases it on Vinted (webhook arrives at Worker 1). At `14:00:00.120`, a periodic sync or a second buyer event arrives from Wallapop at Worker 2. How do we guarantee atomic state transitions and prevent race conditions?

### Approach A: Pessimistic Locking (`SELECT ... FOR UPDATE`)
Locks the row in PostgreSQL at the moment it is read until `transaction.atomic()` commits:
```python
from django.db import transaction

def process_sale_webhook(item_id: int, marketplace: str) -> bool:
    with transaction.atomic():
        # skip_locked=True or nowait=True prevents workers from piling up on lock waits
        item = (
            Item.objects.select_for_update(nowait=True)
            .filter(id=item_id)
            .first()
        )
        if not item or item.status != "active":
            return False  # Already sold!
        item.status = "sold"
        item.save(update_fields=["status"])
        return True
```
- **`nowait=True`:** Immediately raises `DatabaseError` if another transaction holds the lock (great for rejecting duplicate concurrent webhook deliveries).
- **`skip_locked=True`:** Skips locked rows and grabs the next available unlocked row (the gold-standard SQL pattern for building a concurrent job polling queue in Postgres!).

### Approach B: Optimistic Locking (Atomic Conditional `UPDATE` + `version` Column)
No row lock is held during reads. Instead, the `UPDATE` statement itself checks the expected state/version atomically:
```python
# Single atomic SQL statement:
# UPDATE items SET status = 'sold', version = version + 1
# WHERE id = 123 AND status = 'active' AND version = 7;
rows_updated = Item.objects.filter(
    id=item_id,
    status="active",
    version=current_version,
).update(
    status="sold",
    version=F("version") + 1,
)
if rows_updated == 0:
    # Another worker beat us to it!
    return False
```
> **When to prefer Optimistic vs Pessimistic:** Optimistic locking (atomic conditional `UPDATE`) holds the row lock for the shortest possible duration (microseconds during the single `UPDATE` statement) and never deadlocks across multiple rows. Use `SELECT ... FOR UPDATE` when you must read complex state, compute business logic in Python, and write multiple related tables atomically.

---

## 3. Connection Pooling (`PgBouncer` & Django `CONN_MAX_AGE`)

- **Why Postgres Connections Are Expensive:** Unlike MySQL (threads), PostgreSQL spawns a **separate OS process (`postgres` backend)** per connection (~5–10 MB RAM each). Opening a new TCP + TLS + Postgres auth connection on every Django request adds 15–50ms of latency, and 200 Celery workers will exhaust `max_connections`!
- **Two-Layer Solution:**
  1. **Django `CONN_MAX_AGE = 600` (or `Django 5.1+` native `OPTIONS: {"pool": True}`):** Reuses persistent DB connections across requests in each worker.
  2. **`PgBouncer` in `transaction` pooling mode:** Multiplexes thousands of application/Celery worker connections onto a small pool of ~50–100 real PostgreSQL server connections (assigning a server connection only for the duration of a single SQL transaction).

---

## 4. Redis Caching Patterns & Distributed Primitives

1. **Cache-Aside Pattern:** Application checks Redis (`GET item:123`) $\rightarrow$ on miss, queries Postgres $\rightarrow$ populates Redis (`SET item:123 ... EX 300`).
   - **Why `DELETE` on write beats `SET` on write:** When an item is updated in Postgres, **invalidate (`DEL item:123`)** the cache inside `transaction.on_commit()` rather than overwriting it directly—otherwise two concurrent writers can finish their DB updates in order `A -> B` and their Redis `SET`s in order `B -> A`, leaving stale data `A` in Redis forever!
2. **Preventing Cache Stampede (Thundering Herd) & Avalanche:**
   - **Avalanche (10,000 keys expire at the exact same second):** Always add **random TTL jitter** (`ttl = 300 + random.randint(0, 60)`).
   - **Stampede (1 hot key expires and 500 concurrent requests all miss and hammer Postgres):** Use a short Redis mutex lock (`SET lock:recompute:key 1 NX EX 5`) so only 1 worker queries Postgres while others wait briefly or serve slightly stale data (stale-while-revalidate).
3. **Redis Distributed Rate Limiting (Token Bucket / Sliding Window):**
   - When Ruit must cap calls to Vinted's API at e.g. `60 requests/minute per seller IP/proxy`, use an **atomic Redis Lua script** (or `INCR` + `EXPIRE` / Sorted Set `ZREMRANGEBYSCORE` + `ZCARD` + `ZADD`) so all Celery workers share a single global rate-limit counter with zero race conditions.

