# Ruit Final Interview Preparation — Project Context & AI State Tracker

> **Last Updated:** 2026-11-02 (Full Review & Polish Pass Complete — 100% Aligned with Email Cheat Sheet)  
> **Target Interview Date:** Friday, November 6, 2026 (`12:45h` arrival $\rightarrow$ `13:00h–16:00h` interviews)  
> **Location:** Ruit Offices @ Lanzadera, Valencia, Spain (Traveling from Barcelona via Euromed)  
> **Current Phase:** Phase 2 Complete — All Modules 0–6, Guides, Whiteboards & Code Labs Reviewed, Polished & Verified  
> **Total Prep Time Budget:** Up to 10 Hours (Structured into focused, high-ROI blocks)

---

## 1. Executive Context: Company, Product, Role & Interviewer

### 1.1 About Ruit (`https://ruit.es/en/` — `RUIT COMPARATOR S.L.`)
- **Mission & Vision (From Luis's Email):** *"We want second-hand to become the first way everyone in Europe shops, and we're building the tool that lets professional sellers sell on every marketplace from one place. Whoever joins now will shape a big part of what ruit becomes."*
- **The Product (Cross-Listing & Multi-Marketplace Management):**
  - Centralizes inventory, cross-listing, automated stock delisting (preventing double-sells when an item sells on one channel), dynamic pricing, orders, and analytics from one place.
  - **Connected & Target Marketplace Ecosystem (Directly Related to API Integrations & System Design):** Wallapop, Vinted, eBay, Milanuncios, Todocolección, IberLibro, Shopify, WooCommerce, PrestaShop, and expanding to Facebook Marketplace, Etsy, Poshmark, Mercari, Whatnot, Grailed, Depop, Vestiaire Collective, Amazon, and TikTok Shop.
- **Interviewer:** **Luis Grau** (CEO & Founder, `luis.grau@ruit.es`) and the Ruit engineering team at **Lanzadera** (Valencia).

### 1.2 Target Role & Core Integration Focus
- **Primary Role Applied:** **Senior Backend Engineer, Integrations (Python)** (also considered across AI/Full-Stack roles per Luis: *"you applied for multiple roles. There's no need to fill in two forms: I'll consider you for both roles with the one I sent you"*).
- **Core Technical Focus (Email Cheat Sheet + Directly Related Integration Scope):**
  - Building and maintaining resilient marketplace integrations in Python & Django (by official API, reverse-engineered network traffic, or browser/extension automation).
  - Keeping integrations alive when the other side changes and catching breakages via observability/validation before sellers notice.
  - Working daily with AI agents, skills, plugins, and parallel sessions.

---

## 2. Candidate Profile & Strategic Alignment (Simin Shoeibi)

### 2.1 Why Simin Already Stood Out to Luis (From `first emails.md`)
1. **Shipping Products People Rely On:** Built the **Dadroit JSON Generator** VS Code extension in 3 days (**630K+ installs**, top-10 extension) and contributed to a high-performance multi-GB desktop JSON Viewer (**60K+ users**).
2. **Real-World Integration & Crawling Experience:** Built and maintained the **crawler behind a semantic news app for over 150 sites** (60K+ DAU) at Parsaiane—which Luis explicitly highlighted as *"close to the integration work we do"*.
3. **Antifragile AI & Validation Pipelines:** Architected QueryLaw/TreeScribe's AI integration layer (Claude Opus/Sonnet, GPT-4o, 95%+ accuracy, dynamic context windows, multi-layer JSON Schema/AJV validation, guardrails, and backend telemetry to detect brittle logic).
4. **High-Load Backend & Real-Time Architecture:** 9+ years experience; scaled PERN/MERN systems to **60K+ concurrent users** with Node.js (NestJS, Fastify, Express), **Socket.IO / WebSockets**, PostgreSQL, Redis, RabbitMQ, Kafka, Docker, and Kubernetes.

### 2.2 The Key Technical Bridge to Master (TS/Node.js $\rightarrow$ Python/Django)
- Map Simin's deep expertise in Event Loop concurrency, AJV/Zod, Prisma/TypeORM, and BullMQ/RabbitMQ directly to **CPython's GIL + `asyncio`**, **Pydantic v2 + Python Type Hints (`Protocol`, `TypedDict`)**, **Django ORM (sync vs async ASGI)**, and **Celery + Redis**.
- Articulate cross-language engineering tradeoffs clearly (especially **Python vs Go vs Rust error-handling philosophies**, low-level networking & TLS fingerprinting, reverse-engineering APIs, and proactive breakage detection).

---

## 3. Final Onsite Schedule & Literal Evaluation Cheat Sheet (Friday, Nov 6)

| Time | Session | Format & What They Evaluate (Directly from `first emails.md`) |
| :--- | :--- | :--- |
| **12:45 – 13:00** | **Arrival & Office Tour** | Arrive at Lanzadera (Valencia) so the team can show you the offices. Sister can wait comfortably at the office. |
| **13:00 – 14:00** | **Interview 1: Conversational + Live AI Task + Cheat-Sheet Concepts (45–60 min)** | *"We will ask you to fire up your laptop, show us your setup and complete a brief task with AI. We will talk about it for a bit and then we will chat about some concepts (cheat sheet below)."* |
| **14:00 – 15:00** | **Lunch with the Team (60 min)** | *"This is the most important part. It's on the house."* Culture fit, ownership, curiosity, product mindset, and team chemistry. |
| **15:00 – 16:00** | **Interview 2: System Design Challenge (60 min)** | *"We have ~5 challenges for the following months. We will explain the challenges, and you will choose the one you like. We will design it together and see how it compares to our existing approach. This is teamwork!"* |

### 3.1 Luis's Literal Evaluation Cheat Sheet (`"Simin, this is literally my cheat sheet for evaluating candidates. This is all there is."`)

- [x] **1. Working with AI & Live Laptop Task**
  - [x] Fire up laptop, show setup, and complete a brief task with AI.
  - [x] How you use **agents, skills (`SKILL.md`), plugins/MCPs, rules, and context/state files (`ai-state.md`)**.
  - [x] How you use **sessions in parallel** (subagents, git worktrees, parallel payload forensics + implementation + adversarial test generation).
- [x] **2. Python & Django Knowledge**
  - [x] **The GIL (Global Interpreter Lock):** CPython reference counting, thread safety, CPU-bound vs I/O-bound, `threading` vs `multiprocessing` vs `asyncio`, Python 3.13+ free-threading (PEP 703).
  - [x] **Async in Django:** WSGI vs ASGI, `async def` views, `sync_to_async` & `async_to_sync`, Django ORM async methods (`aget`, `aiterator`) vs sync-only parts (`transaction.atomic`), connection pooling.
  - [x] **Generators:** `yield`, iterator protocol, lazy evaluation, streaming pipelines, `yield from`, async generators (`async for`), memory efficiency in large crawls/ETL.
  - [x] **Making Robust Python:** Type hints (`typing`, `Protocol`, `TypedDict`, `Generic`, `Annotated`), runtime validation (`Pydantic v2`), static analysis (`mypy`, `pyright`, `ruff`).
- [x] **3. Core Engineering Fundamentals**
  - [x] **Concurrency & Async:** Event loops, threads, processes, race conditions, distributed locks, idempotency.
  - [x] **JSON Validation:** Schema enforcement at boundaries (Pydantic v2 / JSON Schema / AJV), handling dirty/evolving 3rd-party marketplace JSON, schema drift detection.
  - [x] **ORMs & SQL:** Query optimization, N+1 (`select_related` vs `prefetch_related`), indexing (B-Tree, GIN, partial, composite), transactions, isolation levels, `SELECT ... FOR UPDATE SKIP LOCKED`.
  - [x] **Background Queues & Brokers (i.e. Celery & Redis / RabbitMQ):** Task lifecycle, acks (`acks_late`), visibility timeouts, retries + backoff/jitter, idempotency, rate-limiting queues per marketplace, Dead Letter Queues (DLQ).
  - [x] **HTTP Clients & TLS:** Connection pooling (`httpx`/`requests.Session`), timeouts, TLS 1.2/1.3 handshake, **TLS fingerprinting (JA3/JA4) & HTTP/2 fingerprinting** in anti-bot evasion (`curl_cffi`).
  - [x] **Error Handling & Philosophy Behind Them (Python vs Go vs Rust):** Exceptions (EAFP) vs Errors-as-Values (`if err != nil`) vs Algebraic `Result<T, E>` / `Option<T>`, and designing resilient integration error taxonomies.
  - [x] **Databases & Cache:** Postgres MVCC/VACUUM/PgBouncer, Redis data structures & caching patterns (Cache-Aside, stampede protection, TTL jitter, distributed locks).
  - [x] **Low-Level Networking & Protocols (HTTP, WS, etc.) and Their Peculiarities:** TCP/IP, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), WebSockets (upgrade, heartbeats, scaling via Redis Pub/Sub), Webhooks vs Polling.
  - [x] **API Integrations & Reverse Engineering:** Rebuilding undocumented web & mobile APIs from network traffic (`mitmproxy`, Chrome DevTools, HAR files, SSL unpinning concepts), auth flows (OAuth2, JWT refresh rotation, HMAC request signing, CSRF), proxy rotation, rate limits, and keeping integrations alive when the other side changes.
  - [x] **Browsers, Their Automations & Chrome Extensions:** Playwright/CDP, headless anti-detect, Chrome Extensions (Manifest V3, content scripts, background service workers, piggybacking on authenticated seller sessions).
  - [x] **DevOps (Linux, Docker & Docker Compose, Deployment Strategies, Zero-Downtime Strategies):** Linux signals (`SIGTERM` graceful drain, file descriptors), Docker multi-stage builds & Compose, Blue-Green/Rolling deploys, **Expand-and-Contract zero-downtime DB migrations**.
  - [x] **Observability (Metrics, Logs, Traces) & Scaling:** Prometheus RED metrics, Structured Logs (`structlog` + correlation IDs), Distributed Traces (OpenTelemetry), Sentry, horizontal scaling & backpressure.
