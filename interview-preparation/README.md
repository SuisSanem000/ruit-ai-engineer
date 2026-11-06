# Ruit Final Interview Preparation (Senior Systems Architecture & AI Orchestration)

> **Position Applying For:** **Senior Backend Engineer, Integrations**  
> *(Dual Consideration: Luis confirmed you are also considered for **Senior Full Stack Engineer, Integrations / AI Engineer**).*
>
> - **Candidate:** Simin Shoeibi (9+ Years Senior Backend Engineering)
> - **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival @ Lanzadera, Valencia)
> - **Company Guide:** [COMPANY-AND-PRODUCT-GUIDE.md](./COMPANY-AND-PRODUCT-GUIDE.md) (~€1M funding, €1M ARR target, 1-photo AI listing, anti-double-sell sync)
> - **Primary Foundation:** Luis's email cheat sheet ([`docs/resources/first emails.md`](../docs/resources/first%20emails.md))
> - **Honest Positioning:** You do **not** know Python and have never worked with Python in production. You orchestrate AI agents (Antigravity IDE, Claude Code via OpenRouter, GitHub Copilot) with senior architectural rigor, strict data schemas, and automated testing harnesses.

---

## Study Progress Tracker

| Section | Core Files | Status |
| :--- | :--- | :--- |
| **Root Interview Showcase** | [Root README.md](../README.md) & [`CLAUDE.md`](../CLAUDE.md) | `[x] READY TO SHOW` |
| **AI Workflow Step-by-Step** | [ai-workflow-step-by-step/](./ai-workflow-step-by-step/README.md) (Files 01, 02, 03) | `[x] PRIMARY FOR TODAY` |
| **16-Agent Worktree Prototype** | [multi-agent-worktree-orchestrator/](./multi-agent-worktree-orchestrator/README.md) | `[x] RUNNABLE DEMO` |
| **Company & Role** | [COMPANY-AND-PRODUCT-GUIDE.md](./COMPANY-AND-PRODUCT-GUIDE.md) | `[x] COMPLETED` |
| **0. Roadmap & Quick Sheets** | [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) | `[x] COMPLETED` |
| | [01-my-senior-backend-positioning-and-polyglot-mindset.md](./00-roadmap-and-quick-sheets/01-my-senior-backend-positioning-and-polyglot-mindset.md) | `[x] COMPLETED` |
| | [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) | `[x] COMPLETED` |
| **1. AI Foundations & Resume** | `01-ai-workflow-and-live-task/` (Files 01, 02, 03) | `[x] COMPLETED` |
| **2. Backend Fundamentals (Queues, Locks)** | `03-backend-fundamentals-cheatsheet/` (Files 01, 02) | `[x] COMPLETED` |
| **3. Networking, Reverse Eng, DevOps** | `04-integrations-reverse-eng-browsers/` (Files 01, 02) | `[x] COMPLETED` |
| **4. System Design Whiteboard** | `05-system-design-whiteboard/` (Files 01, 02) (5 Ruit Challenges) | `[x] COMPLETED` |
| **5. Stories & Team Lunch** | `06-culture-lunch-and-storytelling/` (File 01) | `[x] COMPLETED` |

---

## Consolidated Module Index (Zero Fluff, 100% Systems Architecture)

### 🌟 Primary Live Demo & Interview Execution (13:00h – 14:00h)

- **Step-by-Step AI Interview Playbook (`ai-workflow-step-by-step/`)**
  - [01-part1-show-your-laptop-setup.md](./ai-workflow-step-by-step/01-part1-show-your-laptop-setup.md) — 4 things to show on screen in the first 5 minutes.
  - [02-part2-execute-the-live-ai-task.md](./ai-workflow-step-by-step/02-part2-execute-the-live-ai-task.md) — 6 chronological steps to execute any 20-minute live task as a Senior Harness Engineer.
  - [03-part3-agents-skills-plugins-and-parallel-sessions.md](./ai-workflow-step-by-step/03-part3-agents-skills-plugins-and-parallel-sessions.md) — Spoken answers for agents, skills, plugins, and parallel sessions.

- **16-Agent Concurrency Prototype (`multi-agent-worktree-orchestrator/`)**
  - [multi-agent-worktree-orchestrator/README.md](./multi-agent-worktree-orchestrator/README.md) — Full architecture diagram, 5 deep technical interview Q&As, and 2-minute demo commands.
  - Runs 16 isolated Git worktrees (`.worktrees/agent-01..16`) with a 4-slot Token-Bucket Rate Limiter and sequential merge queue.

