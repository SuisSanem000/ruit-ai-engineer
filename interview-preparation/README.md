# Ruit Final Interview Preparation (10-Hour Master Guide)

> **Position Applying For:** **Senior Backend Engineer, Integrations (Python)**  
> *(Note: Luis confirmed in writing that you applied for multiple roles and are being considered for both **Senior Backend Engineer** and **Senior Full Stack Engineer, Integrations (Python) / AI Engineer** with this single process).*
>
> - **Candidate:** Simin Shoeibi
> - **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival, `13:00h–16:00h` interviews @ Lanzadera, Valencia)
> - **Company & Product Guide:** Read [COMPANY-AND-PRODUCT-GUIDE.md](./COMPANY-AND-PRODUCT-GUIDE.md) for full company background, product features, founding team, and funding.
> - **Main Source:** Luis Grau's email cheat sheet ([`docs/resources/first emails.md`](../docs/resources/first%20emails.md))
> - **AI Project Files:** [`ai-state.md`](../docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md) | [`master-prompt.md`](../docs/ai-assitant-analysis/the-context-of-the-project/master-prompt.md)

---

## Master Company & Role Guide

- **[COMPANY-AND-PRODUCT-GUIDE.md](./COMPANY-AND-PRODUCT-GUIDE.md)**
  - Exact role breakdown (**Senior Backend Engineer, Integrations**).
  - Ruit's mission: *"We want second-hand to become the first way everyone in Europe shops."*
  - Key investors: **Angels Capital** (Mercadona / Juan Roig), **Decelera**, **Abac**, **Successful Fund** (~€1M raised, target €1M ARR by 2027).
  - Product deep dive: 1-photo AI catalog listing, instant cross-listing, inventory anti-double-sell sync, Chrome Extension + Celery cloud workers.
  - Team: CEO **Luis Grau** and Founding Engineer **Alonso Veliz Garcia** (Python, Django, Rust).

---

## 7 Study Modules (10 Hours Total)

- **0. Schedule & Quick Cheat Sheets (`00-roadmap-and-quick-sheets/`)**
  - [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) — Step-by-step 10-hour study plan.
  - [01-ts-node-to-python-django-bridge.md](./00-roadmap-and-quick-sheets/01-ts-node-to-python-django-bridge.md) — How your Node.js/TypeScript knowledge maps to Python & Django, plus how to explain your honest Python level.
  - [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) — Quick summary of every topic on Luis's email cheat sheet for the train ride.

- **1. Hours 1–2: AI Workflow, Laptop Setup & Live Task (`01-ai-workflow-and-live-task/`)**
  - [01-my-real-ai-story-and-daily-workflow.md](./01-ai-workflow-and-live-task/01-my-real-ai-story-and-daily-workflow.md) — Your real resume work (QueryLaw schema checks, 150-site crawler, Dadroit VS Code extension) and daily 5-step workflow. (Zero claims of RAG, fine-tuning, ML deployment, or production Python/Django).
  - [02-harness-engineering-step-by-step.md](./01-ai-workflow-and-live-task/02-harness-engineering-step-by-step.md) — How to use **Harness Engineering** to implement an idea, feature, or project safely.
  - [03-antigravity-claude-code-and-copilot-flow.md](./01-ai-workflow-and-live-task/03-antigravity-claude-code-and-copilot-flow.md) — How you use **Antigravity IDE**, **Claude Code** (OpenRouter token in VS Code & CLI), and **GitHub Copilot Code Review**.
  - [04-multi-agents-parallel-sessions-skills-and-plugins.md](./01-ai-workflow-and-live-task/04-multi-agents-parallel-sessions-skills-and-plugins.md) — Agents, rules, skills, plugins, and 3 parallel session patterns without race conditions.
  - [05-laptop-setup-and-agentic-workflow-script.md](./01-ai-workflow-and-live-task/05-laptop-setup-and-agentic-workflow-script.md) — 5-minute pre-interview checklist and 3-minute screen-share presentation script for Luis.
  - [06-live-ai-coding-playbook.md](./01-ai-workflow-and-live-task/06-live-ai-coding-playbook.md) — 5-step calm strategy for the 20-minute live AI coding task.
  - [07-interview-qa-script-how-i-work-with-ai.md](./01-ai-workflow-and-live-task/07-interview-qa-script-how-i-work-with-ai.md) — 8 word-for-word Upper-B2 spoken interview answers.
  - [live-task-sandbox/README.md](./01-ai-workflow-and-live-task/live-task-sandbox/README.md) — Hands-on basic Python integration sandbox (`pytest` passing).
  - **Basic Python Code:** [marketplace_connector.py](./01-ai-workflow-and-live-task/live-task-sandbox/marketplace_connector.py) & [test_marketplace_connector.py](./01-ai-workflow-and-live-task/live-task-sandbox/test_marketplace_connector.py).