- [x] **4. Collaborative System Design (5 Upcoming Ruit Challenges)**
  - [x] **Challenge 1:** Proactive Breakage Detection & Self-Healing Marketplace Integrations.
  - [x] **Challenge 2:** Multi-Marketplace Real-Time Inventory Sync & Double-Sell Prevention.
  - [x] **Challenge 3:** Plug-and-Play Marketplace Connector Engine (Official APIs, Reverse-Engineered APIs, and Browser/Extension Channels).
  - [x] **Challenge 4:** AI-Powered Cross-Marketplace Product Listing Normalizer & Category/Attribute Mapper.
  - [x] **Challenge 5:** Hybrid Chrome Extension + Cloud Worker Execution Architecture.

---

## 4. Workspace Architecture

```text
ruit-ai-engineer/
├── resources/                                  # [READ-ONLY — NEVER MODIFY]
│   ├── about the company.md
│   ├── cv-simin-shoeibi-fullstack-web-developer.pdf
│   ├── first emails.md
│   ├── job ad on bebee - Senior Backend Engineer, Integrations (Python) _ ruit _ LinkedIn.pdf
│   └── job ad on linkedin - Senior Backend Engineer, Integrations (Python) _ ruit _ LinkedIn.pdf
├── ai-assitant-analysis/                       # [META & CONTROL PLANE]
│   └── the-context-of-the-project/
│       ├── ai-state.md                         # This file: Live state, tracker & context
│       └── master-prompt.md                    # Master prompt driving the 10-hour prep curriculum
└── interview-preparation/                      # [COMPLETE 10-HOUR STUDY & PRACTICE KIT]
    ├── README.md                               # Master navigation index
    ├── 00-roadmap-and-quick-sheets/            # 10-hour schedule, TS->Python bridge, Euromed train sheet
    ├── 01-ai-workflow-and-live-task/           # Laptop demo script, 20-min playbook, live-task-sandbox/
    ├── 02-python-and-django-deep-dive/         # GIL, Async Django, Generators, Typing/Pydantic + python-django-labs/
    ├── 03-backend-fundamentals-cheatsheet/     # Celery/Redis, SQL/Locks, Python vs Go vs Rust + fundamentals-labs/
    ├── 04-integrations-reverse-eng-browsers/   # HTTP/TLS/JA3, API reverse-eng, Playwright/Chrome Ext, DevOps/Observability
    ├── 05-system-design-whiteboard/            # Collaborative whiteboard playbook + 5 Ruit system design challenges
    └── 06-culture-lunch-and-storytelling/      # Simin's 3 signature stories + team lunch playbook & questions
```

