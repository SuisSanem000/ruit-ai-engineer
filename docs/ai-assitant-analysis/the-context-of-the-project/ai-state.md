# Ruit Final Interview — Project Context & AI State

> **Last Updated:** 2026-11-05  
> **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival $\rightarrow$ `13:00h–16:00h` @ Lanzadera, Valencia)  
> **Status:** Python Teaching & Code Completely Removed. Pure Senior Backend Systems Architecture & AI Orchestration (14 High-Signal Markdown Files).

---

## 1. Company & Role Summary

- **Company:** Ruit (`https://ruit.es/en/`), based at Lanzadera in Valencia.
- **Interviewer:** Luis Grau (CEO) and Founding Engineer Alonso Veliz Garcia (Python, Django, Rust).
- **Product:** A tool that lets professional second-hand sellers list and manage products on many marketplaces (Wallapop, Vinted, eBay, Depop, Vestiaire, Facebook Marketplace, etc.) from one place with 1-photo AI listing and instant inventory sync to prevent double-selling.
- **Position Applied For:** **Senior Backend Engineer, Integrations** (with dual-role consideration for **Senior Full Stack Engineer, Integrations / AI Engineer** confirmed by Luis).

---

## 2. Candidate Profile & Honest Positioning (Simin Shoeibi)

- **Main Strengths (9+ Years Experience):**
  - Built **Dadroit JSON Generator** VS Code extension in 3 days (630K+ installs) and worked on a desktop JSON Viewer (60K+ users).
  - Built a **news crawler for 150+ websites** (60K+ daily users) at Parsaiane with OpenAI summarization.
  - Built **QueryLaw's AI legal platform** (95%+ accuracy using prompt engineering, strict **JSON Schema/AJV validation checks**, retry/repair loops, and error monitoring — **no** RAG, fine-tuning, or ML model deployment).
  - Strong backend architecture experience in **Node.js/TypeScript**, PostgreSQL, Redis, RabbitMQ, Socket.IO (60K+ concurrent users), and Docker.
  - **Daily AI Coding Setup:** Uses **Harness Engineering**, **Antigravity IDE** (agents, skills, rules, subagents), **Claude Code** in VS Code & terminal via **OpenRouter token** (`CLAUDE.md`, Plan Mode, `/compact`, custom commands, skills), and **GitHub Copilot Code Review** on diffs and PRs.
- **Honest Positioning on Python:**
  - Simin **does not know Python** and has **never worked with Python or Django in production**.
  - She does not memorize or manually write Python syntax.
  - When working across any new language or codebase (Python, Rust, Go), she acts as the **Senior Systems Architect & Harness Engineer**: she defines the data models, system boundaries, error types, and test contracts. She directs AI agents (Antigravity, Claude Code via OpenRouter) to generate the implementation and self-correct via terminal test suites.

---

## 3. Consolidated Workspace Structure (14 Markdown Files Total — Zero Code Files)

```text
ruit-ai-engineer/
├── docs/
│   ├── resources/                              # [READ-ONLY — NEVER TOUCH]
│   └── ai-assitant-analysis/
│       └── the-context-of-the-project/
│           ├── ai-state.md                     # Project state & rules
│           └── master-prompt.md                # Master prompt
└── interview-preparation/
    ├── README.md                               # Master index & study progress tracker
    ├── COMPANY-AND-PRODUCT-GUIDE.md            # Master company, product, funding & team guide
    ├── 00-roadmap-and-quick-sheets/
    │   ├── 00-master-10-hour-schedule.md       # 5-step master study schedule
    │   ├── 01-my-senior-backend-positioning-and-polyglot-mindset.md # Honest positioning script
    │   └── 02-euromed-train-rapid-cheatsheet.md # 10-minute cheat sheet for train ride
    ├── 01-ai-workflow-and-live-task/
    │   ├── README.md                           # Module overview
    │   ├── 01-my-real-ai-story-and-daily-workflow.md # Real resume story & 5-step workflow
    │   ├── 02-multi-agents-laptop-setup-and-live-task-playbook.md # Agents, laptop demo, live task
    │   └── 03-spoken-qa-scripts-how-i-work-with-ai.md # 6 spoken Upper-B2 interview scripts
    ├── 03-backend-fundamentals-cheatsheet/
    │   ├── 01-celery-redis-and-sql-locking.md  # Queues, Redis caching, SELECT FOR UPDATE
    │   └── 02-error-handling-python-vs-go-vs-rust.md # Error handling philosophies
    ├── 04-integrations-reverse-eng-browsers/
    │   ├── 01-networking-protocols-and-tls.md  # TCP, UDP, DNS, HTTP/1-2-3, WS, TLS (curl-impersonate)
    │   └── 02-reverse-engineering-browsers-and-devops.md # .har traffic, Chrome Ext, DevOps
    ├── 05-system-design-whiteboard/
    │   ├── 01-collaborative-framework-and-architecture.md # Whiteboard framework & spoken phrases
    │   └── 02-the-5-ruit-system-design-challenges.md # 5 complete Ruit challenge designs
    └── 06-culture-lunch-and-storytelling/
        └── 01-stories-lunch-and-questions.md   # 3 STAR stories, lunch prep, questions for Luis
```

