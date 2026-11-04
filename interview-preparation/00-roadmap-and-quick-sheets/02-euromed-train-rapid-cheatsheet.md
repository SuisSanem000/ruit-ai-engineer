# Train Ride Rapid Cheat Sheet (Barcelona to Valencia)

> Read this 15-minute summary on the Euromed train on Friday morning. Every bullet matches Luis's email cheat sheet.

---

## 1. Python & Django Questions

- **The GIL (Global Interpreter Lock):**
  - A lock in standard Python (CPython) that lets only **one thread run Python code at a time** per process.
  - It exists because Python manages memory by counting references to objects, and that counter is not thread-safe without a lock.
  - **Network/disk I/O (`async` or threads):** Releases the GIL while waiting for the network, so Python handles thousands of API calls easily.
  - **Heavy CPU work:** Holds the GIL, so threads do not speed it up. Use **multiple processes (`multiprocessing` or Celery workers)** so each process gets its own GIL and CPU core.
- **Async in Django:**
  - **WSGI** runs synchronous views; **ASGI** runs `async def` views and WebSockets.
  - **Main Rule:** Never call slow synchronous code (like `time.sleep`, `requests.get`, or normal Django ORM queries) directly inside an `async def` view, or it freezes the whole event loop.
  - Use **`sync_to_async`** to run sync code in a background thread, or use Django's async ORM methods (`aget`, `aiterator`).
  - **Gotcha:** Database transactions (`transaction.atomic()`) are still synchronous—put the transaction inside a normal sync function and call it with `sync_to_async`.
- **Generators (`yield`):**
  - Functions that use `yield` instead of `return` to produce items **one by one on demand**, instead of building a giant list in RAM.
  - When syncing 100,000 items or reading a huge JSON file, generators keep memory usage tiny and flat.
  - In Django ORM, `.iterator(chunk_size=2000)` streams database rows in chunks instead of loading the whole table into memory.
- **Robust Python (Types & Static Analysis):**
  - Add **type hints** to function inputs and outputs so humans and AI agents know the exact data types.
  - Use **`mypy` or `pyright`** to check types before deploying, **`ruff`** for fast linting, and **`Pydantic`** to validate untrusted JSON from marketplaces at runtime.

---

## 2. Backend & Integration Fundamentals

- **Concurrency vs Async:**
  - **Concurrency:** Managing many tasks at the same time (like waiting on 50 API calls using an `async` event loop).
  - **Parallelism:** Running computations at the exact same instant on multiple CPU cores (using multiple processes).
  - Always limit how many async requests run at once using a **Semaphore** so you do not get rate-limited or run out of connections.
- **JSON Validation:**
  - Marketplace APIs often return messy data (like prices as strings `"15,50 €"`) or change fields without warning.
  - Validate every external response with **Pydantic** (like you did with AJV at QueryLaw), clean the values, and log a warning if unexpected new fields appear.
- **ORMs & SQL:**
  - **N+1 Problem:** Fetching 100 items and then running 100 extra queries in a loop to get each item's seller.
  - **Fix:** Use `select_related` (uses a SQL `JOIN` for single foreign keys) and `prefetch_related` (runs 1 extra query with `WHERE id IN (...)` for many-to-many or reverse lists).
  - **Preventing Double-Sells:** Lock the item row in PostgreSQL (`SELECT ... FOR UPDATE`) or use an atomic `UPDATE ... WHERE status = 'active' AND quantity >= 1` so two buyers cannot buy the same item at once.
- **Background Queues (Celery & Redis):**
  - Run slow marketplace calls in background Celery workers, never inside the user's HTTP request.
  - Use **separate queues by priority**: a fast queue for urgent tasks (`delist sold item` in seconds) and slower queues for bulk catalog imports.
  - Turn on **late acknowledgment (`acks_late=True`)** so tasks are not lost if a worker crashes, use **idempotency keys** so retrying a task never posts duplicate items, and use **exponential backoff + random jitter** on retries.
- **HTTP Clients & TLS Fingerprinting:**
  - Reuse a client session (`httpx.AsyncClient` or `requests.Session`) to keep TCP/TLS connections open (connection pooling) and always set timeouts.
  - **Anti-Bot TLS Fingerprinting (JA3/JA4):** Cloudflare and DataDome look at the TLS handshake (`ClientHello` cipher list) and HTTP/2 settings. Normal Python `requests`/`httpx` uses OpenSSL, which looks different from Chrome's BoringSSL and gets blocked (`403`). Use **`curl_cffi`** to mimic Chrome's exact TLS fingerprint.
