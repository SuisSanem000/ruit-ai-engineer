# 01 — My Real AI Story & Daily Coding Workflow

> **Email Context:** Luis picked your application because you **ship real tools fast** (Dadroit VS Code extension in 3 days with 630K+ installs, and the 150-site news crawler). In Interview 1, he wants to see **how you actually work with AI every day**.

---

## 1. What I Did (And Did NOT Do) — My Honest Positioning

- **What I do NOT claim:**
  - I did **not** train models, do fine-tuning, build vector RAG pipelines, or deploy custom ML models on GPUs.
  - I have **not** used Python or Django in production (my 9+ years of backend production work are in Node.js, TypeScript, SQL, Redis, and Delphi).
- **What I ACTUALLY built in production with AI (My Real Resume Strengths):**
  - **QueryLaw (AI Legal Platform — 95%+ Accuracy via Strict Schema Checks):**
    - Legal answers cannot hallucinate or return broken formats.
    - I built a strict validation pipeline around the LLM using **prompt engineering**, **JSON Schema / AJV validation**, automated retry/repair loops when output failed the schema, and error logging.
    - This is the exact same pattern Ruit needs when turning product photos into structured marketplace listings or checking if a marketplace API changed its JSON.
  - **Parsaiane (News Crawler for 150+ Websites — 60K+ Daily Users):**
    - I built a crawler that scraped 150+ news sites, cleaned messy HTML/JSON into one standard format, and used the **OpenAI API** to summarize articles automatically.
  - **Dadroit JSON Generator (VS Code Extension — 630K+ Installs in 3 Days):**
    - Shows I deeply understand developer tools, VS Code extensions, JSON structures, and shipping fast.

---

## 2. My Daily AI Coding Workflow (In 5 Simple Steps)

- **Step 1 — Context First (Before Writing Any Code):**
  - I never start with a vague prompt like *"build this feature."*
  - I keep a living state file (`ai-state.md` or `CLAUDE.md` / `AGENTS.md`) that tells the agent the project architecture, rules, and what files we are touching.
- **Step 2 — Plan Mode Before Editing Files:**
  - In **Antigravity IDE** or **Claude Code** (in VS Code using my **OpenRouter token**), I ask the agent to read the relevant files first and propose a short step-by-step plan.
  - I check the plan in 1 minute and remove anything over-engineered before letting the agent write code.
- **Step 3 — Build in Small Slices with Strict Guardrails (Harness Engineering):**
  - I ask the agent to build **one small piece at a time** (for example: first the data schema, then the HTTP function, then the tests).
  - After every slice, the agent must run tests and linters (`pytest`/`vitest`, `ruff`/`eslint`, type checks) in the terminal.
- **Step 4 — Independent AI Code Review (GitHub Copilot Code Review):**
  - Before I commit, I open the Git diff in VS Code and run **GitHub Copilot Code Review** (and on GitHub PRs).
  - Having a second tool review the diff catches edge cases, missing error handling, or leftover debug code that the coding agent missed.
- **Step 5 — Update Project State & Git Commit:**
  - Once tests pass and I understand every line, I update the project state file and make a clean Git commit so I always have a safe checkpoint.

---

## 3. Why This Workflow Makes Me Fast in Python at Ruit

- **Architecture is language-agnostic:**
  - Designing retry queues, database row locks, rate limiters, and schema validators is the same in Python as in Node.js/TypeScript.
- **AI handles Python syntax; my harness guarantees quality:**
  - When coding in Python, I tell my agent to write **simple, readable Python** with clear comments and strict **Pydantic** types.
  - Then I verify it immediately with `pytest`, `ruff`, and `mypy` so I never ship code I don't understand or haven't tested.

