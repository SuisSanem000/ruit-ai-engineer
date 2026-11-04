# Ruit Final Interview Preparation (Consolidated Master Guide)

> **Position Applying For:** **Senior Backend Engineer, Integrations (Python)**  
> *(Dual Consideration: Luis confirmed you are also considered for **Senior Full Stack Engineer, Integrations (Python) / AI Engineer**).*
>
> - **Candidate:** Simin Shoeibi
> - **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival @ Lanzadera, Valencia)
> - **Company Guide:** [COMPANY-AND-PRODUCT-GUIDE.md](./COMPANY-AND-PRODUCT-GUIDE.md) (~€1M funding, €1M ARR target, 1-photo AI listing, anti-double-sell sync)
> - **Main Source:** Luis's email cheat sheet ([`docs/resources/first emails.md`](../docs/resources/first%20emails.md))

---

## Study Progress Tracker

| Section | Core Files | Status |
| :--- | :--- | :--- |
| **Company & Role** | [COMPANY-AND-PRODUCT-GUIDE.md](./COMPANY-AND-PRODUCT-GUIDE.md) | `[ ] Pending` |
| **0. Roadmap & Quick Sheets** | [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) | `[x] COMPLETED` |
| | [01-ts-node-to-python-django-bridge.md](./00-roadmap-and-quick-sheets/01-ts-node-to-python-django-bridge.md) | `[x] COMPLETED` |
| | [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) | `[x] COMPLETED` |
| **1. AI Workflow & Live Task** | Files `01` to `03` & `live-task-sandbox/` | `[ ] Up Next / Revisit` |
| **2. Python & Django Deep Dive** | Files `01` and `02` & `python-django-labs/` | `[ ] Pending` |
| **3. Backend Fundamentals (Queues, Locks)** | Files `01` and `02` & `fundamentals-labs/` | `[ ] Pending` |
| **4. Networking, Reverse Eng, DevOps** | Files `01` and `02` | `[⏳ READING NOW]` |
| **5. System Design Whiteboard** | Files `01` and `02` (5 Ruit Challenges) | `[ ] Pending` |
| **6. Stories & Team Lunch** | File `01` (STAR stories & questions) | `[ ] Pending` |

---

## Consolidated Module Index (Lean & High-Signal)

- **0. Roadmap & Quick Sheets (`00-roadmap-and-quick-sheets/`)**
  - [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) — 6-step study schedule.
  - [01-ts-node-to-python-django-bridge.md](./00-roadmap-and-quick-sheets/01-ts-node-to-python-django-bridge.md) — Node.js vs Python concept bridge and honest positioning.
  - [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) — 10-minute cheat sheet for the train ride.

- **1. AI Workflow, Laptop Setup & Live Task (`01-ai-workflow-and-live-task/`)**
  - [01-my-real-ai-story-and-daily-workflow.md](./01-ai-workflow-and-live-task/01-my-real-ai-story-and-daily-workflow.md) — Real resume story (QueryLaw AJV schema validation, 150-site crawler, Dadroit extension) and 5-step daily workflow.
  - [02-multi-agents-laptop-setup-and-live-task-playbook.md](./01-ai-workflow-and-live-task/02-multi-agents-laptop-setup-and-live-task-playbook.md) — Multi-agent patterns, 3-minute screen-share walkthrough script, 20-minute live task execution plan, and 5 code audit checks.
  - [03-spoken-qa-scripts-how-i-work-with-ai.md](./01-ai-workflow-and-live-task/03-spoken-qa-scripts-how-i-work-with-ai.md) — 6 spoken Upper-B2 interview scripts.
  - [live-task-sandbox/](./01-ai-workflow-and-live-task/live-task-sandbox/) — Basic Python integration code and offline tests (`pytest` passing).

- **2. Python & Django Deep Dive (`02-python-and-django-deep-dive/`)**
  - [01-the-gil-concurrency-and-async-django.md](./02-python-and-django-deep-dive/01-the-gil-concurrency-and-async-django.md) — The GIL, I/O vs CPU concurrency, WSGI vs ASGI, and fixing N+1 queries.
  - [02-generators-streaming-pydantic-and-typing.md](./02-python-and-django-deep-dive/02-generators-streaming-pydantic-and-typing.md) — Generators, streaming large catalogs, Pydantic validation, and static analysis.
  - [python-django-labs/](./02-python-and-django-deep-dive/python-django-labs/) — Basic Python labs for generators, context managers, and Django ORM concepts.

- **3. Backend Fundamentals (Queues, Locks & Errors) (`03-backend-fundamentals-cheatsheet/`)**
  - [01-celery-redis-and-sql-locking.md](./03-backend-fundamentals-cheatsheet/01-celery-redis-and-sql-locking.md) — Celery worker queues, Redis cache stampede prevention, and SQL `SELECT ... FOR UPDATE` double-sell prevention.
  - [02-error-handling-python-vs-go-vs-rust.md](./03-backend-fundamentals-cheatsheet/02-error-handling-python-vs-go-vs-rust.md) — Comparing error handling philosophies and integration error hierarchies.
  - [fundamentals-labs/](./03-backend-fundamentals-cheatsheet/fundamentals-labs/) — Basic Python concurrency, locking, and rate limiting labs.

- **4. Networking, Reverse Engineering, Browsers & DevOps (`04-integrations-reverse-eng-browsers/`)**
  - [01-networking-protocols-and-tls.md](./04-integrations-reverse-eng-browsers/01-networking-protocols-and-tls.md) — TCP 3-way handshake, UDP, DNS, HTTP/1.1 vs HTTP/2 vs HTTP/3, WebSockets vs SSE vs Webhooks, and TLS fingerprinting bypass (`curl_cffi`).
  - [02-reverse-engineering-browsers-and-devops.md](./04-integrations-reverse-eng-browsers/02-reverse-engineering-browsers-and-devops.md) — `.har` traffic analysis, Chrome Extensions (MV3), Playwright, zero-downtime DB migrations, and observability.

- **5. System Design Whiteboard (`05-system-design-whiteboard/`)**
  - [01-collaborative-framework-and-architecture.md](./05-system-design-whiteboard/01-collaborative-framework-and-architecture.md) — 4-step collaborative whiteboard framework and spoken phrases.
  - [02-the-5-ruit-system-design-challenges.md](./05-system-design-whiteboard/02-the-5-ruit-system-design-challenges.md) — Complete architectures for the 5 real Ruit challenges (Breakage detection, double-sell prevention, rapid connector adapter, 1-photo AI mapping, hybrid Chrome extension).

- **6. Stories, Team Lunch & Questions (`06-culture-lunch-and-storytelling/`)**
  - [01-stories-lunch-and-questions.md](./06-culture-lunch-and-storytelling/01-stories-lunch-and-questions.md) — 3 STAR stories (Visual Meta B2B SaaS, Dotin banking deadlock fix, Visual Meta PHP rewrite), lunch etiquette, and questions for Luis and the team.
