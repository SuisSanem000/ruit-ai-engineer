# 10-Hour Study Plan — Ruit Final Interview

- **Interview Day:** Friday, November 6, 2026 in Valencia (Lanzadera).
- **Schedule:**
  - `12:45 – 13:00`: Arrive at the office (your sister can wait there).
  - `13:00 – 14:00`: Show your laptop AI setup, do a short task with AI, and talk about Luis's cheat sheet topics.
  - `14:00 – 15:00`: Lunch with the team (most important part for team fit).
  - `15:00 – 16:00`: 60-minute whiteboard system design (pick 1 of ~5 real Ruit challenges and design it together).

---

## Step-by-Step 10-Hour Study Schedule

### Preparation Before Starting (15 mins)
- Read [COMPANY-AND-PRODUCT-GUIDE.md](../COMPANY-AND-PRODUCT-GUIDE.md) to understand Ruit's mission, product features, funding, team, and your exact role (Senior Backend Engineer, Integrations).

### Hours 1–2: AI Setup, Daily Workflow & Live Task Practice
- Read [01-ai-workflow-and-live-task/README.md](../01-ai-workflow-and-live-task/README.md) and study the 7 guides in [`01-ai-workflow-and-live-task/`](../01-ai-workflow-and-live-task/) covering **Harness Engineering**, your real QueryLaw schema check story, Antigravity IDE, Claude Code (OpenRouter), Copilot Code Review, parallel sessions, and the 20-minute live task playbook (60 mins).
- Practice with [marketplace_connector.py](../01-ai-workflow-and-live-task/live-task-sandbox/marketplace_connector.py) and [test_marketplace_connector.py](../01-ai-workflow-and-live-task/live-task-sandbox/test_marketplace_connector.py), reading the code comments and running tests with your AI assistant (60 mins).

### Hours 2–4: Python & Django Concepts
- Read [01-ts-node-to-python-django-bridge.md](./01-ts-node-to-python-django-bridge.md) to connect your Node.js/TypeScript knowledge to Python (20 mins).
- Read [01-the-gil-concurrency-and-async-python.md](../02-python-and-django-deep-dive/01-the-gil-concurrency-and-async-python.md) (25 mins).
- Read [02-async-django-and-orm-internals.md](../02-python-and-django-deep-dive/02-async-django-and-orm-internals.md) (25 mins).
- Read [03-generators-iterators-and-streaming.md](../02-python-and-django-deep-dive/03-generators-iterators-and-streaming.md) (20 mins).
- Read [04-robust-python-typing-pydantic-static-analysis.md](../02-python-and-django-deep-dive/04-robust-python-typing-pydantic-static-analysis.md) and review the comments in [test_python_deep_dive_labs.py](../02-python-and-django-deep-dive/python-django-labs/test_python_deep_dive_labs.py) (30 mins).

### Hours 4–6: Queues, Databases, Cache & Error Handling
- Read [01-celery-redis-and-background-queues.md](../03-backend-fundamentals-cheatsheet/01-celery-redis-and-background-queues.md) (40 mins).
- Read [02-databases-sql-locking-and-redis-caching.md](../03-backend-fundamentals-cheatsheet/02-databases-sql-locking-and-redis-caching.md) (40 mins).
- Read [03-error-handling-python-vs-go-vs-rust.md](../03-backend-fundamentals-cheatsheet/03-error-handling-python-vs-go-vs-rust.md) and review [test_concurrency_locks_and_errors.py](../03-backend-fundamentals-cheatsheet/fundamentals-labs/test_concurrency_locks_and_errors.py) (40 mins).

### Hours 6–8: Networking, API Reverse Engineering, Browsers & DevOps
- Read [00-low-level-networking-tcp-udp-dns-and-http-fundamentals.md](../04-integrations-reverse-eng-browsers/00-low-level-networking-tcp-udp-dns-and-http-fundamentals.md) for TCP 3-way handshake, UDP, DNS resolution, socket `TIME_WAIT`, and status codes (25 mins).
- Read [01-http-clients-tls-fingerprinting-and-networking.md](../04-integrations-reverse-eng-browsers/01-http-clients-tls-fingerprinting-and-networking.md) for HTTP/1.1 vs HTTP/2 vs HTTP/3, WebSockets vs SSE vs Webhooks, connection pools, and TLS bot protection (25 mins).
- Read [02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md](../04-integrations-reverse-eng-browsers/02-rebuilding-apis-from-network-traffic-and-keeping-integrations-alive.md) (25 mins).
- Read [03-browsers-playwright-and-chrome-extensions.md](../04-integrations-reverse-eng-browsers/03-browsers-playwright-and-chrome-extensions.md) (25 mins).
- Read [04-devops-docker-zero-downtime-and-observability.md](../04-integrations-reverse-eng-browsers/04-devops-docker-zero-downtime-and-observability.md) (20 mins).

### Hours 8–9.5: System Design Whiteboard Practice
- Read [00-collaborative-whiteboard-framework.md](../05-system-design-whiteboard/00-collaborative-whiteboard-framework.md) (15 mins).
- Read the 5 Ruit system design challenges (`01` to `05`) in [`05-system-design-whiteboard/`](../05-system-design-whiteboard/) and practice drawing simple box-and-arrow diagrams on paper (75 mins).

### Hours 9.5–10: Project Stories, Lunch Prep & Train Review
- Read [01-my-3-signature-stories-for-ruit.md](../06-culture-lunch-and-storytelling/01-my-3-signature-stories-for-ruit.md) and [02-team-lunch-and-questions-for-luis-and-team.md](../06-culture-lunch-and-storytelling/02-team-lunch-and-questions-for-luis-and-team.md) (20 mins).
- Save [02-euromed-train-rapid-cheatsheet.md](./02-euromed-train-rapid-cheatsheet.md) for a 10-minute review on the train to Valencia.
