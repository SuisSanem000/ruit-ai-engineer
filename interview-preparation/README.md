# Ruit Final Onsite Interview Preparation Hub (10-Hour Study & Practice Kit)

> **Candidate:** Simin Shoeibi  
> **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival $\rightarrow$ `13:00h–16:00h` @ Lanzadera, Valencia)  
> **Primary Source:** Built strictly around CEO **Luis Grau's literal evaluation cheat sheet** (`resources/first emails.md`).

---

## Quick Navigation (Start Here)

### 0. Roadmap, Mental Bridge & Euromed Train Flash Sheet (`00-roadmap-and-quick-sheets/`)
- [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) — Your hour-by-hour 10-hour study & active-recall plan.
- [01-ts-node-to-python-django-bridge.md](./00-roadmap-and-quick-sheets/01-ts-node-to-python-django-bridge.md) — Side-by-side translation of your 9+ years of TypeScript/Node.js expertise into Python/Django/Pydantic/Celery idioms.
- [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) — **Read on Friday morning on the train to Valencia:** 30-second senior answers for every single item on Luis's email cheat sheet.

---

### 1. Hours 1.0 – 2.0: Live AI Setup, Parallel Agents & Live Task Sandbox (`01-ai-workflow-and-live-task/`)
- [01-laptop-setup-and-agentic-workflow-script.md](./01-ai-workflow-and-live-task/01-laptop-setup-and-agentic-workflow-script.md) — Exact script for showing your laptop setup (`ai-state.md`, Skills, Rules, Plugins/MCPs, and **parallel agent sessions**).
- [02-live-ai-coding-playbook.md](./01-ai-workflow-and-live-task/02-live-ai-coding-playbook.md) — Your 5-step protocol for the 20-minute live AI task + what to audit in AI-generated Python code.
- **Runnable Sandbox (`live-task-sandbox/`):**
  - [README.md](./01-ai-workflow-and-live-task/live-task-sandbox/README.md) — 3 realistic 20-minute Ruit task prompts.
  - [marketplace_connector.py](./01-ai-workflow-and-live-task/live-task-sandbox/marketplace_connector.py) — Reference async connector with Pydantic v2, schema-drift detector, `Retry-After` backoff+jitter, and `asyncio.Semaphore` cross-marketplace delister.
  - [test_marketplace_connector.py](./01-ai-workflow-and-live-task/live-task-sandbox/test_marketplace_connector.py) — 5 `pytest` tests using `httpx.MockTransport`.

---

### 2. Hours 2.0 – 4.0: Python & Django Deep Dive (`02-python-and-django-deep-dive/`)
- [01-the-gil-concurrency-and-async-python.md](./02-python-and-django-deep-dive/01-the-gil-concurrency-and-async-python.md) — CPython GIL, reference counting, I/O vs CPU-bound, `asyncio` vs `threading` vs `multiprocessing`, and Python 3.13+ free-threading (PEP 703).
- [02-async-django-and-orm-internals.md](./02-python-and-django-deep-dive/02-async-django-and-orm-internals.md) — WSGI vs ASGI, `sync_to_async`, `SynchronousOnlyOperation` traps, `transaction.atomic()`, `select_related` vs `prefetch_related`, `F()` & `Q()` expressions.
- [03-generators-iterators-and-streaming.md](./02-python-and-django-deep-dive/03-generators-iterators-and-streaming.md) — Iterator protocol, `yield`, `yield from`, `@contextmanager`, async generators (`async for`), and $O(1)$ memory streaming.
- [04-robust-python-typing-pydantic-static-analysis.md](./02-python-and-django-deep-dive/04-robust-python-typing-pydantic-static-analysis.md) — `typing.Protocol`, `TypedDict`, `Generic`, Pydantic v2 (`model_validate_json`), `ruff`, `mypy`, and classic Python footguns.
- **Runnable Code Lab:** [test_python_deep_dive_labs.py](./02-python-and-django-deep-dive/python-django-labs/test_python_deep_dive_labs.py).

---

