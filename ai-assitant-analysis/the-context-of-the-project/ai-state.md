# Ruit Final Interview Preparation — Project Context & AI State Tracker

> **Last Updated:** 2026-11-02 (Updated with `about the company.md`, LinkedIn Job Ad PDF, and BeBee Job Ad PDF)  
> **Target Interview Date:** Friday, November 6, 2026 (12:45 CET – 16:00 CET)  
> **Location:** Ruit Offices @ Lanzadera (Marina de Empresas, by the beach), Valencia, Spain  
> **Current Phase:** Phase 0 — Context Enriched & Ready to Generate `interview-preparation/` Modules  
> **Total Prep Time Budget:** Up to 10 Hours (Structured into focused, high-ROI blocks)

---

## 1. Executive Context: Company, Product, Team & Role

### 1.1 About Ruit (`https://ruit.es/en/` — `RUIT COMPARATOR S.L.`)
- **Mission & Vision:** Make second-hand the first way everyone in Europe shops ("Millions of products sold again instead of made new, millions of euros for the people who sell them, and a world a bit better than we found it").
- **The Product (The Recommerce OS for Professional Sellers):**
  - Centralizes inventory, cross-listing, automated stock delisting (preventing double-sells when an item sells on one channel), dynamic pricing, customer messaging, order management, and analytics from one single platform.
  - **Currently Connected Channels:** Wallapop, Vinted, eBay, Milanuncios, Todocolección, IberLibro, plus e-commerce store integrations (Shopify, WooCommerce, PrestaShop).
  - **Next 12-Month Marketplace Roadmap (The Exact Scope of This Hire):** **Facebook Marketplace, Etsy, Poshmark, Mercari, Whatnot, Grailed, Depop, Vestiaire Collective, Amazon, TikTok Shop**, and more.
