# Ruit Final Interview — Project Context & AI State

> **Last Updated:** 2026-11-02  
> **Interview Date:** Friday, November 6, 2026 (`12:45h` arrival $\rightarrow$ `13:00h–16:00h` @ Lanzadera, Valencia)  
> **Status:** All Modules (0–6) Updated to Short Bullet Lists, Upper-B2 English, and Basic Python Code

---

## 1. Company & Role Summary

- **Company:** Ruit (`https://ruit.es/en/`), based at Lanzadera in Valencia.
- **Interviewer:** Luis Grau (CEO) and the engineering team.
- **Product:** A tool that lets professional second-hand sellers list and manage products on many marketplaces (Wallapop, Vinted, eBay, Shopify, Depop, Vestiaire, etc.) from one place.
- **Role:** Senior Backend Engineer, Integrations (Python) + AI/Full-Stack Engineer.

---

## 2. Candidate Profile & Honest Python Positioning (Simin Shoeibi)

- **Main Strengths (9+ Years Experience):**
  - Built **Dadroit JSON Generator** VS Code extension in 3 days (630K+ installs) and worked on a desktop JSON Viewer (60K+ users).
  - Built a **news crawler for 150+ websites** (60K+ daily users) at Parsaiane with OpenAI summarization.
  - Built **QueryLaw's AI legal platform** (95%+ accuracy using prompt engineering, JSON Schema/AJV validation, and error monitoring).
  - Strong backend architecture experience in **Node.js/TypeScript**, PostgreSQL, Redis, RabbitMQ, Socket.IO (60K+ concurrent users), and Docker.
- **Honest Python & Django Positioning:**
  - Simin has **never used Python or Django in production**.
  - She has used Python in **basic side projects** and **reviewed Python syntax and Django concepts** for this interview.
  - She is 100% open about this. She answers architecture questions using her 9+ years of backend experience and writes **simple, basic Python** with the help of AI agents and tests.

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
    ├── README.md                               # Short index of all folders
    ├── 00-roadmap-and-quick-sheets/            # 10-hour plan, TS->Python bridge, train cheat sheet
    ├── 01-ai-workflow-and-live-task/           # Laptop demo guide, live task steps, basic Python sandbox
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