### 3. Hours 4.0 – 6.0: Backend Fundamentals Part 1 (`03-backend-fundamentals-cheatsheet/`)
- [01-celery-redis-and-background-queues.md](./03-backend-fundamentals-cheatsheet/01-celery-redis-and-background-queues.md) — Celery + Redis vs RabbitMQ, `visibility_timeout`, `acks_late=True`, `transaction.on_commit()`, idempotency, backoff+jitter, queue isolation, and DLQs.
- [02-databases-sql-locking-and-redis-caching.md](./03-backend-fundamentals-cheatsheet/02-databases-sql-locking-and-redis-caching.md) — Postgres MVCC & HOT updates, B-Tree/Partial/GIN indexes, `SELECT ... FOR UPDATE` vs optimistic locking, PgBouncer, and Redis caching + distributed locks.
- [03-error-handling-python-vs-go-vs-rust.md](./03-backend-fundamentals-cheatsheet/03-error-handling-python-vs-go-vs-rust.md) — Python EAFP exceptions vs Go explicit `err != nil` vs Rust `Result<T, E>` / `?` operator + action-oriented integration error hierarchies.
- **Runnable Code Lab:** [test_concurrency_locks_and_errors.py](./03-backend-fundamentals-cheatsheet/fundamentals-labs/test_concurrency_locks_and_errors.py).

---

### 4. Hours 6.0 – 8.0: Backend Fundamentals Part 2 (`04-integrations-reverse-eng-browsers/`)
- [01-http-clients-tls-fingerprinting-and-networking.md](./04-integrations-reverse-eng-browsers/01-http-clients-tls-fingerprinting-and-networking.md) — TCP vs UDP, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), WebSockets scaling, `httpx` connection pooling, and **JA3/JA4 TLS + HTTP/2 fingerprinting (`curl_cffi`)**.
- [02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md](./04-integrations-reverse-eng-browsers/02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md) — Intercepting web/mobile APIs (`mitmproxy`, HAR files, Frida SSL unpinning, Redis-locked token refresh, HMAC signing) and **proactive breakage detection**.
- [03-browsers-playwright-and-chrome-extensions.md](./04-integrations-reverse-eng-browsers/03-browsers-playwright-and-chrome-extensions.md) — Playwright & CDP hybrid mode, anti-bot evasion, and **Chrome Extensions (Manifest V3)** (Service Workers, Content Scripts, Isolated vs MAIN world).
- [04-devops-docker-zero-downtime-and-observability.md](./04-integrations-reverse-eng-browsers/04-devops-docker-zero-downtime-and-observability.md) — Linux `SIGTERM` graceful drain, Docker multi-stage builds, Blue-Green/Rolling deploys, **Expand-and-Contract zero-downtime Django migrations**, and Prometheus/Structlog/OpenTelemetry.

---

### 5. Hours 8.0 – 9.5: Collaborative System Design Whiteboard (`05-system-design-whiteboard/`)
- [00-collaborative-whiteboard-framework.md](./05-system-design-whiteboard/00-collaborative-whiteboard-framework.md) — Pacing & teamwork framework for the 60-minute whiteboard session (`15:00–16:00`).
- [01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md](./05-system-design-whiteboard/01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md)
- [02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md](./05-system-design-whiteboard/02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md)
- [03-challenge-3-rapid-new-marketplace-connector-architecture.md](./05-system-design-whiteboard/03-challenge-3-rapid-new-marketplace-connector-architecture.md)
- [04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md](./05-system-design-whiteboard/04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md)
- [05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md](./05-system-design-whiteboard/05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md)

---

### 6. Hours 9.5 – 10.0: Storytelling & Team Lunch (`06-culture-lunch-and-storytelling/`)
- [01-my-3-signature-stories-for-ruit.md](./06-culture-lunch-and-storytelling/01-my-3-signature-stories-for-ruit.md) — Your 90-second pitches + technical follow-ups for (1) 150+ Site News Crawler, (2) 630K-Install Dadroit JSON Generator, and (3) QueryLaw Antifragile AI Engine.
- [02-team-lunch-and-questions-for-luis-and-team.md](./06-culture-lunch-and-storytelling/02-team-lunch-and-questions-for-luis-and-team.md) — Winning the team lunch + tailored questions for Luis Grau and the engineering team.

---

## Verification Command
To run all code lab tests, linter checks, and static type checks offline using the pre-configured `.venv`:
```bash
.venv/bin/pytest interview-preparation/ -v && .venv/bin/ruff check interview-preparation/ && .venv/bin/mypy interview-preparation/
```

