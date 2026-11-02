# Master 10-Hour Study & Practice Schedule — Ruit Final Onsite (Valencia)

> **Candidate:** Simin Shoeibi  
> **Interview Date:** Friday, November 6, 2026 (`12:45 CET` arrival $\rightarrow$ `13:00–16:00 CET` interviews @ Lanzadera, Valencia)  
> **Interviewer:** Luis Grau (CEO) & Ruit Engineering Team  
> **Primary Source of Truth:** Luis Grau's literal evaluation cheat sheet from `resources/first emails.md`

---

## 1. The Onsite Day Blueprint (Friday, Nov 6)

| Time | Block | What Happens | What Wins the Offer |
| :--- | :--- | :--- | :--- |
| **12:45 – 13:00** | **Arrival & Tour** | Arrive at Lanzadera (Marina de Empresas) with your sister (who can relax in the waiting area). Office tour with Luis/team. | Warm energy, curiosity about their workspace and team dynamics. |
| **13:00 – 14:00** | **Interview 1: Laptop AI Setup, Live Task & Cheat-Sheet Concepts (45–60m)** | **1. Laptop Showcase & Brief AI Task (~20m):** Fire up your laptop, show your AI setup (agents, skills, plugins, parallel sessions), and solve a short practical task.<br>**2. Technical Concepts Chat (~35m):** Conversational deep dive into Luis's literal cheat sheet (Python/Django internals + Backend/Integration fundamentals). | **Speed + Verification:** Show a structured, multi-agent workflow (context files, schema-first Pydantic, automated pytest/ruff checks) and crisp, senior-level explanations bridging your 9+ years of high-load systems to Python/Django. |
| **14:00 – 15:00** | **Interview 2: Lunch with the Team (60m)** | *"This is the most important part. It's on the house."* Casual lunch near Lanzadera. | **Ownership + Low Ego:** Genuine excitement about second-hand commerce, customer empathy, war stories from your 150-site crawler & 630K-install extension. |
| **15:00 – 16:00** | **Interview 3: System Design Whiteboard (60m)** | Choose **1 of ~5 real Ruit challenges** for the coming months. Design it together on the whiteboard and compare with their existing approach. *"This is teamwork!"* | **Collaborative Co-Design:** Clarify constraints first, draw clear data/queue flows, ask *"How do you currently handle X?"*, and focus on reliability & proactive breakage detection. |

---

## 2. Hour-by-Hour 10-Hour Preparation Plan

### Hours 1.0 – 2.0: Live AI Setup & Agentic Workflow Mastery
**Folder:** [`01-ai-workflow-and-live-task/`](../01-ai-workflow-and-live-task/)

- **0:00 – 0:25 (25m) | Read & Rehearse Your Laptop Tour:**
  - Read [`01-laptop-setup-and-agentic-workflow-script.md`](../01-ai-workflow-and-live-task/01-laptop-setup-and-agentic-workflow-script.md).
  - Practice a **3-minute live walkthrough** of your screen:
    1. How you maintain persistent context (`ai-state.md`, architecture specs) so agents never hallucinate project state.
    2. How you use **Skills (`SKILL.md`), Rules, and Plugins/MCPs**.
    3. How you run **parallel agent sessions** (e.g., Session 1 analyzing raw API network payloads/HAR files, Session 2 writing Pydantic v2 models & async `httpx` client, Session 3 writing `pytest` edge-case tests).
- **0:25 – 0:45 (20m) | Study the 5-Step Live Task Playbook:**
  - Read [`02-live-ai-coding-playbook.md`](../01-ai-workflow-and-live-task/02-live-ai-coding-playbook.md).
- **0:45 – 2:00 (75m) | Hands-On Timed Practice in the Live Task Sandbox:**
  - Open [`live-task-sandbox/`](../01-ai-workflow-and-live-task/live-task-sandbox/).
  - Run the existing test suite (`pytest`) and inspect the 3 realistic 20-minute Ruit tasks.
  - Pick 1 practice prompt, open a fresh agent prompt, and complete it end-to-end in **under 18 minutes** while narrating your thought process out loud.

---

### Hours 2.0 – 4.0: Python & Django Deep Dive (Bridging from TS/Node)
**Folder:** [`02-python-and-django-deep-dive/`](../02-python-and-django-deep-dive/)

