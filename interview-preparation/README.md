# Ruit Final Interview Preparation (10-Hour Guide)

- **Candidate:** Simin Shoeibi
- **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival, `13:00h–16:00h` interviews @ Lanzadera, Valencia)
- **Main Source:** Luis Grau's email cheat sheet ([`docs/resources/first emails.md`](../docs/resources/first%20emails.md))
- **AI Project Files:** [`ai-state.md`](../docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md) | [`master-prompt.md`](../docs/ai-assitant-analysis/the-context-of-the-project/master-prompt.md)

---

## Study Folders (10 Hours Total + Dedicated 2–4 Hour AI Workflow Deep Dive)

- **★ Dedicated AI Workflow Deep Dive (`ai-workflow/` — 2 to 4 Hours):**
  - [ai-workflow/README.md](./ai-workflow/README.md) — 2-to-4-hour study plan for your daily AI workflow.
  - [01-my-real-ai-story-and-daily-workflow.md](./ai-workflow/01-my-real-ai-story-and-daily-workflow.md) — Your real resume story (QueryLaw AJV schema checks, 150-site crawler, no RAG/fine-tuning/Python claims) and daily 5-step AI workflow.
  - [02-harness-engineering-step-by-step.md](./ai-workflow/02-harness-engineering-step-by-step.md) — How to use **Harness Engineering** to implement an idea, feature, or project safely.
  - [03-antigravity-claude-code-and-copilot-flow.md](./ai-workflow/03-antigravity-claude-code-and-copilot-flow.md) — How you use **Antigravity IDE**, **Claude Code** (OpenRouter token + VS Code), and **GitHub Copilot Code Review**.
  - [04-multi-agents-parallel-sessions-skills-and-plugins.md](./ai-workflow/04-multi-agents-parallel-sessions-skills-and-plugins.md) — Agents, subagents, skills (`SKILL.md`), plugins, custom commands, and parallel sessions.
  - [05-interview-qa-script-how-i-work-with-ai.md](./ai-workflow/05-interview-qa-script-how-i-work-with-ai.md) — Word-for-word Upper-B2 Q&A script for Luis's AI workflow questions.

- **0. Schedule & Quick Cheat Sheets (`00-roadmap-and-quick-sheets/`)**
  - [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) — Step-by-step 10-hour study plan.
  - [01-ts-node-to-python-django-bridge.md](./00-roadmap-and-quick-sheets/01-ts-node-to-python-django-bridge.md) — How your Node.js/TypeScript knowledge maps to Python & Django, plus how to explain your honest Python level.
  - [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) — Quick summary of every topic on Luis's email cheat sheet for the train ride.

- **1. Hours 1–2: AI Setup & Live Task (`01-ai-workflow-and-live-task/`)**
  - [01-laptop-setup-and-agentic-workflow-script.md](./01-ai-workflow-and-live-task/01-laptop-setup-and-agentic-workflow-script.md) — How to show your laptop, AI agents, skills, plugins, and parallel sessions.
  - [02-live-ai-coding-playbook.md](./01-ai-workflow-and-live-task/02-live-ai-coding-playbook.md) — Simple 5-step plan for the 20-minute live AI task.
  - [live-task-sandbox/README.md](./01-ai-workflow-and-live-task/live-task-sandbox/README.md) — 3 practice tasks.
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
