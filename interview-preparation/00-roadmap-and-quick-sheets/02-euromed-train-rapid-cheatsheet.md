# Euromed Train Rapid Cheat Sheet (15-Minute Review)

> Read this on the train to Valencia on Friday morning. Every bullet below matches a topic from Luis's email cheat sheet.

---

## 1. Python & Django Knowledge

- **The GIL (Global Interpreter Lock):**
  - A lock inside standard Python (CPython) that lets only **one thread run Python code at a time** per process.
  - It exists because Python manages memory by counting references to objects, and that counter is not thread-safe without a lock.
  - **I/O tasks (network calls, DB queries):** Python **releases the GIL** while waiting for the network, so `asyncio` or threads work great for API integrations.
  - **CPU tasks (heavy math, image resizing):** Keep holding the GIL, so threads do not speed them up. Use **multiple processes (`multiprocessing` or multiple Celery workers)** so each process gets its own GIL.
- **Async in Django:**
  - **WSGI (`Gunicorn`):** Classic synchronous Django (1 request blocks 1 thread).
  - **ASGI (`Uvicorn`):** Async Django (1 worker handles many concurrent `async def` views and WebSockets).
  - **Main rule:** Never run slow synchronous code (like `requests.get` or sync ORM) directly inside an `async def` view, or you will freeze the whole event loop.
  - **Bridges:** Use `sync_to_async` to call sync code from async code, and `async_to_sync` to call async code from sync code.
  - **ORM Caveats:** Django has async methods like `aget()`, **but** `transaction.atomic()` is still synchronous, and accessing an un-loaded `ForeignKey` inside an `async def` view crashes with `SynchronousOnlyOperation` unless you pre-load it with `select_related()`.
- **Generators (`yield`):**
  - A function with `yield` does not return a full list in memory at once.
  - Instead, it pauses at `yield`, gives you **one item at a time**, and remembers where it stopped.
  - **Why use it:** Processing 100,000 marketplace items or a huge JSON file uses almost zero RAM instead of crashing the server with Out-Of-Memory.
- **Robust Python (Type Hints & Static Analysis):**
  - Python is dynamically typed, so bugs can hide until runtime.
  - We make it safe by adding **type hints** (`str`, `int`, `list[str]`), checking types before deploy with **`mypy`** and **`ruff`**, and validating external JSON at runtime with **Pydantic**.

---

## 2. Backend & Integration Fundamentals

- **Concurrency & Async:**
  - **Concurrency:** Handling many network tasks at the same time on 1 CPU core by switching while waiting for I/O (`asyncio`).
  - **Parallelism:** Running heavy CPU tasks at the exact same moment across multiple CPU cores (`multiprocessing`).
  - Prevent race conditions across workers using **database row locks** or **Redis locks**.
- **JSON Validation:**
  - Never trust JSON from external marketplaces because they change fields without warning.
  - Validate every API response with **Pydantic** (like AJV/Zod in JS) and log unknown or missing fields so we know when a marketplace changed its API.
- **ORMs & SQL:**
  - **N+1 Query Problem:** Fetching 50 items and then running 50 separate queries to get each item's seller.
  - **Fix in Django:** Use **`select_related`** (uses a single SQL `JOIN` for single foreign keys) and **`prefetch_related`** (runs a 2nd query with `WHERE id IN (...)` and joins in Python for `Many-to-Many` or `1-to-Many` lists).
  - **Preventing Double-Sells:** Lock the item row in Postgres using `SELECT ... FOR UPDATE` inside a transaction (or use an atomic `UPDATE ... WHERE status = 'active'`).
- **Background Queues & Brokers (Celery & Redis):**
  - **How it works:** Django puts a small job message (just the `item_id`) into **Redis** or **RabbitMQ**, and **Celery worker processes** pick it up in the background.
  - **Best practices:**
    - Queue jobs only **after** the DB transaction commits (`transaction.on_commit`).
    - Use **separate queues** (`critical_delist` vs `slow_bulk_sync`) so slow jobs never block urgent delisting.
    - Enable **`acks_late=True`** (only remove job from queue after it finishes), **idempotency keys** (so running a job twice does not create 2 listings), **exponential backoff with jitter**, and a **Dead Letter Queue (DLQ)**.