- **2. Hours 2–4: Python & Django Basics (`02-python-and-django-deep-dive/`)**
  - [01-the-gil-concurrency-and-async-python.md](./02-python-and-django-deep-dive/01-the-gil-concurrency-and-async-python.md) — The GIL, threads, processes, and `asyncio`.
  - [02-async-django-and-orm-internals.md](./02-python-and-django-deep-dive/02-async-django-and-orm-internals.md) — Async in Django, ORM queries, and fixing the N+1 problem.
  - [03-generators-iterators-and-streaming.md](./02-python-and-django-deep-dive/03-generators-iterators-and-streaming.md) — How `yield` and generators process large data without using much RAM.
  - [04-robust-python-typing-pydantic-static-analysis.md](./02-python-and-django-deep-dive/04-robust-python-typing-pydantic-static-analysis.md) — Type hints, Pydantic validation, and code checkers (`ruff`, `mypy`).
  - **Basic Python Code:** [django_concepts_examples.py](./02-python-and-django-deep-dive/python-django-labs/django_concepts_examples.py) & [test_python_deep_dive_labs.py](./02-python-and-django-deep-dive/python-django-labs/test_python_deep_dive_labs.py).

- **3. Hours 4–6: Backend Fundamentals Part 1 (`03-backend-fundamentals-cheatsheet/`)**
  - [01-celery-redis-and-background-queues.md](./03-backend-fundamentals-cheatsheet/01-celery-redis-and-background-queues.md) — Background jobs with Celery, Redis, and RabbitMQ.
  - [02-databases-sql-locking-and-redis-caching.md](./03-backend-fundamentals-cheatsheet/02-databases-sql-locking-and-redis-caching.md) — SQL indexes, database locks (stopping double-sells), and Redis cache.
  - [03-error-handling-python-vs-go-vs-rust.md](./03-backend-fundamentals-cheatsheet/03-error-handling-python-vs-go-vs-rust.md) — Error handling in Python vs Go vs Rust.
  - **Basic Python Code:** [test_concurrency_locks_and_errors.py](./03-backend-fundamentals-cheatsheet/fundamentals-labs/test_concurrency_locks_and_errors.py).

- **4. Hours 6–8: Backend Fundamentals Part 2 (`04-integrations-reverse-eng-browsers/`)**
  - [01-http-clients-tls-fingerprinting-and-networking.md](./04-integrations-reverse-eng-browsers/01-http-clients-tls-fingerprinting-and-networking.md) — HTTP/1.1 vs HTTP/2 vs HTTP/3, WebSockets, and TLS anti-bot checks.
  - [02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md](./04-integrations-reverse-eng-browsers/02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md) — Rebuilding APIs from network traffic and catching broken integrations early.
  - [03-browsers-playwright-and-chrome-extensions.md](./04-integrations-reverse-eng-browsers/03-browsers-playwright-and-chrome-extensions.md) — Playwright browser automation and Chrome Extensions.
  - [04-devops-docker-zero-downtime-and-observability.md](./04-integrations-reverse-eng-browsers/04-devops-docker-zero-downtime-and-observability.md) — Linux, Docker, zero-downtime deployments, and monitoring (metrics, logs, traces).

- **5. Hours 8–9.5: System Design Whiteboard (`05-system-design-whiteboard/`)**
  - [00-collaborative-whiteboard-framework.md](./05-system-design-whiteboard/00-collaborative-whiteboard-framework.md) — How to design together with the team on the whiteboard.
  - [01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md](./05-system-design-whiteboard/01-challenge-1-proactive-breakage-detection-and-self-healing-integrations.md)
  - [02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md](./05-system-design-whiteboard/02-challenge-2-multi-marketplace-inventory-sync-and-double-sell-prevention.md)
  - [03-challenge-3-rapid-new-marketplace-connector-architecture.md](./05-system-design-whiteboard/03-challenge-3-rapid-new-marketplace-connector-architecture.md)
  - [04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md](./05-system-design-whiteboard/04-challenge-4-ai-catalog-normalization-and-cross-marketplace-mapping.md)
  - [05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md](./05-system-design-whiteboard/05-challenge-5-hybrid-chrome-extension-and-cloud-worker-execution.md)

- **6. Hours 9.5–10: Stories & Team Lunch (`06-culture-lunch-and-storytelling/`)**
  - [01-my-3-signature-stories-for-ruit.md](./06-culture-lunch-and-storytelling/01-my-3-signature-stories-for-ruit.md) — Your 3 main project stories.
  - [02-team-lunch-and-questions-for-luis-and-team.md](./06-culture-lunch-and-storytelling/02-team-lunch-and-questions-for-luis-and-team.md) — Team lunch tips and questions to ask.
