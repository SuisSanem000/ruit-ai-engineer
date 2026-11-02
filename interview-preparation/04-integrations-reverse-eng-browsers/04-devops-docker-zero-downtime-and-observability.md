# DevOps, Zero-Downtime Deployments, Observability & Scaling

> **From Luis's Email Cheat Sheet:** *"devops (linux, docker and docker compose, deployment strategies, zero downtime strategies), observability (metrics, logs, traces), scaling, etc."*

---

## 1. Linux & Docker Basics for Backend Production

- **Graceful Shutdown with Linux Signals (`SIGTERM` vs `SIGKILL`):**
  - When deploying new Docker containers, the server sends **`SIGTERM`** first (telling the app to finish current work and stop) and waits ~30 seconds before sending **`SIGKILL`** (hard kill).
  - **Important Rule:** Run Gunicorn and Celery using Docker `CMD ["celery", ...]` (exec form) so the Python process receives `SIGTERM` directly, finishes its current marketplace API call, and exits cleanly without losing jobs.
- **File Descriptors (`ulimit -n`) & Zombie Processes:**
  - Every network connection (Postgres, Redis, HTTP calls, WebSockets) counts as an open file in Linux. Increase `ulimit -n` (e.g., to `65535`) on high-concurrency servers.
  - For Docker containers running headless Chrome (Playwright), turn on **`init: true`** and **`shm_size: '2gb'`** so crashed browser tabs do not become zombie processes or run out of shared memory.
- **Docker & Docker Compose Tips:**
  - Use **multi-stage builds** to keep final images small and secure.
  - Copy `requirements.txt` / `pyproject.toml` and install packages *before* copying code (`COPY . .`) so Docker reuses cached layers on every build.
  - Run containers as a non-root user and add healthchecks (`HEALTHCHECK`).

---

## 2. Deployment Strategies & Zero-Downtime Database Migrations

- **Rolling vs Blue-Green vs Canary Deploys:**
  - **Rolling:** Replaces old containers a few at a time. Simple, but means **old code (v1) and new code (v2) run at the exact same time** against the same database for a few minutes.
  - **Blue-Green:** Starts a full new set of containers ("Green") next to the old ones ("Blue"), tests them, and switches router traffic all at once. Instant rollback if something breaks.
  - **Canary:** Sends 5% of traffic to the new version first to check error rates before rolling out to 100%.
- **Zero-Downtime Database Migrations (Expand and Contract Pattern):**
  - **The Problem:** If you rename or delete a column in PostgreSQL and deploy, the old v1 containers that are still running for 30 seconds will crash with `column does not exist`! Also, naive `ALTER TABLE` commands can lock the whole table.
  - **The 3-Step Fix (Expand and Contract):**
    1. **Expand:** Add the new column as **nullable (`null=True`)** (instant in Postgres, no lock). Deploy code that writes to both the old and new columns.
    2. **Backfill:** Copy old data into the new column in small batches (`5,000 rows` at a time), then switch code to read from the new column.
    3. **Contract:** Remove the old column from the code, and drop the old column in a later deploy when no old containers are running.
  - **Safe Postgres Indexes:** Always create new indexes on big tables using **`CREATE INDEX CONCURRENTLY`** (`AddIndexConcurrently` in Django) so Postgres does not block writes while building the index.

---

## 3. Observability (Metrics, Logs, Traces) & Scaling

- **1. Metrics (Prometheus & Grafana — "What is broken right now?"):**
  - Track **Request rate**, **Error rate** (`401`, `403`, `429`, `5xx`), and **Duration (latency)** per marketplace.
  - Track **Celery Queue Length and Wait Time** (if the urgent `delist` queue falls behind by more than 10 seconds, send an alert).
- **2. Structured Logs (`structlog` — "Why did this item fail?"):**
  - Log in **JSON format** and attach `correlation_id`, `seller_id`, `item_id`, and `marketplace` to every log line so you can filter all logs for one failed listing in seconds.
- **3. Distributed Traces (OpenTelemetry & Sentry — "Where was the time spent?"):**
  - Pass a `trace_id` from the incoming Django HTTP request into the Celery job header so you can see the full timeline from web request $\rightarrow$ Redis queue $\rightarrow$ Celery worker $\rightarrow$ Vinted API call.
- **4. Scaling:**
  - Scale stateless Django web servers and Celery workers horizontally (add more containers).
  - Protect PostgreSQL using **PgBouncer** connection pooling, read replicas for heavy analytics, and separate Celery queues so slow tasks never block fast tasks.
