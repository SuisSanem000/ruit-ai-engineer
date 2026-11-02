# Euromed Train 15-Minute Rapid Flash Sheet (Barcelona $\rightarrow$ Valencia)

> **Purpose:** Read this on the Euromed train on Friday morning (Nov 6) before arriving at Lanzadera at `12:45h`.  
> Every bullet below corresponds **1:1** to Luis Grau's literal evaluation cheat sheet from his email.

---

## Part 1: Python & Django Deep Dive

### 1. The GIL (Global Interpreter Lock)
- **What it is:** A mutex in CPython that allows only **one native OS thread to execute Python bytecodes at a time** per process, because CPython's memory management (`PyObject` reference counting) is not thread-safe without locks.
- **I/O-Bound vs CPU-Bound:**
  - **I/O-bound** operations (network sockets, HTTP calls, DB queries, disk reads) **release the GIL** while waiting on the OS kernel. Thus, `asyncio` (single-threaded cooperative multitasking) or thread pools scale well for I/O.
  - **CPU-bound** operations (heavy JSON/HTML parsing, image resizing, cryptography) hold the GIL. Threads will contend and run slower than 1 thread; use **`multiprocessing` (`ProcessPoolExecutor`)**, native C/Rust extensions (`pydantic-core`, `orjson`, `lxml`), or offload to Celery workers.
- **Modern Update (PEP 703):** Python 3.13/3.14 introduced experimental **free-threaded CPython (`python3.13t`, `--disable-gil`)** using biased reference counting and per-object locks.

### 2. Async in Django
- **WSGI vs ASGI:** WSGI (`Gunicorn`) is synchronous (1 request = 1 thread/worker blocking). ASGI (`Uvicorn`/`Daphne`) is asynchronous, supporting `async def` views, long-lived WebSockets, and Server-Sent Events (SSE).
- **The Golden Rule of Django Async:** Never call synchronous blocking code (sync ORM, `requests.get`, `time.sleep`) directly inside an `async def` view—it blocks the entire event loop thread for all concurrent users!
- **Bridges (`asgiref.sync`):**
  - `await sync_to_async(sync_fn, thread_sensitive=True)()` $\rightarrow$ runs blocking code in a thread pool.
  - `async_to_sync(async_fn)()` $\rightarrow$ runs a coroutine from synchronous code (e.g., inside a sync Celery worker).
- **Django ORM Async Caveats:** Django 4.1+/5.x added `aget()`, `acount()`, `aiterator()`, `acreate()` (mostly wrappers around `sync_to_async` under the hood), **but**:
  1. **`transaction.atomic()` does NOT work with `async def` directly**—wrap the entire atomic transactional unit in a sync function and call it via `await sync_to_async(run_tx)()`.
  2. Accessing an un-fetched `ForeignKey` attribute (`item.seller.name`) in an async context triggers a `SynchronousOnlyOperation` exception unless pre-loaded via `select_related('seller')`!

### 3. Generators & Iterators
- **How they work:** Any function with `yield` returns a **generator object** implementing the Iterator Protocol (`__iter__` and `__next__`). Execution pauses at `yield`, preserving local stack frame state in heap memory, and resumes on the next `next()` call until `StopIteration`.
- **Why they matter for Ruit:**
  - **Constant Memory ($O(1)$ RAM):** Streaming 500,000 marketplace listings or multi-GB JSON feeds one chunk at a time without loading everything into memory (`OutOfMemory` kill).
  - **Django ORM `.iterator(chunk_size=2000)`:** Streams rows using server-side cursors in Postgres without caching all model instances in the `QuerySet` cache.
  - **Sub-generators & Async Generators:** `yield from` delegates to sub-generators cleanly; `async def` + `yield` creates an `AsyncGenerator` consumed with `async for` (ideal for paginated async API scraping!).

### 4. Robust Python (Type Hints, Pydantic v2, Static Analysis)
- **Type Hints (`typing`):** `TypedDict` (typed dicts), `Protocol` (structural duck-typing / interfaces), `Generic[T]`, `Literal["vinted", "wallapop"]`, `Annotated[int, Field(gt=0)]`, `Union` (`X | Y`).
- **Runtime Boundary Validation (`Pydantic v2`):** Type hints alone are ignored at runtime. At external boundaries (marketplace API responses, webhooks, LLM outputs), use **Pydantic v2** (powered by Rust `pydantic-core`) to parse, coerce, and validate data into typed `BaseModel` objects.
- **Static Analysis Pipeline:** **`Ruff`** (Rust linter/formatter) + **`mypy --strict` / `pyright`** in CI/CD and pre-commit hooks.

---

## Part 2: Core Backend & Integration Fundamentals (Luis's Cheat Sheet)

