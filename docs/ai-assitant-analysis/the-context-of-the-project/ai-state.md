# Ruit Final Interview Prep — Project Context & AI State

> **Last Updated:** 2026-11-02  
> **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival, `13:00h–16:00h` interviews)  
> **Location:** Ruit Office @ Lanzadera, Valencia (Train from Barcelona)  
> **Status:** All modules (`00` to `06`) rewritten in concise Upper-B2 English with basic, well-commented Python code files.

---

## 1. Company & Interview Context (From `docs/resources/first emails.md`)

- **Company:** **Ruit** (`ruit.es`), based at Lanzadera in Valencia.
- **CEO & Interviewer:** **Luis Grau** (`luis.grau@ruit.es`) and the engineering team.
- **Product:** A tool that lets professional second-hand sellers list, manage, and sell on every marketplace (Wallapop, Vinted, eBay, Depop, Vestiaire, etc.) from one place.
- **Role:** **Senior Backend Engineer, Integrations (Python)** (and considered across AI/full-stack roles).
- **Why Luis Invited Simin:**
  - Built the **Dadroit JSON Generator** VS Code extension in 3 days (**630K+ installs**).
  - Built the **crawler behind a news app for 150+ sites** (**60K+ DAU**).
  - Strong AI validation and backend systems experience at **QueryLaw** and **Parsaiane**.

---

## 2. Simin's Honest Positioning on Python & Django

- **Be 100% open and honest:** You have **never used Python or Django in production**.
- **Your real strength:** 9+ years of production backend, database, queue, crawler, and AI experience using **TypeScript/Node.js, SQL (PostgreSQL), Redis, RabbitMQ, and Delphi**.
- **Your Python level:** You know core backend concepts deeply, you use Python in basic side projects, and you reviewed Python & Django syntax and concepts for this interview.
- **Why this works with AI:** Because your system design and debugging fundamentals are strong, you guide AI agents effectively and read/verify simple, clean Python code easily.

---

## 3. Friday Onsite Schedule & Luis's Cheat Sheet

- **12:45 – 13:00 | Arrival & Office Tour:** Arrive at Lanzadera. Your sister can wait at the office.
- **13:00 – 14:00 | Interview 1 (45–60 min):**
  - **Part A:** Open laptop, show your AI setup, and complete a short task with AI.
  - **Part B:** Chat about concepts from Luis's cheat sheet:
    - **Fundamentals:** Concurrency, async, JSON validation, ORMs & SQL, background queues & brokers (Celery & Redis), HTTP clients & TLS, error handling philosophy (Python vs Go vs Rust), databases & cache, low-level networking & protocols (HTTP, WebSockets), API integrations & reverse engineering, browsers/automations & Chrome extensions, DevOps (Linux, Docker, Compose, deployments, zero-downtime), observability (metrics, logs, traces), scaling.
    - **Python & Django:** The GIL, async in Django, generators, and making robust Python (type hints, static analysis).
    - **Working with AI:** How you use agents, skills, plugins, and parallel sessions.
- **14:00 – 15:00 | Team Lunch (60 min):** *"This is the most important part. It's on the house."*
- **15:00 – 16:00 | Interview 2 — System Design (60 min):** Pick 1 of ~5 real Ruit challenges for the coming months and design it together on the whiteboard (*"This is teamwork!"*).

---

## 4. Mandatory Rules for AI Assistant

1. **Never Touch `docs/resources/`:** Strictly read-only.
2. **Email Cheat Sheet First:** Prioritize `docs/resources/first emails.md` over any other file. Only keep job-ad details if they directly relate to the email cheat sheet.
3. **Writing Style (Upper-B2 & Short Bullet Lists):**
   - Keep all `.md` and `README.md` files as **short as possible** using **bullet lists** and **short sentences**.
   - Use natural **Upper-B2 English** (clear, simple words that are easy to read and speak out loud), while keeping explanations descriptive enough to understand the concept fully.
4. **Code Rules (Basic Python Only, Inside `.py` Files Only):**
   - **Do NOT put code blocks inside `.md` files.** Put all code inside `.py` files.
   - Write all Python code at a **basic, simple level** (simple functions, basic classes, simple loops, basic `try/except`, basic `async/await`) matching someone who only used Python in basic side projects.
   - Put **clear, detailed comments inside every `.py` file** explaining what each part of the code does and why.
5. **State & Git Commits:** Update this `ai-state.md` file and run `git add -A && git commit -m "..."` after every change.

---

## 5. Workspace Structure & Progress Tracker

```text
ruit-ai-engineer/
├── docs/
│   ├── resources/                              # [READ-ONLY]
│   └── ai-assitant-analysis/
│       └── the-context-of-the-project/
│           ├── ai-state.md                     # Project state & rules
│           └── master-prompt.md                # Master prompt
└── interview-preparation/
    ├── README.md                               # Short index of all modules
    ├── 00-roadmap-and-quick-sheets/            # 10h plan, TS->Python bridge, train cheat sheet
    ├── 01-ai-workflow-and-live-task/           # Laptop demo guide, live task steps, basic Python sandbox
    ├── 02-python-and-django-deep-dive/         # GIL, Async Django, Generators, Typing + basic Python labs
    ├── 03-backend-fundamentals-cheatsheet/     # Celery/Redis, SQL/Cache, Error handling + basic Python labs
    ├── 04-integrations-reverse-eng-browsers/   # HTTP/TLS, Reverse eng, Playwright/Extensions, DevOps
    ├── 05-system-design-whiteboard/            # Whiteboard guide + 5 Ruit system design challenges
    └── 06-culture-lunch-and-storytelling/      # Your 3 stories + lunch tips & questions
```

| Hours | Module | Status |
| :--- | :--- | :--- |
| **1–2** | `01-ai-workflow-and-live-task/` | `[x] Completed (Short B2 MD + Basic Commented Python)` |
| **2–4** | `02-python-and-django-deep-dive/` | `[x] Completed (Short B2 MD + Basic Commented Python)` |
| **4–6** | `03-backend-fundamentals-cheatsheet/` | `[x] Completed (Short B2 MD + Basic Commented Python)` |
| **6–8** | `04-integrations-reverse-eng-browsers/` | `[x] Completed (Short B2 MD)` |
| **8–9.5** | `05-system-design-whiteboard/` | `[x] Completed (Short B2 MD)` |
| **9.5–10** | `06-culture-lunch-and-storytelling/` | `[x] Completed (Short B2 MD)` |

---

## 6. Changelog

- **2026-11-02 (Sessions 1–12):** Initialized repo, created context/prompt files, built `interview-preparation/`, and synced `docs/` move.
- **2026-11-02 (Session 13 — Upper-B2 Short Bullet Rewrite & Basic Python Refactor):**
  - Updated `ai-state.md` and `master-prompt.md` with Simin's 4 new rules (short bullet-list `.md` files, Upper-B2 English, no code in `.md` files, and basic heavily-commented Python in `.py` files reflecting her honest side-project Python level).
