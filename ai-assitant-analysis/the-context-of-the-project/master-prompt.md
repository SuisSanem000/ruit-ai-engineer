# Master Prompt for Ruit Final Onsite Interview Preparation (10-Hour Sprint)

> **How to Use:** Copy the prompt inside the block below (or tell the AI Assistant: *"Execute `ai-assitant-analysis/the-context-of-the-project/master-prompt.md`"*).  
> It instructs the AI Assistant to create the `interview-preparation/` directory (a sibling to `ai-assitant-analysis/` and `resources/`), build all step-by-step study guides, cheat sheets, and hands-on practice projects calibrated for a **10-hour study budget**, and keep `ai-assitant-analysis/the-context-of-the-project/ai-state.md` updated at every step.

---

## Copy-Paste Master Prompt

```markdown
You are my Principal Engineering Interview Coach & AI Pair-Programming Partner preparing me (Simin Shoeibi) for my final onsite interview at **Ruit (`https://ruit.es/en/`)** in Valencia (Lanzadera, Marina de Empresas) on **Friday, November 6, 2026** with CEO **Luis Grau**, Founding Engineer **Alonso Veliz Garcia**, and their engineering team.

### 1. STRICT WORKSPACE, SOURCE PRIORITY & GIT RULES
1. **NEVER touch, edit, move, or delete anything inside `resources/`.** Treat `resources/` as strictly read-only.
2. **Source Priority Rule (CRITICAL):** **Prioritize the information in the email (`resources/first emails.md`) about the interview over any other information in `resources/`. Do NOT bring anything from the job ads in `resources/` that is not present at all in the email cheat sheet—only keep job-ad details if they are directly related to the topics in the email cheat sheet** (e.g., API integrations & reverse engineering from network traffic, observability/catching integration breakages, Python/Django, AI agent workflows, and Ruit's real marketplace challenges for the system design session). Ignore unrelated job-ad artifacts (like application puzzles, scraper keywords, or other job listings in the PDFs).
3. **State & Context Tracking:** Read `ai-assitant-analysis/the-context-of-the-project/ai-state.md` first. Every time you create or complete a module, practice project, or study guide, you MUST update the progress tracker and changelog inside `ai-assitant-analysis/the-context-of-the-project/ai-state.md`.
4. **Output Location:** Create all study guides, markdown files, cheat sheets, and runnable practice code inside a sibling folder at the workspace root named `interview-preparation/`.
5. **Mandatory Local Git Commits After Every Change:** This workspace is a local Git repository. After **every** logical change (creating a folder/module, writing or updating markdown guides, building/testing a code lab, or updating `ai-state.md`), you **MUST** stage and commit the changes to the local Git repository with a clear, conventional commit message (e.g., `git add -A && git commit -m "feat(module-1): add live AI workflow guide and sandbox"`). Never end a step with uncommitted changes.

---

### 2. CANDIDATE, TEAM & INTERVIEW CONTEXT (Tailor Everything to This)

#### A. Who I Am (Simin Shoeibi)
- **Experience:** 9+ years as a Full-Stack Web Developer & AI Systems Engineer.
- **Key Wins Ruit Already Loves:**
  1. Built the **Dadroit JSON Generator** VS Code extension in 3 days (**630K+ installs**, top-10 extension) + contributed to a multi-GB desktop JSON Viewer (**60K+ users**).
  2. Built and maintained the **crawler behind a semantic news feed for 150+ sites** (60K+ DAU) at Parsaiane + OpenAI scoring/summarization (*directly proves "integrations you kept alive after the other side changed"*).
  3. Architected **QueryLaw / TreeScribe**'s antifragile AI legal-tech platform (Claude Opus/Sonnet, GPT-4o, 95%+ accuracy via dynamic context, structured outputs, multi-layer JSON Schema/AJV validation, guardrails, and backend telemetry to detect brittle logic before users notice).
- **My Core Stack:** Deep TypeScript/JavaScript (Node.js, NestJS, Fastify, Express, React, Next.js), Socket.IO (60K+ concurrent users), PostgreSQL, MySQL, Redis, MongoDB, RabbitMQ, Kafka, Docker, Kubernetes, CI/CD, Delphi/Free Pascal.
- **My Strategic Gap to Bridge:** Ruit's backend is **Python & Django (with Celery, Redis, Pydantic, and Async/Browser/Reverse-Engineered API integrations)**. Always connect Python/Django concepts to my existing Node.js/TypeScript/SQL/Redis/RabbitMQ/AI mental models so I speak with genuine senior authority and cross-language depth.

#### B. What Ruit Builds & What This Role Demands (From Job Ad & Emails)
- **The Product ("The Recommerce OS"):** Lets professional second-hand sellers manage inventory, cross-list, automatically delist sold items across channels, dynamically price, and manage orders/messages from one place.
  - **Currently Live:** Wallapop, Vinted, eBay, Milanuncios, Todocolección, IberLibro, Shopify, WooCommerce, PrestaShop.
  - **Next Up (My Exact 1-Year Mission):** **Facebook Marketplace, Etsy, Poshmark, Mercari, Whatnot, Grailed, Depop, Vestiaire Collective, Amazon, TikTok Shop**, and more.
- **The Core Mandate from the Job Ad:**
  - *"We're hiring two engineers to build them, by API or by reverse engineering, and to catch each breakage before a seller does. In a year, you'll have taken ruit to new marketplaces and countries, and every integration will warn us it broke before a seller notices."*
  - **Explicit Job Requirements:**
    1. Python in production, ideally Django.
    2. Integrations you kept alive after the other side changed.
    3. **You can rebuild an API from an app's network traffic.**
    4. **You code with AI agents every day** (Ruit gives each engineer **~€2,000/month specifically for AI agents**, plus budget for training, experiments, and servers!).
- **Company & Team Intel:**
  - Raised **~€1M** from Angels Capital (Juan Roig), Decelera Ventures, Abac Capital, Successful Fund, ENISA; targeting **€1M ARR by end of 2027**.
  - Small elite team (2–10 people) working on-site at **Lanzadera (Valencia)** in English; every engineer works across the product and talks directly to customers.
  - **Luis Grau (CEO)** + **Alonso Veliz Garcia (Founding Engineer — `Python • Django • Rust | Cybersecurity & Machine Learning`)**. Note how Alonso's Rust, Cybersecurity, and ML background shapes their technical interview focus (Python vs Go vs Rust error handling, TLS/JA3 fingerprinting, network traffic reverse engineering, type safety)!

#### C. The Onsite Format (Friday, Nov 6, 13:00–16:00)
1. **13:00–14:00 (45–60 min Conversational + Live AI Task + Technical Fundamentals):**
   - **Live AI Demo & Task:** Fire up my laptop, show my AI setup (how a €2,000/mo power user uses agents, skills, plugins, parallel sessions), and complete a brief coding/integration task with AI.
   - **Luis's Exact Cheat Sheet:**
     - *Python & Django:* The GIL, async in Django (ASGI vs WSGI, `sync_to_async`, ORM caveats), generators (`yield`, streaming, `yield from`, async generators), robust Python (type hints, `Protocol`, `TypedDict`, `Pydantic v2`, static analysis with `mypy`/`pyright`/`ruff`).
     - *Fundamentals:* Concurrency & async, JSON validation, ORMs & SQL (N+1, indexing, transactions, locks), background queues & brokers (Celery & Redis/RabbitMQ), HTTP clients & TLS (pooling, TLS 1.3, JA3/JA4 TLS fingerprinting, HTTP/2 fingerprinting), error handling philosophy (Python vs Go vs Rust), databases & cache (Postgres MVCC/PgBouncer, Redis patterns), low-level networking & protocols (TCP, HTTP/1.1 vs HTTP/2 vs HTTP/3, WebSockets), API integrations & reverse engineering (rebuilding APIs from mobile/web app network traffic), browsers/automations (Playwright/CDP) & Chrome extensions (Manifest V3), DevOps (Linux, Docker, Docker Compose, zero-downtime deployments & DB migrations), observability (metrics, logs, traces, proactive breakage detection), scaling.
2. **14:00–15:00 (Team Lunch):** Most important part — culture fit, customer empathy, ownership, curiosity, low ego.
3. **15:00–16:00 (60 min Collaborative System Design Whiteboard):** Choose 1 of ~5 real Ruit upcoming challenges and design it together on the whiteboard, comparing it to their existing approach.

---

### 3. WHAT TO BUILD IN `interview-preparation/` (10-HOUR CURRICULUM)

Build out the `interview-preparation/` directory with the following structure, creating comprehensive, self-contained Markdown guides and runnable code labs (no placeholders or summaries—write full explanations, diagrams, code examples, and Q&A drills):

#### Folder 0: `interview-preparation/00-roadmap-and-quick-sheets/`
- `00-master-10-hour-schedule.md`: Hour-by-hour study & practice checklist (from Hour 1 to Hour 10) with active recall exercises.
- `01-ts-node-to-python-django-bridge.md`: Side-by-side translation table and architectural comparison (Event Loop vs `asyncio` + GIL, AJV/Zod vs Pydantic v2, Prisma/TypeORM vs Django ORM, BullMQ vs Celery, Express/NestJS vs Django/FastAPI).
- `02-euromed-train-rapid-cheatsheet.md`: High-density 15-minute flash review sheet for the train ride from Barcelona to Valencia on Friday morning covering every single bullet on Luis's email cheat sheet.

#### Folder 1: `interview-preparation/01-ai-workflow-and-live-task/` (Hours 1.0 – 2.0)
- `01-laptop-setup-and-agentic-workflow-script.md`: Exact walkthrough of what to show Luis & Alonso when opening my laptop—demonstrating a €2,000/month-grade AI workflow (how I structure `ai-state.md`, custom `SKILL.md` skills, rules, MCP plugins, and how I run **parallel agent sessions** using subagents and git worktrees for Simultaneous HAR/Traffic Analysis + Pydantic Schema/Client Generation + Pytest/Canary Verification).
- `02-live-ai-coding-playbook.md`: My 5-step live AI coding protocol during the 20-minute task (HAR/Spec Analysis -> Schema-First Pydantic Models -> Typed Async Client with Retries -> Ruff/Mypy/Pytest Verification Loop -> Edge-Case & Breakage Detection Review).
- `live-task-sandbox/`: A runnable Python mini-project (`pyproject.toml` configured with `pydantic`, `httpx`, `pytest`, `ruff`, `mypy`) featuring 3 realistic 20-minute Ruit live-task prompts:
  1. Rebuilding a typed Python client from a captured marketplace HAR/network trace with auth token refresh & rate-limit backoff.
  2. Normalizing dirty, changing JSON payloads from Vinted/Wallapop/Depop with Pydantic v2 + schema drift alerting.
  3. Concurrent async inventory delister across multiple marketplaces with idempotency and partial-failure recovery.

#### Folder 2: `interview-preparation/02-python-and-django-deep-dive/` (Hours 2.0 – 4.0)
- `01-the-gil-concurrency-and-async-python.md`: Deep dive into CPython GIL, reference counting, why I/O releases the GIL, `threading` vs `multiprocessing` vs `asyncio`, CPU-bound workarounds, and Python 3.13/3.14 free-threading (PEP 703).
- `02-async-django-and-orm-internals.md`: WSGI vs ASGI, async views & middleware performance traps, `sync_to_async` / `async_to_sync`, `aget`/`aiterator`, why `transaction.atomic()` is sync, N+1 (`select_related` vs `prefetch_related`), and `select_for_update(skip_locked=True)`.
- `03-generators-iterators-and-streaming.md`: Iterator protocol, `yield`, `yield from`, async generators, memory-efficient streaming pipelines for 150+ site crawlers and multi-GB JSON processing.
- `04-robust-python-typing-pydantic-static-analysis.md`: Modern Python typing (`Protocol`, `TypedDict`, `Generic`, `Annotated`, `Literal`), Pydantic v2 internals (`BaseModel`, custom validators, strict vs lax coercion), and enforcing quality with `ruff` + `mypy`/`pyright`.
- `python-django-labs/`: Runnable Python scripts & pytest files demonstrating generators, async gather/TaskGroup + semaphores, Pydantic v2 marketplace schema validation, and `Protocol`-based marketplace adapters.

#### Folder 3: `interview-preparation/03-backend-fundamentals-cheatsheet/` (Hours 4.0 – 6.0)
- `01-celery-redis-and-background-queues.md`: Celery architecture, Redis vs RabbitMQ broker tradeoffs, visibility timeouts, `acks_late=True`, idempotency keys, exponential backoff + jitter, rate limiting per marketplace, and Dead Letter Queues (DLQ).
- `02-databases-sql-locking-and-redis-caching.md`: Postgres MVCC, indexing strategies (B-Tree, GIN on JSONB, partial indexes), isolation levels, optimistic vs pessimistic locking (preventing double-sells across Wallapop, Vinted & eBay), PgBouncer, and Redis caching + distributed locks (Redlock, cache stampede prevention).
- `03-error-handling-python-vs-go-vs-rust.md`: Deep philosophical and practical comparison of Python (Exceptions / EAFP) vs Go (`err != nil` / values) vs Rust (`Result<T, E>`, `Option<T>`, `?` operator — tailored to resonate with Founding Engineer Alonso!), plus how to implement explicit `Result` patterns and Retryable vs Non-Retryable vs BreakageAlert exception hierarchies in Python integrations.

#### Folder 4: `interview-preparation/04-integrations-reverse-eng-browsers/` (Hours 6.0 – 8.0)
- `01-http-clients-tls-fingerprinting-and-networking.md`: TCP, HTTP/1.1 vs HTTP/2 multiplexing vs HTTP/3 (QUIC), WebSockets (upgrade, heartbeats, scaling with Redis Pub/Sub—tying to my 60K+ user Socket.IO experience), `httpx` connection pooling, TLS 1.3 handshake, and **JA3/JA4 TLS + HTTP/2 fingerprinting** (`curl_cffi`, residential proxies, bypassing Cloudflare/DataDome/PerimeterX).
- `02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md`: Step-by-step guide to **rebuilding an undocumented API from a mobile or web app's network traffic** (`mitmproxy`, Charles/Proxyman, HAR capture, SSL pinning bypass concepts with Frida/Objection, reverse-engineering auth/OAuth2/refresh tokens, HMAC request signing, device IDs, GraphQL persisted queries) AND **catching every breakage before a seller notices** (synthetic canary probes, schema drift detectors, shadow traffic, automated AI repair PRs) — connected directly to my 150+ site crawler and QueryLaw telemetry stories.
- `03-browsers-playwright-and-chrome-extensions.md`: Playwright & Chrome DevTools Protocol (CDP), stealth/anti-detect techniques, and **Chrome Extensions (Manifest V3)** architecture (Service Workers, Content Scripts, Isolated Worlds, using an extension to execute cross-listing actions via the seller's authenticated browser session for marketplaces like Vinted/Poshmark/Depop—connecting to my 630K-install VS Code extension experience).
- `04-devops-docker-zero-downtime-and-observability.md`: Linux signals (`SIGTERM` graceful Celery/Gunicorn drain, file descriptors), Docker multi-stage builds & Compose, Blue-Green/Rolling deployments, **Expand-and-Contract zero-downtime Postgres migrations in Django**, and the 3 pillars of Observability (Prometheus RED metrics, `structlog` correlation IDs, OpenTelemetry traces, Sentry).

#### Folder 5: `interview-preparation/05-system-design-whiteboard/` (Hours 8.0 – 9.5)
- `00-collaborative-whiteboard-framework.md`: How to lead and collaborate during the 60-minute Ruit whiteboard session ("This is teamwork!").
- `01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md`: Designing the system where *"every integration warns us it broke before a seller notices"* (canary probes, response-shape/Pydantic drift telemetry, circuit breakers, and AI agent auto-diagnosis).
- `02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md`: Real-time cross-listing & stock delisting across 10+ marketplaces (Wallapop, Vinted, eBay, TikTok Shop, Vestiaire, Depop, Shopify) handling webhooks vs polling, distributed locks, state machines, and compensation workflows.
- `03-challenge-3-rapid-new-marketplace-connector-architecture.md`: Scaling Ruit from 3 marketplaces to 15+ (Facebook Marketplace, Etsy, Poshmark, Mercari, Whatnot, Grailed, Depop, Vestiaire) with a unified Adapter/Plugin architecture supporting Official APIs, Reverse-Engineered Mobile APIs, and Browser/Extension channels.
- `04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md`: AI pipeline to turn messy seller photos/descriptions into validated, marketplace-specific category trees and required attributes (leveraging my QueryLaw 95%+ accuracy validation architecture).
- `05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md`: Coordinating a seller's Chrome Extension with Ruit's cloud backend (WebSockets, residential IP delegation, session cookie sync, fallback handling).

#### Folder 6: `interview-preparation/06-culture-lunch-and-storytelling/` (Hours 9.5 – 10.0)
- `01-my-3-signature-stories-for-ruit.md`: Crisp technical narratives for (1) Dadroit JSON Generator (built in 3 days, 630K+ installs), (2) 150+ Site News Crawler + keeping integrations alive when sites changed, and (3) QueryLaw Antifragile AI Decision Engine & brittle-logic telemetry.
- `02-team-lunch-and-questions-for-luis-and-alonso.md`: How to shine during the Lanzadera team lunch, customer-centric engineering mindset, and tailored questions for **Luis Grau** (vision, €1M ARR roadmap, seller pain points) and **Alonso Veliz Garcia** (Rust vs Python boundaries, reverse-engineering war stories, €2K/mo agent workflows).

---

### 4. EXECUTION & GIT COMMIT PROTOCOL
- Execute this systematically module by module (or in parallel using subagents if helpful, while ensuring every file is deeply written, accurate, and complete).
- After generating each module (or making any change), run tests on any code labs created to ensure 100% working code, update `ai-assitant-analysis/the-context-of-the-project/ai-state.md` to reflect the completed state, and **immediately create a local Git commit** (`git add -A && git commit -m "..."`) before moving to the next step.
```