---

## 5. Mandatory AI Operational Rules (Source Priority, State & Git Discipline)

1. **Read-Only `resources/`:** Never modify, rename, or delete any file inside `resources/`.
2. **Source Priority Rule (Email Cheat Sheet First):** Prioritize the information in `resources/first emails.md` about the interview over any other information in `resources/`. Do NOT bring anything from the job ads in `resources/` that is not present at all in the email cheat sheet—only include job-ad details when they are directly related to the email cheat sheet topics (e.g., API integrations & reverse-engineering from network traffic, observability/catching breakage before sellers notice, Python/Django, AI agent workflows, and Ruit's upcoming marketplace challenges).
3. **State Synchronization:** Update this file (`ai-state.md`) after every completed step, module, or code lab.
4. **Atomic Local Git Commits After Every Change:**
   - This workspace is tracked in a local Git repository (`.git`).
   - **After every single logical change** (updating context/state files, generating a study guide, creating or testing a code lab), the AI Assistant **MUST** immediately stage the changes and create a clean, descriptive local commit (`git add -A && git commit -m "..."`).
   - Never leave uncommitted changes dangling at the end of a turn or module.

---

## 6. 10-Hour Study Plan & Progress Tracker

| Hour Block | Module | Focus Area | Target Folder | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Hours 1.0 – 2.0** | **Module 1: Live AI Setup & Agentic Workflow** | Configure laptop showcase, parallel agent sessions, custom skills/rules, and practice a 20-min live AI Python integration task. | `interview-preparation/01-ai-workflow-and-live-task/` | `[x] Completed` |
| **Hours 2.0 – 4.0** | **Module 2: Python & Django Internals + Code Labs** | GIL, Async Django (ASGI/ORM), Generators, Type Hints, Pydantic v2, Mypy/Ruff, plus TS-to-Python mental mapping. | `interview-preparation/02-python-and-django-deep-dive/` | `[x] Completed` |
| **Hours 4.0 – 6.0** | **Module 3: Backend Fundamentals Part 1 (Data, Async, Queues, Errors)** | Concurrency, JSON validation, Django ORM & SQL locking, Celery & Redis internals, Error handling (Python vs Go vs Rust), DB & Cache + runnable lab. | `interview-preparation/03-backend-fundamentals-cheatsheet/` | `[x] Completed` |
| **Hours 6.0 – 8.0** | **Module 4: Backend Fundamentals Part 2 (Reverse Eng, TLS, Browsers, DevOps, Observability)** | Rebuilding APIs from app traffic (`mitmproxy`/HAR), HTTP/2/3, WebSockets, TLS/JA3 fingerprinting, keeping integrations alive, Playwright & Chrome Extensions, Docker/Zero-Downtime, Observability. | `interview-preparation/04-integrations-reverse-eng-browsers/` | `[x] Completed` |
| **Hours 8.0 – 9.5** | **Module 5: Ruit System Design Whiteboard Mastery** | Collaborative whiteboard framework + full architectures for the 5 core Ruit marketplace challenges. | `interview-preparation/05-system-design-whiteboard/` | `[x] Completed` |
| **Hours 9.5 – 10.0** | **Module 6: Story Bank, Team Lunch & Final Mock Drill** | Pitching Dadroit (630K), 150-site crawler, and QueryLaw; team lunch playbook & questions for Luis and the team; Euromed train rapid review sheet. | `interview-preparation/06-culture-lunch-and-storytelling/` | `[x] Completed` |

---

## 7. Session Change Log

- **2026-11-02 (Sessions 1–3):**
  - Read `resources/` files (read-only), initialized `ai-state.md` and `master-prompt.md`, initialized local Git repository (`git init`), and enforced the Email-First Source Priority Rule and Atomic Git Commit Rule.
- **2026-11-02 (Sessions 4–10):**
  - Implemented Modules 0 through 6 inside `interview-preparation/`, configured `.venv` (`pydantic`, `httpx`, `pytest`, `ruff`, `mypy`), and committed each module atomically to Git.
- **2026-11-02 (Session 11 — Comprehensive Review & Polish):**
  - Audited all files from scratch to remove any job-ad details not directly tied to Luis's email cheat sheet.
  - Added runnable `fundamentals-labs/test_concurrency_locks_and_errors.py` in Module 3 and verified 100% pass across `pytest`, `ruff check`, and `mypy`.
