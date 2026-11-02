# DevOps, Zero-Downtime Deployments, Observability & Scaling

> **Luis's Cheat Sheet Topic:** *"devops (linux, docker and docker compose, deployment strategies, zero downtime strategies), observability (metrics, logs, traces), scaling, etc."*

---

## 1. Linux & Container Fundamentals for Backend Engineers

### 1.1 Linux Process Signals & Graceful Shutdown (`SIGTERM` vs `SIGKILL`)
When deploying a new version of Ruit via Docker / Kubernetes / Kamal, the orchestrator stops old containers by sending **`SIGTERM` (Signal 15)**, waiting a grace period (`stop_grace_period: 30s`), and then sending **`SIGKILL` (Signal 9)** if the process hasn't exited.
- **Why this matters for Django & Celery:**
  - If your `Dockerfile` uses shell form `ENTRYPOINT python manage.py ...` (which runs `/bin/sh -c` as **PID 1**), `/bin/sh` does **not** forward `SIGTERM` to child Python processes! The container hangs for 30s and gets brutally killed with `SIGKILL` mid-transaction—corrupting marketplace syncs!
  - **The Fix:** Always use **exec form** (`CMD ["gunicorn", "ruit.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]` or `CMD ["celery", "-A", "ruit", "worker", "-l", "info"]`) so Gunicorn/Celery runs as **PID 1** (or use `init: true` / `tini`).
  - When Celery receives `SIGTERM`, it enters **warm shutdown**: stops pulling new tasks from Redis, finishes any currently executing marketplace API call, acknowledges it, and exits cleanly with code `0`.

### 1.2 File Descriptors (`ulimit -n`) & Zombies
- Every open TCP socket (Postgres, Redis, HTTPX connection pool, WebSocket) is a **file descriptor** in Linux. High-concurrency async workers need `ulimit -n 65535` (default 1024 will crash with `OSError: [Errno 24] Too many open files`).
- When running headless Chromium (Playwright) inside Docker, always enable **`init: true`** (runs `tini` as PID 1) and **`shm_size: '2gb'`** (or `--disable-dev-shm-usage`). Without `init: true`, crashed Chromium renderer subprocesses become `<defunct>` **zombie processes** that exhaust the container's PID table!

### 1.3 Production Docker & Docker Compose Best Practices
- **Multi-Stage Builds:** Stage 1 (`builder`) installs build compilers (`gcc`, `libpq-dev`) and compiles wheels into a virtualenv; Stage 2 (`runtime` on `python:3.12-slim`) copies only the compiled virtualenv and app code—shrinking image size by 60%+ and removing compiler attack surface.
- **Layer Caching:** Copy `pyproject.toml` / `uv.lock` / `requirements.txt` and run `pip install` *before* `COPY . .` so code changes don't invalidate the dependency layer cache.
- **Security & Healthchecks:** Run as a non-root user (`USER appuser`) and define `HEALTHCHECK` + `depends_on: { db: { condition: service_healthy } }` in `docker-compose.yml`.

---

## 2. Deployment Strategies & Zero-Downtime Database Migrations

### 2.1 Rolling vs Blue-Green vs Canary Deployments
- **Rolling Update:** Replaces instances gradually (e.g., 2 of 6 containers at a time). Simple, zero extra hardware cost, **but requires old code (v1) and new code (v2) to run simultaneously against the exact same database!**
- **Blue-Green:** Spins up a complete parallel "Green" environment alongside "Blue", runs smoke tests, and flips the load balancer router (`Nginx`/`Traefik`/`ALB`) instantaneously. Instant rollback by flipping traffic back to Blue.
- **Canary:** Routes 5% of traffic (or internal test seller accounts) to v2 first; monitors error rates/latency before rolling out to 100%.

### 2.2 The Expand-and-Contract Pattern for Zero-Downtime Django Migrations
**Guaranteed Senior Question:** *"How do you rename or drop a column, or add a `NOT NULL` constraint, on a 50-million-row Postgres table in Django without downtime?"*