- **Traction, Funding & Goals:**
  - Raised **close to €1M (~€880K round)** backed by **Angels Capital** (Juan Roig's investment vehicle at Marina de Empresas), **Decelera Ventures**, **Abac Capital (Abac Nest)**, **Successful Fund**, and **ENISA**.
  - **North Star Goal:** Reaching **€1M in ARR by the end of 2027**.
- **Culture, Perks & Working Style:**
  - **Small, elite team (2–10 employees)** working in English on-site 5 days/week at **Lanzadera, Valencia** (ranked 19th among Europe's startup hubs in the 2026 Financial Times & Statista ranking).
  - **Customer-centric engineering:** Every engineer works across the product and talks directly to customers; Simin's core focus is **integrations**.
  - **AI-First Engineering Culture:** Ruit provides **~€2,000/month per engineer specifically for AI agents**, plus a budget for training, experiments, and servers.
  - **Compensation & Speed:** Pay at the **75th percentile of the market**; final hiring decision within **48 hours** of the Valencia onsite.
  - **Team Rituals:** Free team lunch together every Thursday; games on Fridays.

### 1.2 Key People You Will Meet
1. **Luis Grau (CEO & Founder, `luis.grau@ruit.es`):** Reviews every application and form personally. Cares deeply about shipping velocity, ownership, deep engineering fundamentals, and practical AI-agent workflows.
2. **Alonso Veliz Garcia (Founding Engineer @ Ruit):** Headline: **`Python • Django • Rust | Cybersecurity & Machine Learning`** (and a 1st-degree LinkedIn connection of Simin).
   - *Strategic Insight:* Alonso's background in **Python, Django, Rust, Cybersecurity, and ML** directly explains why the interview rubric emphasizes **Python vs Go vs Rust error handling**, **rebuilding APIs from network traffic**, **TLS/low-level networking**, **reverse engineering**, and **type safety/static analysis**!

### 1.3 Target Role & Core 1-Year Mandate
- **Role:** **Senior Backend Engineer, Integrations (Python)** (also considered across AI/Full-Stack engineering per Luis).
- **The 1-Year Mandate (Directly from Job Ad):**
  > *"We're hiring two engineers to build them [Facebook Marketplace, Etsy, Poshmark, Mercari, Whatnot, Grailed, Depop, Vestiaire Collective, Amazon, TikTok Shop...], by API or by reverse engineering, and to catch each breakage before a seller does. In a year, you'll have taken ruit to new marketplaces and countries, and every integration will warn us it broke before a seller notices."*
- **The 6 Explicit Job Requirements:**
  1. **Python in production, ideally Django.**
  2. **Integrations you kept alive after the other side changed.**
  3. **You can rebuild an API from an app's network traffic.**
  4. **You code with AI agents every day.**
  5. **Working English** (the team works in English).
  6. **Legal work authorization in Spain** (already met).

---

## 2. Candidate Profile & Strategic Alignment (Simin Shoeibi)

### 2.1 Why Simin Is a High-Signal Match for Ruit's Exact Needs
1. **"Integrations you kept alive after the other side changed":**
   - Built and maintained the **crawler behind a semantic news app for 150+ sites** (60K+ DAU) at Parsaiane—dealing with heterogeneous DOMs/APIs, rate limits, and silent upstream changes.
   - Built **backend telemetry for large-scale AI validation at QueryLaw**, including real-time monitoring and failure feedback to detect brittle logic before end-users noticed.
2. **"Shipping things people rely on":**
   - Built the **Dadroit JSON Generator** VS Code extension in 3 days (**630K+ installs**, top-10 extension) and contributed to a high-performance multi-GB desktop JSON Viewer (**60K+ users**).
3. **"You code with AI agents every day" & AI Systems Engineering:**
   - Architected QueryLaw/TreeScribe's antifragile AI decision system (Claude Opus/Sonnet, GPT-4o, 95%+ accuracy, dynamic context windows, multi-layer JSON Schema/AJV validation, guardrails, and human-in-the-loop comparison tooling).
4. **High-Load Backend & Real-Time Architecture:**
   - 9+ years experience; scaled PERN/MERN systems to **60K+ concurrent users** with Node.js (NestJS, Fastify, Express), **Socket.IO / WebSockets**, PostgreSQL, Redis, RabbitMQ, Kafka, Docker, and Kubernetes.

### 2.2 The Key Technical Bridge to Master (TS/Node.js $\rightarrow$ Python/Django + Rust Mindset)
- **Bridging Node.js/TypeScript to Python/Django:** Map Simin's deep expertise in Event Loop concurrency, AJV/Zod, Prisma/TypeORM, and BullMQ/RabbitMQ directly to **CPython's GIL + `asyncio`**, **Pydantic v2 + Python Type Hints (`Protocol`, `TypedDict`)**, **Django ORM (sync vs async ASGI)**, and **Celery + Redis**.
- **Connecting with Alonso's Rust & Cybersecurity Mindset:** Emphasize strict boundary validation (Pydantic v2), explicit error taxonomies (`Result<T, E>` philosophy in Python), defensive network engineering (TLS/JA3 fingerprinting, mitmproxy, mobile API traffic reconstruction), and proactive canary monitoring.

---

## 3. Final Onsite Schedule & Exact Evaluation Rubric (Friday, Nov 6)

| Time | Session | Format & What They Evaluate |
| :--- | :--- | :--- |
| **12:45 – 13:00** | **Arrival & Office Tour** | Arrive at Lanzadera (Marina de Empresas, Valencia). Sister waits comfortably at the office. |
| **13:00 – 14:00** | **Interview 1: Live AI Task + Engineering Fundamentals (45–60 min)** | **Part A:** Fire up laptop, show AI/dev setup, complete a brief live task with AI.<br>**Part B:** Deep conversational dive into Luis's literal evaluation cheat sheet (Fundamentals + Python/Django + AI workflows). |
| **14:00 – 15:00** | **Team Lunch (60 min)** | *"This is the most important part. It's on the house."* Culture fit, customer empathy, product ownership, curiosity, rapport with Luis, Alonso, and team. |
| **15:00 – 16:00** | **Interview 2: System Design Whiteboard (60 min)** | Choose **1 of ~5 real Ruit challenges** for the coming months. Design it collaboratively on the whiteboard and compare with Ruit's existing approach. *"This is teamwork!"* |

### 3.1 Luis's Literal Evaluation Cheat Sheet + Job Ad Core Requirements (Master Checklist)

- [ ] **1. Live Laptop Setup & €2,000/mo AI Agent Workflow**
  - [ ] Showing IDE/agent setup (Antigravity / Claude Code / Cursor / VS Code).
  - [ ] Using **Agents, Skills (`SKILL.md`), Plugins/MCPs, Rules, and Context/State files (`ai-state.md`)**.
  - [ ] Running **sessions in parallel** (subagents, git worktrees, parallel traffic analysis + Pydantic modeling + pytest generation).
  - [ ] Completing a brief live coding/integration task with AI cleanly and verifying it with static analysis (`ruff`, `mypy`) and tests (`pytest`).
- [ ] **2. Python & Django Deep Dive**
  - [ ] **The GIL (Global Interpreter Lock):** CPython reference counting, thread safety, CPU-bound vs I/O-bound, `threading` vs `multiprocessing` vs `asyncio`, Python 3.13/3.14 free-threading (PEP 703).
  - [ ] **Async in Django:** WSGI vs ASGI, `async def` views, `sync_to_async` & `async_to_sync`, Django ORM async methods (`aget`, `aiterator`) vs sync-only parts (`transaction.atomic`), connection pooling.
  - [ ] **Generators:** `yield`, iterator protocol, lazy evaluation, streaming pipelines, `yield from`, async generators (`async for`), memory efficiency in large crawls/ETL.
  - [ ] **Robust Python:** Type hints (`typing`, `Protocol`, `TypedDict`, `Generic`, `Annotated`), runtime validation (`Pydantic v2`), static analysis (`mypy`, `pyright`, `ruff`).
- [ ] **3. Core Backend & Integration Fundamentals**
  - [ ] **Concurrency & Async:** Event loops, threads, processes, race conditions, distributed locks, idempotency.
  - [ ] **JSON Validation:** Schema enforcement at boundaries (Pydantic v2 / JSON Schema / AJV), handling dirty/evolving 3rd-party marketplace JSON, schema drift detection.
  - [ ] **ORMs & SQL:** Query optimization, N+1 (`select_related` vs `prefetch_related`), indexing (B-Tree, GIN, partial, composite), transactions, isolation levels, `SELECT ... FOR UPDATE SKIP LOCKED`.
  - [ ] **Background Queues & Brokers (Celery & Redis / RabbitMQ):** Task lifecycle, acks (`acks_late`), visibility timeouts, retries + backoff/jitter, idempotency, rate-limiting queues per marketplace, Dead Letter Queues (DLQ).
  - [ ] **HTTP Clients & TLS:** Connection pooling (`httpx`/`requests.Session`), timeouts, TLS 1.2/1.3 handshake, **TLS fingerprinting (JA3/JA4) & HTTP/2 fingerprinting** in anti-bot evasion (`curl_cffi`).
  - [ ] **Error Handling Philosophy (Python vs Go vs Rust):** Exceptions (EAFP) vs Errors-as-Values (`if err != nil`) vs Algebraic `Result<T, E>` / `Option<T>` (connecting with Alonso's Rust background!), and designing resilient integration error taxonomies.
  - [ ] **Databases & Cache:** Postgres MVCC/VACUUM/PgBouncer, Redis data structures & caching patterns (Cache-Aside, stampede protection, TTL jitter, distributed locks).
  - [ ] **Low-Level Networking & Protocols:** TCP/IP, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), WebSockets (upgrade, heartbeats, scaling via Redis Pub/Sub), Webhooks vs Polling.
  - [ ] **API Integrations & Rebuilding APIs from App Network Traffic:** Inspecting web & mobile app traffic (`mitmproxy`, Charles/Proxyman, Chrome DevTools, HAR files, SSL pinning concepts, Android/iOS private APIs), reverse-engineering auth flows (OAuth2, JWT refresh rotation, HMAC request signing, CSRF, device fingerprints), proxy rotation, rate limits.
  - [ ] **Keeping Integrations Alive & Proactive Breakage Detection:** Canary health checks, contract/schema drift tests, shadow runs, anomaly alerts on HTTP status/payload shape so *"every integration warns us it broke before a seller notices"*.
  - [ ] **Browsers, Automations & Chrome Extensions:** Playwright/CDP, headless anti-detect, Chrome Extensions (Manifest V3, content scripts, background service workers, piggybacking on authenticated seller sessions for marketplaces like Vinted/Wallapop/Poshmark).
  - [ ] **DevOps & Zero-Downtime Deployments:** Linux fundamentals (`SIGTERM` graceful drain, file descriptors), Docker & Docker Compose, Blue-Green/Rolling deploys, **Expand-and-Contract zero-downtime DB migrations**.
  - [ ] **Observability & Scaling:** Metrics (Prometheus/RED), Structured Logs (`structlog` + correlation IDs), Distributed Traces (OpenTelemetry), Sentry, horizontal scaling & backpressure.
- [ ] **4. Collaborative System Design (5 High-Probability Ruit Challenges)**
  - [ ] **Challenge 1:** Proactive Breakage Detection & Self-Healing Marketplace Integrations (*"every integration will warn us it broke before a seller notices"*).
  - [ ] **Challenge 2:** Multi-Marketplace Real-Time Inventory Sync & Double-Sell Prevention across 10+ channels (Wallapop, Vinted, eBay, TikTok Shop, Vestiaire, Depop, Shopify).
  - [ ] **Challenge 3:** Plug-and-Play Marketplace Connector Engine (Supporting Official APIs, Reverse-Engineered Mobile/Web APIs, and Browser/Extension Automation).
  - [ ] **Challenge 4:** AI-Powered Cross-Marketplace Product Listing Normalizer, Category Mapper & Dynamic Pricing Engine.
  - [ ] **Challenge 5:** Hybrid Chrome Extension + Cloud Worker Architecture for Authenticated Seller Sessions & Anti-Bot Evasion.

---

## 4. Planned Workspace Architecture

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
│       └── master-prompt.md                    # Master prompt to drive the 10-hour prep generation
└── interview-preparation/                      # [TO BE GENERATED IN NEXT PHASE]
    ├── 00-roadmap-and-quick-sheets/            # 10-hour schedule, TS->Python bridge, Euromed train sheet
    ├── 01-ai-workflow-and-live-task/           # Laptop demo setup (€2K/mo agent workflow), parallel sessions, live task lab
    ├── 02-python-and-django-deep-dive/         # GIL, Async Django, Generators, Typing/Pydantic + runnable code
    ├── 03-backend-fundamentals-cheatsheet/     # Celery/Redis, SQL/Locks, Python vs Go vs Rust error handling
    ├── 04-integrations-reverse-eng-browsers/   # Rebuilding APIs from app traffic, TLS/JA3, Playwright, Chrome Ext, DevOps, Observability
    ├── 05-system-design-whiteboard/            # 5 Ruit system design challenges + collaborative whiteboard playbook
    └── 06-culture-lunch-and-storytelling/      # Simin's 3 signature stories + questions for Luis & Alonso
```

---

## 5. Mandatory AI Operational Rules (Source Priority, State & Git Discipline)

1. **Read-Only `resources/`:** Never modify, rename, or delete any file inside `resources/`.
2. **Source Priority Rule (Email Cheat Sheet First):** Prioritize the information in `resources/first emails.md` about the interview over any other information in `resources/`. Do NOT bring anything from the job ads in `resources/` that is not present at all in the email cheat sheet—only include job-ad details when they are directly related to the email cheat sheet topics (e.g., API integrations & reverse-engineering from network traffic, observability/catching breakage before sellers notice, Python/Django, AI agent workflows, and Ruit's upcoming marketplace challenges).
3. **State Synchronization:** Update this file (`ai-state.md`) after every completed step, module, or code lab.
4. **Atomic Local Git Commits After Every Change:**
   - This workspace is tracked in a local Git repository (`.git`).
   - **After every single logical change** (updating context/state files, generating a study guide, creating or testing a code lab), the AI Assistant **MUST** immediately stage the changes and create a clean, descriptive local commit (e.g., `git add -A && git commit -m "feat(prep): ..."`).
   - Never leave uncommitted changes dangling at the end of a turn or module.

---

## 6. 10-Hour Study Plan & Progress Tracker

> **Instructions for AI Assistant:** Whenever a module or practice project is created, updated, or completed with Simin, update the `Status` column below (`[ ] Pending` $\rightarrow$ `[~] In Progress` $\rightarrow$ `[x] Completed`), log the change in Section 7, and **commit all changes to the local Git repository**.

| Hour Block | Module | Focus Area | Target Folder | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Hours 1.0 – 2.0** | **Module 1: Live AI Setup & Power-Agent Workflow** | Configure laptop showcase, parallel agent sessions, custom skills/rules, and practice a 20-min live AI Python integration task (rebuilding/validating a marketplace API client). | `interview-preparation/01-ai-workflow-and-live-task/` | `[x] Completed` |
| **Hours 2.0 – 4.0** | **Module 2: Python & Django Internals + Code Labs** | GIL, Async Django (ASGI/ORM), Generators, Type Hints, Pydantic v2, Mypy/Ruff, plus TS-to-Python mental mapping. | `interview-preparation/02-python-and-django-deep-dive/` | `[x] Completed` |
| **Hours 4.0 – 6.0** | **Module 3: Backend Fundamentals Part 1 (Data, Async, Queues, Errors)** | Concurrency, JSON validation, Django ORM & SQL locking, Celery & Redis internals, Error handling (Python vs Go vs Rust), DB & Cache. | `interview-preparation/03-backend-fundamentals-cheatsheet/` | `[x] Completed` |
| **Hours 6.0 – 8.0** | **Module 4: Backend Fundamentals Part 2 (Reverse Eng, TLS, Browsers, DevOps, Breakage Detection)** | Rebuilding APIs from app traffic (`mitmproxy`/HAR), HTTP/2/3, WebSockets, TLS/JA3 fingerprinting, keeping integrations alive, Playwright & Chrome Extensions, Docker/Zero-Downtime, Observability. | `interview-preparation/04-integrations-reverse-eng-browsers/` | `[x] Completed` |
| **Hours 8.0 – 9.5** | **Module 5: Ruit System Design Whiteboard Mastery** | Collaborative whiteboard framework + full architectures for the 5 core Ruit marketplace challenges (including proactive breakage detection & new marketplace expansion). | `interview-preparation/05-system-design-whiteboard/` | `[x] Completed` |
| **Hours 9.5 – 10.0** | **Module 6: Story Bank, Team Lunch & Final Mock Drill** | Pitching Dadroit (630K), 150-site crawler, and QueryLaw; connecting with Luis Grau & Alonso Veliz Garcia; Euromed train rapid review sheet. | `interview-preparation/06-culture-lunch-and-storytelling/` | `[ ] Pending` |

---

## 7. Session Change Log

- **2026-11-02 (Session 1):**
  - Read `resources/first emails.md` and `resources/cv-simin-shoeibi-fullstack-web-developer.pdf` in full detail (without modifying `resources/`).
  - Created `ai-assitant-analysis/the-context-of-the-project/ai-state.md` and `ai-assitant-analysis/the-context-of-the-project/master-prompt.md`.
- **2026-11-02 (Session 2 — Context Enrichment):**
  - Read newly added files in `resources/`: `about the company.md`, `job ad on linkedin - Senior Backend Engineer, Integrations (Python) _ ruit _ LinkedIn.pdf`, and `job ad on bebee - Senior Backend Engineer, Integrations (Python) _ ruit _ LinkedIn.pdf`.
  - Updated `ai-state.md` and `master-prompt.md` with:
    1. Ruit's current integrations (Wallapop, Vinted, eBay, Milanuncios, Todocolección, IberLibro, Shopify, WooCommerce, PrestaShop) and target roadmap (Facebook Marketplace, Etsy, Poshmark, Mercari, Whatnot, Grailed, Depop, Vestiaire Collective, Amazon, TikTok Shop).
    2. Key mandate: *"rebuild an API from an app's network traffic"*, *"integrations you kept alive after the other side changed"*, and *"every integration will warn us it broke before a seller notices"*.
    3. Founding Engineer profile: **Alonso Veliz Garcia** (`Python • Django • Rust | Cybersecurity & Machine Learning`), explaining the Rust error-handling, TLS/networking, and reverse-engineering focus.
    4. Ruit's €1M funding (Angels Capital, Decelera, Abac Capital, Successful Fund), €1M ARR by end of 2027 target, and **~€2,000/month per engineer AI agent budget**.
- **2026-11-02 (Session 3 — Local Git Repository & Atomic Commit Protocol):**
  - Initialized local Git repository in the workspace root (`git init`) with OS/Python build artifacts excluded via `.git/info/exclude`.
  - Updated `ai-state.md` and `master-prompt.md` to mandate atomic local Git commits after every single file/module change and prioritize the email cheat sheet over unrelated job-ad details.
- **2026-11-02 (Session 4 — Module 0 Completed):**
  - Created `interview-preparation/00-roadmap-and-quick-sheets/` with `00-master-10-hour-schedule.md`, `01-ts-node-to-python-django-bridge.md`, and `02-euromed-train-rapid-cheatsheet.md`.
- **2026-11-02 (Session 5 — Module 1 Completed):**
  - Created `interview-preparation/01-ai-workflow-and-live-task/` with `01-laptop-setup-and-agentic-workflow-script.md`, `02-live-ai-coding-playbook.md`, and the runnable `live-task-sandbox/` (`marketplace_connector.py`, `test_marketplace_connector.py`, `README.md`).
  - Configured `.venv` with `pydantic`, `httpx`, `pytest`, `ruff`, and `mypy`, and verified 5/5 passing tests in `0.26s`.
- **2026-11-02 (Session 6 — Module 2 Completed):**
  - Created `interview-preparation/02-python-and-django-deep-dive/` with `01-the-gil-concurrency-and-async-python.md`, `02-async-django-and-orm-internals.md`, `03-generators-iterators-and-streaming.md`, `04-robust-python-typing-pydantic-static-analysis.md`, and `python-django-labs/test_python_deep_dive_labs.py` (9/9 total tests passing + clean `ruff check`).
- **2026-11-02 (Session 7 — Module 3 Completed):**
  - Created `interview-preparation/03-backend-fundamentals-cheatsheet/` with `01-celery-redis-and-background-queues.md`, `02-databases-sql-locking-and-redis-caching.md`, and `03-error-handling-python-vs-go-vs-rust.md`.
- **2026-11-02 (Session 8 — Module 4 Completed):**
  - Created `interview-preparation/04-integrations-reverse-eng-browsers/` with `01-http-clients-tls-fingerprinting-and-networking.md`, `02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md`, `03-browsers-playwright-and-chrome-extensions.md`, and `04-devops-docker-zero-downtime-and-observability.md`.
- **2026-11-02 (Session 9 — Module 5 Completed):**
  - Created `interview-preparation/05-system-design-whiteboard/` with `00-collaborative-whiteboard-framework.md` and the 5 Ruit system design blueprints (`01` through `05`).
