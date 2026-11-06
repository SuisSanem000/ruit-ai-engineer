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

## 3. Consolidated Workspace Structure

```text
ruit-ai-engineer/
├── README.md                                   # Master interview showcase ("Look how I used Harness Engineering")
├── CLAUDE.md                                   # Root rules, architectural constraints & memory
├── AGENTS.md                                   # Multi-agent roles, subagent hierarchy & write-lock rules
├── .claude/
│   └── commands/                               # Custom Claude Code slash commands (/review, /validate, /plan)
├── skills/                                     # On-demand specialized playbooks (loaded progressively)
│   ├── marketplace-connector/SKILL.md          # Scaffolding connector with schemas & connection pooling
│   └── traffic-reverse-engineering/SKILL.md    # Parsing .har captures & detecting schema drift
├── ai-workflow/                                # Step-by-step live interview playbook (zero code)
│   ├── README.md                               # 4-part interview guide
│   ├── 01-show-laptop-setup.md                 # 4 things to show on screen in first 5 mins
│   ├── 02-live-task-playbook.md                # 6 chronological steps for 20-min task
│   ├── 03-agents-skills-parallel-sessions.md   # Spoken explanations (agents, skills, worktrees)
│   └── 04-my-real-ai-resume-story.md           # QueryLaw schema gates, Dadroit, Parsaiane
├── multi-agent-worktree-orchestrator/          # Production 16-agent Git worktree prototype
│   ├── README.md                               # Architecture diagram, 5 technical Q&As, cheatsheet
│   ├── setup.sh                                # Automation script
│   └── src/ (worktree, orchestrator, merge, logger)
├── interview-preparation/                      # Consecutive systems design & 5 Ruit whiteboard challenges
│   ├── README.md                               # Consolidated index & study progress tracker
│   ├── COMPANY-AND-PRODUCT-GUIDE.md            # Master company, product, funding & team guide
│   ├── 00-roadmap-and-quick-sheets/            # Positioning, 10-hour schedule, train cheat sheet
│   ├── 01-backend-fundamentals/                # Celery, Redis caching, SELECT FOR UPDATE locking
│   ├── 02-networking-and-reverse-eng/          # TCP, HTTP/1-2-3, WebSockets, TLS JA3/JA4, Chrome MV3
│   ├── 03-system-design-whiteboard/            # 4-step framework + the 5 real Ruit challenges
│   └── 04-culture-lunch-and-storytelling/      # 3 STAR stories, lunch prep, questions for Luis
└── docs/
    ├── ai-assitant-analysis/
    │   └── the-context-of-the-project/
    │       ├── ai-state.md                     # Living project state across all sessions
    │       └── master-prompt.md                # Master context prompt
    └── resources/                              # [READ-ONLY — NEVER TOUCH]
```

---

## 4. Study Progress Tracker

| Section | Core Files | Status |
| :--- | :--- | :--- |
| **Root Interview Showcase** | `README.md` & `CLAUDE.md` | `[x] READY TO SHOW` |
| **AI Workflow Playbook** | `ai-workflow/` (Files 01, 02, 03, 04) | `[x] PRIMARY FOR TODAY` |
| **16-Agent Worktree Prototype** | `multi-agent-worktree-orchestrator/` | `[x] RUNNABLE DEMO` |
| **Company & Role Guide** | `COMPANY-AND-PRODUCT-GUIDE.md` | `[x] COMPLETED` |
| **0. Roadmap & Quick Sheets** | `00-roadmap-and-quick-sheets/` (Files 00, 01, 02) | `[x] COMPLETED` |
| **1. Backend Fundamentals** | `01-backend-fundamentals/` (Files 01, 02) | `[x] COMPLETED` |
| **2. Networking & Reverse Eng** | `02-networking-and-reverse-eng/` (Files 01, 02) | `[x] COMPLETED` |
| **3. System Design Whiteboard** | `03-system-design-whiteboard/` (Files 01, 02) | `[x] COMPLETED` |
| **4. Stories & Team Lunch** | `04-culture-lunch-and-storytelling/` (File 01) | `[x] COMPLETED` |
| **5. Stories & Team Lunch** | `06-culture-lunch-and-storytelling/` (File 01) | `[x] COMPLETED` |

---

## 5. Change Log

- **2026-11-06 (Session 22 — Root Showcase README & Unified Harness Engineering Alignment):**
  - Created root `README.md` and `CLAUDE.md` showcasing how Simin used Harness Engineering to prepare for this exact interview.
  - Aligned `interview-preparation/README.md` and roadmap schedules with `ai-workflow-step-by-step/` (left 100% untouched as requested) and `multi-agent-worktree-orchestrator/`.
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