If you simply rename a column or run `migrations.RemoveField` and deploy:
1. During the deployment window, **v1 containers are still running** and executing `SELECT old_column FROM items`—as soon as the migration runs before all v1 containers stop, v1 crashes with `ProgrammingError: column "old_column" does not exist`!
2. Even worse, adding a column with a volatile default or adding a foreign key / constraint naively in PostgreSQL acquires an **`ACCESS EXCLUSIVE` lock**, blocking **all reads and writes** on the table!

**The 3-Phase Expand-and-Contract Solution:**

| Phase | What You Deploy | Impact on Live Traffic |
| :--- | :--- | :--- |
| **1. Expand** | Add the new column as **`null=True`** (instant metadata-only operation in Postgres 11+!). Deploy code that **dual-writes** to both `old_col` and `new_col`, while still reading from `old_col`. | Zero locks, v1 and v2 are 100% compatible. |
| **2. Backfill & Switch** | Run a batched background task (`chunk_size=5000` with brief sleeps so you don't saturate DB IOPS or replication lag) to copy `old_col` $\rightarrow$ `new_col` for historical rows. Switch code to read from `new_col`. | Zero downtime. |
| **3. Contract** | Remove references to `old_col` from Django model (using `SeparateDatabaseAndState` first if needed), then drop `old_col` in a subsequent deploy once zero v1 containers exist. | Zero errors. |

**Postgres Locking Pro-Tips in Django Migrations:**
- **Indexes:** Always create indexes with **`AddIndexConcurrently`** (`CREATE INDEX CONCURRENTLY` inside a migration with `atomic = False`), which builds the index without blocking concurrent writes!
- **Constraints / Foreign Keys:** Add constraints with **`NOT VALID`** first (instant, doesn't scan existing rows under an exclusive lock), then run **`VALIDATE CONSTRAINT`** in a second step (only takes a `SHARE UPDATE EXCLUSIVE` lock, which allows normal reads and writes!).

---

## 3. The 3 Pillars of Observability (Metrics, Logs, Traces) + Scaling

In an integration platform like Ruit, generic CPU/RAM graphs aren't enough—you need **domain-aware observability**:

1. **Metrics (Prometheus + Grafana — "What is broken right now?"):**
   - Track the **RED Method** per marketplace and endpoint:
     - `ruit_marketplace_requests_total{marketplace="vinted", endpoint="publish", status="429"}` (**Rate & Errors**)
     - `ruit_marketplace_request_duration_seconds_bucket{marketplace="vinted"}` (**Duration** histogram for p50/p95/p99)
   - Track **Celery Queue Depth & Lag** (`ruit_celery_queue_length{queue="critical_delist"}` and `oldest_task_age_seconds`). If `critical_delist` lag exceeds 10 seconds, auto-scale workers or page immediately!
2. **Structured Logs (`structlog` — "Why did this specific seller's item fail?"):**
   - Emit single-line JSON logs containing context variables bound via `contextvars`: `correlation_id`, `seller_id`, `item_id`, `marketplace`, `task_id`, `proxy_id`.
3. **Distributed Traces (OpenTelemetry + Sentry — "Where was the latency spent?"):**
   - Propagate the W3C `traceparent` header from the incoming Django HTTP request $\rightarrow$ into the Celery task headers (`before_task_publish` signal) $\rightarrow$ into the worker's `httpx` spans and SQL queries, giving a single waterfall view across processes.
4. **Scaling & Backpressure:**
   - Scale stateless ASGI web workers and Celery workers horizontally behind a load balancer.
   - Protect PostgreSQL with **PgBouncer** connection pooling, read replicas for heavy analytics queries, and **table partitioning** on high-volume append-only tables (like `marketplace_sync_logs` partitioned monthly by `created_at`).