- **HTTP Clients & TLS:**
  - Always reuse a **connection pool (`Session` / `AsyncClient`)** so you do not repeat slow TCP + TLS handshakes on every request.
  - Always set explicit **connect and read timeouts**.
  - **TLS Fingerprinting (JA3/JA4):** Anti-bot systems like Cloudflare check the TLS `ClientHello` handshake and HTTP/2 settings. Standard Python `requests`/`httpx` has a Python OpenSSL fingerprint and gets blocked (`403`). Tools like **`curl_cffi`** copy Chrome's exact TLS fingerprint.
- **Error Handling (Python vs Go vs Rust):**
  - **Python:** Uses **exceptions (`try / except`)**. Clean to read, but you cannot see which errors a function might throw just by looking at its signature.
  - **Go:** Returns **errors as values (`result, err`)**. Forces you to check `if err != nil` right away, but creates repetitive code.
  - **Rust:** Uses **`Result<T, E>` and `Option<T>` types**. The compiler forces you to handle both success and error cases before code can compile.
  - **In Python integrations:** Group errors clearly into **Retryable** (`429`, `503`, timeout), **Auth Expired** (`401`—refresh seller token), and **Broken Contract** (JSON schema changed—stop and alert engineers).
- **Databases & Cache:**
  - **PostgreSQL:** Uses MVCC (reads don't block writes) and needs **PgBouncer** to pool database connections when running many workers.
  - **Redis:** Used for caching, rate limiting, and short locks. Add **random jitter to TTLs** so 1,000 cached items do not expire at the exact same second (cache stampede).
- **Low-Level Networking & Protocols:**
  - **HTTP/1.1:** One request at a time per TCP connection.
  - **HTTP/2:** Sends many requests at once (multiplexing) over 1 TCP connection, but if 1 TCP packet drops, all streams wait.
  - **HTTP/3 (QUIC):** Runs over **UDP** with built-in TLS 1.3; if 1 packet drops, only that single stream waits.
  - **WebSockets:** Upgrades an HTTP connection into a two-way real-time pipe. Needs **ping/pong heartbeats** to detect dead connections and **Redis Pub/Sub** to scale across multiple servers.
- **API Integrations & Reverse Engineering:**
  - Capture web traffic in **Chrome DevTools (`.har` files)** and mobile app traffic with **`mitmproxy` / Proxyman** (using Frida on a test device if the app uses SSL certificate pinning).
  - Find the login/refresh token flow, required headers, and CSRF/signature rules.
  - Catch breakages **before sellers notice** by running scheduled test jobs (canary probes) every 15 minutes and alerting on Pydantic validation errors.
- **Browsers, Automations & Chrome Extensions:**
  - **Playwright:** Controls Chrome via WebSocket (CDP). Block images/fonts to save proxy data, or use the browser just to get anti-bot cookies and run fast API calls.
  - **Chrome Extensions (Manifest V3):** Has a **Background Service Worker** (wakes up on events/alarms, no DOM access) and **Content Scripts** (can read/click the webpage DOM). Great for Ruit because requests come from the seller's **real home IP and logged-in browser**.
- **DevOps & Zero-Downtime Deployments:**
  - Handle Linux **`SIGTERM`** so Gunicorn and Celery finish their current task before shutting down.
  - **Zero-Downtime DB Migrations (Expand & Contract):** Never rename or delete a DB column in one step while old containers are still running. First add the new nullable column, write to both, backfill old rows, switch reads, and delete the old column later.
- **Observability & Scaling:**
  - **Metrics (Prometheus/Grafana):** Request rate, error rate (especially `403`/`429`), latency, and Celery queue length.
  - **Logs:** Structured JSON logs with a shared `correlation_id` and `seller_id`.
  - **Traces (OpenTelemetry/Sentry):** Track a request from Django $\rightarrow$ Redis $\rightarrow$ Celery $\rightarrow$ Marketplace API.
- **Working with AI:**
  - Keep a state file (`ai-state.md`), use reusable **Skills** and **Rules**, run **parallel sessions** (one agent researching API payloads, one writing code, one writing `pytest` tests), and always verify with tests.