- **Error Handling (Python vs Go vs Rust):**
  - **Python:** Uses `try / except` exceptions. Easy to read, but you cannot see which errors a function might throw just by looking at its name.
  - **Go:** Returns errors as normal values (`val, err := fn()`). Very clear and local, but requires lots of `if err != nil` checks.
  - **Rust:** Uses `Result<T, E>` and `Option<T>`. The compiler forces you to handle both success and error cases before the code can even compile.
  - **Best Practice in Python Integrations:** Group errors clearly into **Retryable** (`429`, `503`, timeout), **Auth Expired** (`401` — refresh token or ask seller to log in), and **Broken Contract** (JSON validation failed — stop and alert engineers).
- **Databases & Cache:**
  - **Postgres:** Use indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY` (and `GIN` indexes for `JSONB`). Use **PgBouncer** to pool database connections across many Celery workers.
  - **Redis:** Use for caching, distributed locks, and rate limiting. Add random **jitter** to cache expiration times (TTL) so thousands of cached keys do not expire at the exact same second (cache stampede).
- **Networking & Protocols (HTTP/1.1, HTTP/2, HTTP/3, WebSockets):**
  - **HTTP/1.1:** One request at a time per TCP connection.
  - **HTTP/2:** Sends many streams at once over a single TCP connection, but if 1 TCP packet drops, all streams wait (TCP head-of-line blocking).
  - **HTTP/3 (QUIC):** Runs over **UDP** instead of TCP, so a dropped packet only affects one single stream.
  - **WebSockets:** Upgrades an HTTP request into a two-way live connection. Scale across multiple servers using **Redis Pub/Sub** and use ping/pong heartbeats to close dead connections.
- **API Integrations & Reverse Engineering:**
  - Capture web traffic with **Chrome DevTools (`.har` files)** and mobile app traffic with **`mitmproxy`** (mobile APIs break less often because old app versions must keep working).
  - Lock token refreshes in **Redis** so 5 workers do not refresh the same token at the same time and invalidate the seller's login.
  - Run automated test checks (canaries) every 15 minutes to catch marketplace changes before sellers notice.
- **Browsers, Automations & Chrome Extensions:**
  - **Playwright:** Controls headless Chrome over WebSocket (CDP). Block images and fonts to save proxy bandwidth, and reuse browser contexts.
  - **Chrome Extensions (Manifest V3):** Runs inside the seller's own Chrome browser (`Content Scripts` read the page DOM; `Background Service Worker` talks to Ruit's server and reads cookies). Great because it uses the seller's real home IP, real browser fingerprint, and active login session.
- **DevOps & Zero-Downtime Deployments:**
  - Handle Linux **`SIGTERM`** signals properly so Celery workers finish their current task before shutting down during a deploy.
  - **Zero-Downtime DB Migrations (Expand and Contract):** Never rename or delete a database column in one step while old code is still running. First add the new column as nullable, deploy code that writes to both, copy old data in batches, and remove the old column in a later deploy.
- **Observability & Scaling:**
  - **Metrics (Prometheus/Grafana):** Track request count, error rate (`401`, `403`, `429`, `5xx`), latency, and Celery queue length per marketplace.
  - **Logs (`structlog`):** Structured JSON logs with `correlation_id`, `seller_id`, and `marketplace`.
  - **Traces (OpenTelemetry) & Sentry:** Follow a request from the Django view into the Celery worker and external API call.

---

## 3. Working with AI (How You Work Daily — Deep Dive in `01-ai-workflow-and-live-task/`)

- **Harness Engineering Philosophy:** AI is a fast engine, but you wrap it in a strict harness (context files, schemas, automated tests, linters, and review loops) so its output is always safe and reliable.
- **Real Resume Experience (No RAG/Fine-Tuning/Deploy Claims):** At QueryLaw, you built a strict validation pipeline using prompt engineering, JSON Schema / AJV checks, and automated retry loops (95%+ accuracy). At Parsaiane, you crawled 150+ news sites and used OpenAI to summarize.
- **My Tool Stack:** Antigravity IDE (agent, inline `Cmd+I`, skills, subagents), Claude Code in VS Code & CLI connected via OpenRouter API token (`CLAUDE.md`, Plan Mode, `/compact`, custom commands), and GitHub Copilot Code Review on Git diffs and PRs.
- **Skills vs Rules vs Plugins:** Rules are always on; Skills (`SKILL.md`) load on demand for specific playbooks; Plugins package skills, rules, and MCP tools together.
- **Parallel Sessions:** Run Session 1 on code and Session 2 on tests/fixtures, or use read-only research subagents for large payloads, and `git worktree` for separate features. Never let two agents edit the same file.
