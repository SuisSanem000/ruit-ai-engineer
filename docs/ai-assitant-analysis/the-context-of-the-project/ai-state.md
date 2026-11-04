# Ruit Final Interview — Project Context & AI State

> **Last Updated:** 2026-11-04  
> **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival $\rightarrow$ `13:00h–16:00h` @ Lanzadera, Valencia)  
> **Status:** All Modules (0–6) Unified, Module 1 Merged with AI Workflow & Live Task, Company Guide Added

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

## 3. Friday Onsite Schedule & Luis's Email Cheat Sheet

- **12:45 – 13:00:** Arrive at Lanzadera office (sister can wait at the office).
- **13:00 – 14:00 (Interview 1 — Laptop AI Task + Technical Chat):**
  - Open laptop, show AI setup, and finish a short task with AI.
  - Chat about Luis's cheat sheet:
    - **How you work with AI:** Agents, skills, plugins, parallel sessions.
    - **Python & Django:** The GIL, async in Django, generators, type hints, and static analysis.
    - **Backend Fundamentals:** Concurrency & async, JSON validation, ORMs & SQL, background queues (Celery & Redis), HTTP clients & TLS, error handling (Python vs Go vs Rust), databases & cache, networking & protocols (HTTP, WebSockets), API integrations & reverse engineering, browsers/automations & Chrome extensions, DevOps (Linux, Docker, Docker Compose, zero-downtime deploys), observability (metrics, logs, traces), scaling.
- **14:00 – 15:00 (Team Lunch):** Most important part — team fit, communication, and shared values.
- **15:00 – 16:00 (Interview 2 — System Design Whiteboard):** Pick 1 of ~5 real Ruit challenges for the coming months and design it together on the whiteboard.

---

## 4. Mandatory Rules for AI Assistant

1. **Never Touch `docs/resources/`:** Treat `docs/resources/` as strictly read-only.
2. **Email Cheat Sheet Priority:** Prioritize `docs/resources/first emails.md` over all other files. Only keep job-ad details if they directly relate to the email cheat sheet.
3. **Short Bullet-List Markdown Files:** Keep all `.md` and `README.md` files as short as possible using bullet lists and short sentences, while keeping explanations clear and detailed enough to understand.
4. **Upper-B2 English Level:** Write all explanations and interview answers in clear, natural **Upper-B2 English** (avoid academic or overly complex words).
5. **Code & Comments Only in `.py` Files:** Put all code examples inside `.py` files with detailed comments explaining what the code does. Do not put code blocks inside `.md` study files.
6. **Keep Python Code Basic:** Keep all Python code as basic and simple as possible (matching someone who knows backend systems well, has done basic Python side projects, and is open about not using Python/Django in production).
7. **Update State & Commit to Git:** Update this `ai-state.md` file and run `git add -A && git commit -m "..."` after every change.

---

## 5. Workspace Structure

```text
ruit-ai-engineer/
├── docs/
│   ├── resources/                              # [READ-ONLY]
│   └── ai-assitant-analysis/
│       └── the-context-of-the-project/
│           ├── ai-state.md                     # Project state & rules
│           └── master-prompt.md                # Master prompt
└── interview-preparation/
    ├── README.md                               # Short index of all folders & role reminder
    ├── COMPANY-AND-PRODUCT-GUIDE.md            # Comprehensive company, product, funding & team guide
    ├── 00-roadmap-and-quick-sheets/            # 10-hour plan, TS->Python bridge, train cheat sheet
    ├── 01-ai-workflow-and-live-task/           # Merged AI workflow, Harness Engineering, laptop demo & live sandbox
    ├── 02-python-and-django-deep-dive/         # GIL, Async Django, Generators, Typing + basic Python lab
    ├── 03-backend-fundamentals-cheatsheet/     # Celery/Redis, SQL/Cache, Error handling + basic Python lab
    ├── 04-integrations-reverse-eng-browsers/   # HTTP/TLS, Reverse Eng, Playwright/Chrome Ext, DevOps
    ├── 05-system-design-whiteboard/            # Whiteboard guide + 5 Ruit system design challenges
    └── 06-culture-lunch-and-storytelling/      # 3 project stories + team lunch questions
```

---

## 6. 10-Hour Study Progress Tracker

| Hours | Module | Folder | Status |
| :--- | :--- | :--- | :--- |
| **1.0 – 2.0** | Module 1: AI Setup & Live Task | `interview-preparation/01-ai-workflow-and-live-task/` | `[x] Completed` |
| **2.0 – 4.0** | Module 2: Python & Django Basics | `interview-preparation/02-python-and-django-deep-dive/` | `[x] Completed` |
| **4.0 – 6.0** | Module 3: Queues, DB, Cache & Errors | `interview-preparation/03-backend-fundamentals-cheatsheet/` | `[x] Completed` |
| **6.0 – 8.0** | Module 4: Networking, Reverse Eng, Browsers, DevOps | `interview-preparation/04-integrations-reverse-eng-browsers/` | `[x] Completed` |
| **8.0 – 9.5** | Module 5: System Design Whiteboard | `interview-preparation/05-system-design-whiteboard/` | `[x] Completed` |
| **9.5 – 10.0** | Module 6: Project Stories & Team Lunch | `interview-preparation/06-culture-lunch-and-storytelling/` | `[x] Completed` |

---

## 7. Change Log

- **2026-11-02 (Sessions 1–12):** Initialized context, git repo, and all `interview-preparation/` folders; synced paths after moving `resources/` and `ai-assitant-analysis/` into `docs/`.
- **2026-11-02 (Session 13 — B2 English, Short Bullet Lists & Basic Python Update):**
  - Updated all AI rules, `.md` guides, and `.py` files to use short bullet lists, Upper-B2 English, no code in `.md` files, and simple, well-commented basic Python code.
- **2026-11-04 (Session 14 — Dedicated `ai-workflow/` Study Folder):**
  - Created `interview-preparation/ai-workflow/` (`README.md` + `01` through `05`) covering Simin's real QueryLaw schema-check story (no RAG/fine-tuning), Harness Engineering, Antigravity IDE, Claude Code via OpenRouter in VS Code/CLI, GitHub Copilot Code Review flow, multi-agent parallel sessions, and word-for-word Upper-B2 Q&A scripts.
- **2026-11-04 (Session 15 — Merge AI Workflow into Module 1 & Add Company Guide):**
  - Merged `ai-workflow/` directly into `interview-preparation/01-ai-workflow-and-live-task/` as a single unified 7-guide module with hands-on Python sandbox.
  - Created `interview-preparation/COMPANY-AND-PRODUCT-GUIDE.md` detailing Ruit's mission, funding (€1M from Angels Capital/Decelera/Abac/Successful), €1M ARR 2027 goal, team (Luis Grau, Alonso Veliz Garcia), product capabilities (1-photo listing, inventory anti-double-sell sync, Chrome Extension + Celery workers), and exact role breakdown (**Senior Backend Engineer, Integrations**).
  - Updated `interview-preparation/README.md` with role reminder and links.
- **2026-11-04 (Session 16 — Elite Live AI Task Execution & Claude Code OpenRouter Showcase):**
  - Upgraded `05-laptop-setup-and-agentic-workflow-script.md` and `06-live-ai-coding-playbook.md` with minute-by-minute scripts on what to show and what to say out loud (Amateur Chatter vs Elite Harness Engineer).
  - Created `08-claude-code-openrouter-project-showcase.md` detailing the OpenRouter token setup, active project, `CLAUDE.md`, and custom commands in VS Code and terminal.
