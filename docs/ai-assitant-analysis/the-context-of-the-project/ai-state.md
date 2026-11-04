# Ruit Final Interview — Project Context & AI State

> **Last Updated:** 2026-11-04  
> **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival $\rightarrow$ `13:00h–16:00h` @ Lanzadera, Valencia)  
> **Status:** All Modules Fully Consolidated (50%+ Fewer Files, Zero Fluff, 100% Core Value Preserved)

---

## 1. Company & Role Summary

- **Company:** Ruit (`https://ruit.es/en/`), based at Lanzadera in Valencia.
- **Interviewer:** Luis Grau (CEO) and Founding Engineer Alonso Veliz Garcia (Python, Django, Rust).
- **Product:** A tool that lets professional second-hand sellers list and manage products on many marketplaces (Wallapop, Vinted, eBay, Depop, Vestiaire, Facebook Marketplace, etc.) from one place with 1-photo AI listing and instant inventory sync to prevent double-selling.
- **Exact Position Applied For:** **Senior Backend Engineer, Integrations (Python)** (with dual-role consideration for **Senior Full Stack Engineer, Integrations (Python) / AI Engineer** confirmed by Luis).

---

## 2. Candidate Profile & Honest Python Positioning (Simin Shoeibi)

- **Main Strengths (9+ Years Experience):**
  - Built **Dadroit JSON Generator** VS Code extension in 3 days (630K+ installs) and worked on a desktop JSON Viewer (60K+ users).
  - Built a **news crawler for 150+ websites** (60K+ daily users) at Parsaiane with OpenAI summarization.
  - Built **QueryLaw's AI legal platform** (95%+ accuracy using prompt engineering, strict **JSON Schema/AJV validation checks**, retry/repair loops, and error monitoring — **no** RAG, fine-tuning, or ML model deployment).
  - Strong backend architecture experience in **Node.js/TypeScript**, PostgreSQL, Redis, RabbitMQ, Socket.IO (60K+ concurrent users), and Docker.
  - **Daily AI Coding Setup:** Uses **Harness Engineering**, **Antigravity IDE** (agents, skills, rules, subagents), **Claude Code** in VS Code & terminal via **OpenRouter token** (`CLAUDE.md`, Plan Mode, `/compact`, custom commands, skills), and **GitHub Copilot Code Review** on diffs and PRs.
- **Honest Python & Django Positioning:**
  - Simin has **no production experience with Python or Django**.
  - She has only used Python in **basic side projects** and **reviewed basic Python syntax** for this interview.
  - She is 100% open about this. She answers architecture questions using her 9+ years of backend experience and uses her AI Harness Engineering workflow to write and verify **simple, basic Python**.

---

## 3. Consolidated Workspace Structure (19 Markdown Files Total)

```text
ruit-ai-engineer/
├── docs/
│   ├── resources/                              # [READ-ONLY]
│   └── ai-assitant-analysis/
│       └── the-context-of-the-project/
│           ├── ai-state.md                     # Project state & rules
│           └── master-prompt.md                # Master prompt
└── interview-preparation/
    ├── README.md                               # Consolidated index & study progress tracker
    ├── COMPANY-AND-PRODUCT-GUIDE.md            # Master company, product, funding & team guide
    ├── 00-roadmap-and-quick-sheets/
    │   ├── 00-master-10-hour-schedule.md       # 6-step study schedule
    │   ├── 01-ts-node-to-python-django-bridge.md # Node.js vs Python concept bridge & honest pitch
    │   └── 02-euromed-train-rapid-cheatsheet.md # 10-minute cheat sheet for train ride
    ├── 01-ai-workflow-and-live-task/
    │   ├── README.md                           # Module overview
    │   ├── 01-my-real-ai-story-and-daily-workflow.md # Real resume story & 5-step workflow
    │   ├── 02-multi-agents-laptop-setup-and-live-task-playbook.md # Agents, laptop demo, live task
    │   ├── 03-spoken-qa-scripts-how-i-work-with-ai.md # 6 spoken Upper-B2 interview scripts
    │   └── live-task-sandbox/                  # Basic Python code and tests
    ├── 02-python-and-django-deep-dive/
    │   ├── 01-the-gil-concurrency-and-async-django.md # GIL, WSGI/ASGI, async ORM, N+1 queries
    │   ├── 02-generators-streaming-pydantic-and-typing.md # Generators, streaming, Pydantic, types
    │   └── python-django-labs/                 # Basic Python code and labs
    ├── 03-backend-fundamentals-cheatsheet/
    │   ├── 01-celery-redis-and-sql-locking.md  # Celery, Redis caching, SELECT FOR UPDATE
    │   ├── 02-error-handling-python-vs-go-vs-rust.md # Error handling philosophies
    │   └── fundamentals-labs/                  # Basic Python locking and rate limit labs
    ├── 04-integrations-reverse-eng-browsers/
    │   ├── 01-networking-protocols-and-tls.md  # TCP, UDP, DNS, HTTP/1-2-3, WS, TLS (curl_cffi)
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
| **2. Python & Django Deep Dive** | `02-python-and-django-deep-dive/` (Files 01, 02) | `[ ] Pending` |
| **3. Backend Fundamentals** | `03-backend-fundamentals-cheatsheet/` (Files 01, 02) | `[ ] Pending` |
| **4. Networking & DevOps** | `04-integrations-reverse-eng-browsers/` (Files 01, 02) | `[⏳ READING NOW]` |
| **5. System Design Whiteboard** | `05-system-design-whiteboard/` (Files 01, 02) | `[ ] Pending` |
| **6. Stories & Team Lunch** | `06-culture-lunch-and-storytelling/` (File 01) | `[ ] Pending` |

---

## 5. Change Log

- **2026-11-04 (Session 18 — 50%+ Consolidation & Lean Refactor):**
  - Consolidated `interview-preparation/` from 35 markdown files down to **19 high-signal files** (total lines cut from 1,817 to **884 lines**, exactly 51.3% reduction).
  - Kept 100% of core technical definitions, spoken scripts, architecture diagrams, and the honest Node.js/Python positioning.
  - Zero code blocks in markdown files; all 13 Python tests passing with ruff and mypy clean.
