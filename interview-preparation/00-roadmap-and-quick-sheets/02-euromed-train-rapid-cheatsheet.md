# 02 — Train Ride Rapid Cheat Sheet (Barcelona to Valencia)

> **Quick 10-Minute Read:** Key definitions and answers matching Luis's email cheat sheet for Friday morning on the Euromed.

---

## 1. Python, Django & Concurrency

- **The GIL (Global Interpreter Lock):** A mutex in CPython that lets only one thread execute Python bytecode at a time. Network/IO calls release the GIL (so `asyncio` handles thousands of connections), but heavy CPU tasks require multiple processes (`multiprocessing` / Celery).
- **Async Django (WSGI vs ASGI):** WSGI is synchronous (1 request per thread). ASGI runs an async event loop supporting `async def` views and WebSockets. Never run blocking sync queries in async views (raises `SynchronousOnlyOperation`); use `sync_to_async` or async ORM (`aget`, `acount`).
- **ORM N+1 Queries:** Use `select_related` (SQL `JOIN` for 1-to-1 and ForeignKey) and `prefetch_related` (separate query with `IN (...)` for M2M and reverse relationships).
- **Generators (`yield`):** Produces values lazily one at a time. Keeps RAM flat when streaming millions of rows or large files. Django's `.iterator(chunk_size=2000)` streams rows in chunks.
- **Pydantic & Types:** Enforces runtime schema validation on untrusted marketplace JSON, strips whitespace, converts string prices (`"19,50 €"` $\rightarrow$ `19.50`), and detects unexpected fields.

---

## 2. Backend, Queues, Databases & Error Handling

- **Double-Sell Prevention:** Lock the row in PostgreSQL using `SELECT ... FOR UPDATE` inside `transaction.atomic()`. A concurrent sale event waits on the lock, sees `quantity = 0`, and rejects the duplicate order.
- **Background Queues (Celery + Redis):** Offload slow marketplace calls. Use separate queues by priority (`delist_urgent` vs `bulk_catalog`), `acks_late=True` so failed workers do not lose jobs, and exponential backoff with jitter on retries.
- **Idempotency Keys:** Unique UUID per task/request. If a network call times out and retries, the server/marketplace recognizes the key and does not perform the action twice.
- **Error Handling Philosophy:**
  - **Python:** `try/except` (easy to write, but exceptions can be implicit).
  - **Go:** Explicit return values `val, err := fn()` (clear, lots of boilerplate).
  - **Rust:** `Result<T, E>` and `Option<T>` (compiler forces explicit handling of all cases).
  - *In Ruit Integrations:* Classify errors into **Retryable** (`429`, `503`, timeout), **Auth Expired** (`401` — notify seller to re-login), and **Schema Drift** (log diff, alert engineers).

---

## 3. Networking, Reverse Engineering, Browsers & DevOps

- **TCP 3-Way Handshake:** `SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`. Reliable, ordered, adds 1 RTT. Closed sockets stay in `TIME_WAIT` for 60s; always use connection pooling (`httpx.AsyncClient`) to avoid port exhaustion and repeated DNS lookups.
- **Protocols Comparison:**
  - **HTTP/1.1:** 1 request at a time per TCP connection.
  - **HTTP/2:** Multiplexes many streams over 1 TCP connection, binary framing, `HPACK`. (TCP head-of-line blocking if packet drops).
  - **HTTP/3 (QUIC):** Over UDP. Independent streams, no TCP head-of-line blocking.
  - **WebSockets:** Full-duplex bidirectional TCP stream after `101 Switching Protocols` handshake. Scaled across Django servers using **Redis Pub/Sub**; needs ping/pong heartbeats.
  - **Server-Sent Events (SSE):** Lightweight 1-way text stream (`text/event-stream`) over HTTP, auto-reconnects.
  - **Webhooks:** Server-to-server HTTP POST; requires HMAC signature check and immediate 200 response.
- **TLS Fingerprinting (JA3 / JA4):** Anti-bot systems (Cloudflare, DataDome) inspect the cipher suites in `TLS ClientHello`. Python's `OpenSSL` signature gets blocked; use **`curl_cffi`** to impersonate real Chrome BoringSSL.
- **Reverse Engineering:** Capture browser traffic via Chrome DevTools (`.har`) or mobile traffic via `mitmproxy`. (Mobile APIs break less frequently).
- **Chrome Extension (MV3):** Runs in seller's browser using residential IP, cookies, and fingerprint—bypasses bot blocks for free.
- **DevOps & Observability:** Graceful shutdown with `SIGTERM` in Docker, expand-and-contract zero-downtime DB migrations, and metrics (Prometheus/Grafana), logs (`structlog`), and traces (OpenTelemetry/Sentry).