---

### 📚 Technical Knowledge Base & Systems Architecture

- **0. Roadmap & Quick Sheets (`00-roadmap-and-quick-sheets/`)**
  - [00-master-10-hour-schedule.md](./00-roadmap-and-quick-sheets/00-master-10-hour-schedule.md) — Master study schedule.
  - [01-my-senior-backend-positioning-and-polyglot-mindset.md](./00-roadmap-and-quick-sheets/01-my-senior-backend-positioning-and-polyglot-mindset.md) — Senior backend positioning and honest spoken script.
  - [02-euromed-train-rapid-cheatsheet.md](./00-roadmap-and-quick-sheets/02-euromed-train-rapid-cheatsheet.md) — 10-minute cheat sheet for the train ride.

- **1. AI Workflow & Resume Story (`01-ai-workflow-and-live-task/`)**
  - [01-my-real-ai-story-and-daily-workflow.md](./01-ai-workflow-and-live-task/01-my-real-ai-story-and-daily-workflow.md) — Real resume story (QueryLaw AJV schema validation, 150-site crawler, Dadroit 630K extension) and 5-step Harness Engineering loop.
  - [02-multi-agents-laptop-setup-and-live-task-playbook.md](./01-ai-workflow-and-live-task/02-multi-agents-laptop-setup-and-live-task-playbook.md) — Multi-agent patterns, 3-minute screen-share walkthrough script, and 5 senior architectural audit checks.
  - [03-spoken-qa-scripts-how-i-work-with-ai.md](./01-ai-workflow-and-live-task/03-spoken-qa-scripts-how-i-work-with-ai.md) — 6 spoken Upper-B2 interview scripts answering Luis's exact cheat sheet questions.

- **2. Backend Fundamentals (Queues, Locks & Errors) (`03-backend-fundamentals-cheatsheet/`)**
  - [01-celery-redis-and-sql-locking.md](./03-backend-fundamentals-cheatsheet/01-celery-redis-and-sql-locking.md) — Background queues (Celery/Redis), Redis cache stampede prevention, and SQL `SELECT ... FOR UPDATE` double-sell prevention.
  - [02-error-handling-python-vs-go-vs-rust.md](./03-backend-fundamentals-cheatsheet/02-error-handling-python-vs-go-vs-rust.md) — Comparing error handling philosophies (exceptions vs explicit errors vs algebraic types) and marketplace integration error classification.

- **3. Networking, Reverse Engineering, Browsers & DevOps (`04-integrations-reverse-eng-browsers/`)**
  - [01-networking-protocols-and-tls.md](./04-integrations-reverse-eng-browsers/01-networking-protocols-and-tls.md) — TCP 3-way handshake, UDP, DNS, HTTP/1.1 vs HTTP/2 vs HTTP/3, WebSockets vs SSE vs Webhooks, and TLS fingerprinting bypass (`curl-impersonate` / `curl_cffi`).
  - [02-reverse-engineering-browsers-and-devops.md](./04-integrations-reverse-eng-browsers/02-reverse-engineering-browsers-and-devops.md) — `.har` traffic analysis, Chrome Extensions (MV3), Playwright, zero-downtime DB migrations, and observability.

- **4. System Design Whiteboard (`05-system-design-whiteboard/`)**
  - [01-collaborative-framework-and-architecture.md](./05-system-design-whiteboard/01-collaborative-framework-and-architecture.md) — 4-step collaborative whiteboard framework and spoken phrases.
  - [02-the-5-ruit-system-design-challenges.md](./05-system-design-whiteboard/02-the-5-ruit-system-design-challenges.md) — Complete architectures for the 5 real Ruit challenges (Breakage detection, double-sell prevention, rapid connector adapter, 1-photo AI mapping, hybrid Chrome extension).

- **5. Stories, Team Lunch & Questions (`06-culture-lunch-and-storytelling/`)**
  - [01-stories-lunch-and-questions.md](./06-culture-lunch-and-storytelling/01-stories-lunch-and-questions.md) — 3 STAR stories (Visual Meta B2B SaaS, Dotin banking deadlock fix, Visual Meta PHP rewrite), lunch etiquette, and high-impact questions for Luis and the team.