- **2:00 – 2:20 (20m) | TS/Node $\rightarrow$ Python/Django Mental Bridge:**
  - Read [`01-ts-node-to-python-django-bridge.md`](./01-ts-node-to-python-django-bridge.md).
- **2:20 – 2:50 (30m) | The GIL, Concurrency & Async Python:**
  - Study [`01-the-gil-concurrency-and-async-python.md`](../02-python-and-django-deep-dive/01-the-gil-concurrency-and-async-python.md).
  - *Active Recall Check:* Explain out loud why CPython has a GIL (reference counting thread safety), why `asyncio` excels at 1,000 concurrent marketplace HTTP calls despite the GIL, when you need `multiprocessing` (CPU-bound image/HTML parsing), and what PEP 703 (Python 3.13+ free-threading) changes.
- **2:50 – 3:20 (30m) | Async in Django & ORM Internals:**
  - Study [`02-async-django-and-orm-internals.md`](../02-python-and-django-deep-dive/02-async-django-and-orm-internals.md).
  - *Active Recall Check:* Contrast WSGI vs ASGI, explain `sync_to_async` vs `async_to_sync`, why `transaction.atomic()` still requires sync context in Django, and `select_related` (SQL JOIN) vs `prefetch_related` (2 queries + Python join).
- **3:20 – 3:40 (20m) | Generators, Iterators & Streaming Pipelines:**
  - Study [`03-generators-iterators-and-streaming.md`](../02-python-and-django-deep-dive/03-generators-iterators-and-streaming.md).
  - *Active Recall Check:* Explain how `yield`, `yield from`, and `async for` keep memory flat ($O(1)$ RAM) when streaming 500K marketplace listings or `.iterator(chunk_size=2000)` in Django ORM.
- **3:40 – 4:00 (20m) | Robust Python (Typing, Pydantic v2, Static Analysis) + Code Lab:**
  - Study [`04-robust-python-typing-pydantic-static-analysis.md`](../02-python-and-django-deep-dive/04-robust-python-typing-pydantic-static-analysis.md) and run `pytest` inside [`python-django-labs/`](../02-python-and-django-deep-dive/python-django-labs/).

---

### Hours 4.0 – 6.0: Backend Fundamentals Part 1 (Queues, SQL, Cache, Errors)
**Folder:** [`03-backend-fundamentals-cheatsheet/`](../03-backend-fundamentals-cheatsheet/)

- **4:00 – 4:45 (45m) | Background Queues & Brokers (Celery & Redis / RabbitMQ):**
  - Study [`01-celery-redis-and-background-queues.md`](../03-backend-fundamentals-cheatsheet/01-celery-redis-and-background-queues.md).
  - *Focus:* `acks_late=True`, Redis visibility_timeout pitfalls, idempotency keys (preventing duplicate marketplace listings), exponential backoff + jitter, per-marketplace rate-limiting queues, and Dead Letter Queues (DLQs).
- **4:45 – 5:25 (40m) | Databases, SQL Locking & Redis Caching:**
  - Study [`02-databases-sql-locking-and-redis-caching.md`](../03-backend-fundamentals-cheatsheet/02-databases-sql-locking-and-redis-caching.md).
  - *Focus:* Preventing double-sells when an item sells simultaneously on Vinted and Wallapop (`SELECT ... FOR UPDATE NOWAIT / SKIP LOCKED` vs optimistic locking version column + Redis Redlock), Postgres MVCC, B-Tree vs GIN JSONB indexes, PgBouncer, and cache stampede protection.
- **5:25 – 6:00 (35m) | Error Handling Philosophy (Python vs Go vs Rust):**
  - Study [`03-error-handling-python-vs-go-vs-rust.md`](../03-backend-fundamentals-cheatsheet/03-error-handling-python-vs-go-vs-rust.md).
  - *Focus:* Python EAFP exceptions vs Go explicit `if err != nil` values vs Rust algebraic `Result<T, E>` / `?` operator—and how to build a strict integration error taxonomy in Python (`RetryableNetworkError`, `RateLimitedError`, `SellerAuthExpiredError`, `UpstreamSchemaBreakageError`).

---

### Hours 6.0 – 8.0: Backend Fundamentals Part 2 (Networking, TLS, Reverse Eng, Browsers, DevOps)
**Folder:** [`04-integrations-reverse-eng-browsers/`](../04-integrations-reverse-eng-browsers/)