| Topic | The 30-Second Senior Answer for Luis |
| :--- | :--- |
| **Concurrency & Async** | Concurrency = dealing with many tasks at once (overlapping I/O wait times via `asyncio` event loop); Parallelism = executing many tasks simultaneously on multiple CPU cores (`multiprocessing`). Protect shared state across workers using **idempotency keys** and **distributed locks (Redis / Postgres row locks)**. |
| **JSON Validation** | Third-party marketplace payloads are untrusted and change silently. Use **two-tier validation**: (1) strict **Pydantic v2** models for required business fields (`ConfigDict(extra='allow')` or `'ignore'`), plus (2) **schema-drift telemetry** that logs unexpected/missing optional fields to alert engineers before an integration breaks. |
| **ORMs & SQL** | Fix **N+1** with `select_related` (SQL `JOIN` for FK/1:1) and `prefetch_related` (separate `WHERE id IN (...)` query for M2M/reverse FKs). Prevent double-sells with `SELECT ... FOR UPDATE NOWAIT` inside `transaction.atomic()` + `transaction.on_commit()` before firing Celery tasks. Index foreign keys, status filters (partial index `WHERE status = 'active'`), and JSONB (`GIN` index). |
| **Background Queues (Celery & Redis)** | Separate queues by priority & latency: `high_priority_delist` (when an item sells—must run in seconds!) vs `bulk_catalog_sync` vs `browser_automation`. Always set `acks_late=True`, `reject_on_worker_lost=True`, **idempotency keys**, exponential backoff with **random jitter** (prevents thundering herd), and a **Dead Letter Queue (DLQ)** for poison messages. |
| **HTTP Clients & TLS** | Reuse `httpx.AsyncClient` connection pools with explicit `connect`, `read`, and `pool` timeouts. Standard Python `httpx`/`requests` uses OpenSSL whose **TLS ClientHello (JA3/JA4 fingerprint)** and **HTTP/2 SETTINGS frame** scream "Python bot" to Cloudflare/DataDome. Use **`curl_cffi`** (impersonating Chrome's BoringSSL & HTTP/2 fingerprint) + residential proxies when calling protected marketplace endpoints. |
| **Error Handling (Python vs Go vs Rust)** | **Python:** Exceptions (`try/except`, EAFP)—ergonomic happy path, but failure modes aren't visible in function signatures. **Go:** Explicit `val, err` return values—forces local handling, verbose boilerplate. **Rust:** Algebraic `Result<T, E>` & `Option<T>` with `?` operator—compile-time exhaustive safety. **In Python integrations:** Combine custom domain exception hierarchies (`RetryableError` vs `PermanentIntegrationError` vs `AuthExpiredError` vs `SchemaBreakageError`) or lightweight `Result` types at connector boundaries. |
| **Databases & Cache** | **PostgreSQL:** MVCC (readers don't block writers), watch out for dead tuples (`autovacuum`), and always put **PgBouncer** in front of Postgres when scaling Celery/ASGI workers. **Redis:** Use for Cache-Aside, token-bucket rate limiting (Lua scripts / Sorted Sets), and distributed locks. Add **TTL jitter** and lock-based recomputation to prevent **cache stampedes**. |
| **Low-Level Networking & Protocols** | **HTTP/1.1:** Head-of-line blocking per TCP connection. **HTTP/2:** Multiplexed streams over 1 TCP connection + HPACK binary headers (still has TCP-level head-of-line blocking on packet loss). **HTTP/3 (QUIC):** Runs over **UDP**, built-in TLS 1.3, independent stream recovery (zero head-of-line blocking). **WebSockets:** HTTP `101 Switching Protocols` upgrade $\rightarrow$ full-duplex TCP framing; scale horizontally with **Redis Pub/Sub** + heartbeat ping/pong. |
| **API Integrations & Reverse Engineering** | Inspect mobile/web traffic with **Chrome DevTools (`Copy as cURL`/HAR)** and **`mitmproxy` / Proxyman** (with mobile cert + Frida for SSL unpinning when needed). Reconstruct auth lifecycle (access token, refresh token rotation, CSRF, HMAC request signing, device headers). **Catch breakage early** via scheduled synthetic canary checks and Pydantic schema-drift alerts. |
| **Browsers & Chrome Extensions** | **Playwright (CDP):** Use persistent contexts, stealth patches, and block heavy fonts/media to save bandwidth. **Chrome Extensions (Manifest V3):** Content Scripts (DOM access) + Service Worker (background orchestration) + WebSocket/API link to Ruit cloud. **Superpower:** Executes requests using the seller's real browser TLS fingerprint, cookies, and residential IP! |
| **DevOps & Zero-Downtime** | **Docker:** Multi-stage builds, non-root user, healthchecks. **Zero-Downtime Deploys:** Rolling/Blue-Green + graceful `SIGTERM` handling (drain in-flight requests/Celery tasks) + **Expand-and-Contract DB migrations** (1. add nullable col, 2. dual-write, 3. backfill in batches, 4. enforce constraint with `NOT VALID` $\rightarrow$ `VALIDATE CONSTRAINT` to avoid table locks). |
| **Observability & Scaling** | **Metrics (Prometheus/Grafana):** Track per-marketplace RED metrics (Request rate, Error rate by HTTP status, Duration p95/p99) + Celery queue lag. **Logs (`structlog`):** JSON logs with `correlation_id`, `seller_id`, `marketplace`. **Traces (OpenTelemetry):** End-to-end spans across Django $\rightarrow$ Redis $\rightarrow$ Celery $\rightarrow$ Marketplace API. |

---

## Part 3: Your 3 Signature Stories to Weave In Naturally

1. **Dadroit JSON Generator (VS Code Extension — 630K+ installs, built in 3 days):** Shows product instinct, developer/user empathy, fast execution, and deep understanding of JSON schemas & browser/editor extension ecosystems.
2. **150+ Site News Crawler & Semantic Pipeline (Parsaiane — 60K+ DAU):** Directly mirrors Ruit's integration challenge—keeping 150 heterogeneous sources alive despite constant DOM/API changes, rate limits, and dirty data.
3. **QueryLaw Antifragile AI Engine (95%+ accuracy, Multi-Layer Validation & Brittle-Logic Telemetry):** Proves you know how to make non-deterministic LLMs and brittle external pipelines reliable in production using strict schema validation and real-time failure telemetry.