---

## 4. Study Progress Tracker

| Section | Core Files | Status |
| :--- | :--- | :--- |
| **Company & Role** | `COMPANY-AND-PRODUCT-GUIDE.md` | `[ ] Pending` |
| **0. Roadmap & Quick Sheets** | `00-roadmap-and-quick-sheets/` (Files 00, 01, 02) | `[x] COMPLETED` |
| **1. AI Workflow & Live Task** | `01-ai-workflow-and-live-task/` (Files 01, 02, 03) | `[ ] Up Next / Revisit` |
| **2. Backend Fundamentals** | `03-backend-fundamentals-cheatsheet/` (Files 01, 02) | `[ ] Pending` |
| **3. Networking & DevOps** | `04-integrations-reverse-eng-browsers/` (Files 01, 02) | `[⏳ READING NOW]` |
| **4. System Design Whiteboard** | `05-system-design-whiteboard/` (Files 01, 02) | `[ ] Pending` |
| **5. Stories & Team Lunch** | `06-culture-lunch-and-storytelling/` (File 01) | `[ ] Pending` |

---

## 5. Change Log

- **2026-11-06 (Session 21 — No-Code Step-by-Step AI Workflow Folder for Today's Interview):**
  - Created `ai-workflow-step-by-step/` beside `interview-preparation/` and `multi-agent-worktree-orchestrator/` with zero code blocks:
    - `README.md`: Overview of the 3 parts of the 13:00h AI session.
    - `01-part1-show-your-laptop-setup.md`: 4 exact steps to show on screen and say in the first 5 minutes.
    - `02-part2-execute-the-live-ai-task.md`: 6 exact chronological steps to execute the 20-minute live AI task as a Senior Harness Engineer.
    - `03-part3-agents-skills-plugins-and-parallel-sessions.md`: Step-by-step non-code explanation of Rules vs. Skills vs. Plugins, Subagents, and the 16-Agent Git Worktree parallel architecture.
- **2026-11-06 (Session 20 — 16-Agent Git Worktree & OpenRouter Concurrency Orchestrator Prototype):**
  - Built `multi-agent-worktree-orchestrator/` beside `interview-preparation/` in TypeScript:
    - `setup.sh`: Automates Git verification on `main`, `.gitignore`, dependency setup (`tsx`, `typescript`), and build verification.
    - `src/worktree.ts`: Programmatically provisions and tears down 16 isolated Git worktrees (`.worktrees/agent-01` .. `.worktrees/agent-16` on `feature/agent-01` .. `feature/agent-16`) with stale lock cleanup and `git worktree prune`.
    - `src/orchestrator.ts`: 16 disjoint micro-tasks with a 4-slot Semaphore + Token-Bucket rate limiter supporting direct OpenRouter API (`fetch`), Headless Claude Code CLI (`claude -p`), and zero-token `--mock` mode.
    - `src/merge.ts`: Gated sequential integration pipeline running `npx tsc --noEmit` inside each worktree before FIFO mutex-serialized rebasing and merging onto `main`.
    - `src/logger.ts`: Live terminal dashboard showing all 16 workers, worktree paths, statuses, and rate-limiter telemetry.
    - `README.md`: Comprehensive interview study guide with ASCII architecture diagram, 5 deep technical Q&As, and 2-minute execution cheatsheet.
- **2026-11-05 (Session 19 — Total Removal of Python Teaching & Code Files):**
  - Removed all Python teaching modules (`02-python-and-django-deep-dive/`) and all code sandbox directories (`live-task-sandbox/`, `python-django-labs/`, `fundamentals-labs/`).
  - Total workspace streamlined to **14 high-signal markdown files** with **zero code files** and **zero markdown code blocks**.
  - Reinforced candidate's 100% honest stance: Simin does not know Python and does not write Python syntax manually. She operates as a Senior Systems Architect orchestrating AI agents (Antigravity IDE, Claude Code via OpenRouter, GitHub Copilot) with strict data contracts and automated testing harnesses.