- **6:00 – 6:30 (30m) | HTTP Clients, TLS Fingerprinting & Low-Level Networking:**
  - Study [`01-http-clients-tls-fingerprinting-and-networking.md`](../04-integrations-reverse-eng-browsers/01-http-clients-tls-fingerprinting-and-networking.md).
  - *Focus:* TCP vs UDP, HTTP/1.1 vs HTTP/2 multiplexing vs HTTP/3 (QUIC), WebSockets scaling (your 60K+ concurrent users Socket.IO story!), TLS 1.3 handshake, and **why standard Python `requests`/`httpx` gets blocked by Cloudflare/DataDome (JA3/JA4 TLS fingerprinting + HTTP/2 frame fingerprinting) and how `curl_cffi` fixes it**.
- **6:30 – 7:05 (35m) | API Integrations, Rebuilding APIs from Traffic & Keeping Them Alive:**
  - Study [`02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md`](../04-integrations-reverse-eng-browsers/02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md).
  - *Focus:* Intercepting mobile/web traffic (`mitmproxy`, HAR files, token refresh flows, CSRF/HMAC signatures), residential proxy rotation, and **proactive breakage detection** (synthetic canary probes + Pydantic schema drift alerts).
- **7:05 – 7:35 (30m) | Browsers, Automations & Chrome Extensions:**
  - Study [`03-browsers-playwright-and-chrome-extensions.md`](../04-integrations-reverse-eng-browsers/03-browsers-playwright-and-chrome-extensions.md).
  - *Focus:* Playwright & CDP, stealth evasion, and **Chrome Extensions (Manifest V3)** (Content Scripts vs Service Workers, message passing, and using the extension to execute cross-listing requests from the seller's own authenticated browser IP/session).
- **7:35 – 8:00 (25m) | DevOps, Zero-Downtime Deployments & Observability:**
  - Study [`04-devops-docker-zero-downtime-and-observability.md`](../04-integrations-reverse-eng-browsers/04-devops-docker-zero-downtime-and-observability.md).
  - *Focus:* Linux `SIGTERM` graceful Celery worker draining, Docker Compose, Blue-Green/Rolling deployments, **Expand-and-Contract zero-downtime Postgres migrations in Django**, and the 3 pillars of observability (Metrics, Structured Logs with correlation IDs, OpenTelemetry Traces).

---

### Hours 8.0 – 9.5: Collaborative System Design Whiteboard Mastery
**Folder:** [`05-system-design-whiteboard/`](../05-system-design-whiteboard/)

- **8:00 – 8:15 (15m) | The Collaborative Whiteboard Framework:**
  - Read [`00-collaborative-whiteboard-framework.md`](../05-system-design-whiteboard/00-collaborative-whiteboard-framework.md).
- **8:15 – 9:30 (75m — 15m per Challenge) | Master the 5 Ruit System Design Blueprints:**
  1. [`01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md`](../05-system-design-whiteboard/01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md)
  2. [`02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md`](../05-system-design-whiteboard/02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md)
  3. [`03-challenge-3-rapid-new-marketplace-connector-architecture.md`](../05-system-design-whiteboard/03-challenge-3-rapid-new-marketplace-connector-architecture.md)
  4. [`04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md`](../05-system-design-whiteboard/04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md)
  5. [`05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md`](../05-system-design-whiteboard/05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md)
  - *Practice:* Draw the box-and-arrow diagram for your top 2 favorite challenges on paper in under 10 minutes each.

---

### Hours 9.5 – 10.0: Signature Stories, Team Lunch & Final Flash Review
**Folder:** [`06-culture-lunch-and-storytelling/`](../06-culture-lunch-and-storytelling/)

- **9:30 – 9:50 (20m) | Your 3 Signature Engineering Stories & Team Lunch Questions:**
  - Read [`01-my-3-signature-stories-for-ruit.md`](../06-culture-lunch-and-storytelling/01-my-3-signature-stories-for-ruit.md) and [`02-team-lunch-and-questions-for-luis-and-team.md`](../06-culture-lunch-and-storytelling/02-team-lunch-and-questions-for-luis-and-team.md).
- **9:50 – 10:00 (10m) | Final Rapid Review (Save for the Euromed Train to Valencia):**
  - Skim [`02-euromed-train-rapid-cheatsheet.md`](./02-euromed-train-rapid-cheatsheet.md).

