# Databases, SQL Locking & Redis Caching

> **Code examples with detailed comments:** [test_concurrency_locks_and_errors.py](./fundamentals-labs/test_concurrency_locks_and_errors.py)

---

## 1. PostgreSQL Basics & Indexes

- **MVCC (How Postgres Handles Simultaneous Reads and Writes):**
  - In PostgreSQL, **readers never block writers, and writers never block readers**.
  - When you `UPDATE` a row, Postgres actually writes a new version of the row and marks the old one as dead (**dead tuple**), which `autovacuum` cleans up later.
  - Because updating a row updates all indexes if indexed columns change, always update **only the columns that changed** (`update_fields=["status"]`).
- **4 Types of SQL Indexes to Know:**
  - **B-Tree Index (Default):** Best for `=`, `<`, `>`, `BETWEEN`, and `ORDER BY` on normal columns (`seller_id`, `created_at`).
  - **Composite Index (Multi-Column):** Order matters! Put equality columns first (`seller_id`, `status`) and sorting/range columns last (`updated_at`).
  - **Partial Index (`WHERE` filter):** Indexes only active rows (e.g., `WHERE status = 'active'`). Since 90% of second-hand items eventually become `'sold'`, a partial index is 10x smaller and faster.
  - **GIN Index:** Used to index keys and values inside **`JSONB`** columns (great for storing custom marketplace attributes).

---

## 2. Stopping Double-Sells: Pessimistic vs Optimistic Locking

- **The Problem:** A vintage jacket (`quantity = 1`) is listed on Vinted and Wallapop. Two buyers click "Buy" at almost the exact same moment. How do we make sure only one sale succeeds and the other channel delists?
- **Option 1 — Pessimistic Locking (`SELECT ... FOR UPDATE`):**
  - Locks the item row in PostgreSQL when reading it inside a transaction (`select_for_update()`), so any other worker trying to touch that item must wait (or fail immediately with `nowait=True`).
  - Also supports `skip_locked=True`, which skips locked rows and grabs the next unlocked row (great for job queues).
- **Option 2 — Optimistic Locking (Atomic `UPDATE` with `version` or `quantity` check):**
  - Does not lock the row during reads.
  - Instead, runs a single atomic SQL update: *update status to sold and version = version + 1 ONLY IF status is still active and version matches what we read*.
  - If `0 rows` were updated, we know another worker already sold the item milliseconds earlier!

---

## 3. Database Connection Pooling (`PgBouncer`)

- Opening a new PostgreSQL connection is slow and uses ~5–10 MB of RAM per connection on the database server.
- If you have 100 Celery workers and 20 web workers, they can easily run out of Postgres `max_connections`.
- **Fix:** Reuse connections in Django (`CONN_MAX_AGE`) and put **PgBouncer** in front of PostgreSQL so hundreds of workers share a small pool of ~50 real database connections.

---

## 4. Redis Caching, Rate Limiting & Distributed Locks

- **Cache-Aside Pattern:**
  - Check Redis first $\rightarrow$ if missing, read from PostgreSQL $\rightarrow$ save result in Redis with a TTL (expiration time).
  - When updating data in PostgreSQL, **delete the Redis cache key** after the DB transaction commits instead of overwriting it (avoids race conditions where two writers overwrite Redis in the wrong order).
- **Stopping Cache Stampedes:**
  - **Random Jitter on TTL:** Add a random 0–60 seconds to expiration times so 10,000 cached items do not expire at the exact same second.
  - **Recompute Lock:** When a popular cache key expires, let only 1 worker query PostgreSQL while other requests wait briefly.
- **Distributed Locks & Rate Limits in Redis:**
  - **Locks (`SET key value NX EX 10`):** Ensures only 1 Celery worker refreshes a seller's expired login token or syncs the same listing at a time.
  - **Rate Limiting (Token Bucket):** Stores per-marketplace request counters in Redis so all Celery workers respect Vinted or eBay rate limits together.
