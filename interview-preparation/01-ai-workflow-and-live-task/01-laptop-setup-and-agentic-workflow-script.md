# Laptop Setup & AI Workflow Script (Interview 1)

> **What Luis Asked in the Email:**  
> - *"We will ask you to fire up your laptop, show us your setup and complete a brief task with AI."*  
> - *"And of course how do you work with AI: how do you use agents, skills, plugins... How do you use sessions in parallel, and so on."*

---

## 1. Laptop Checklist Before Entering the Office (12:45h)

- Charge your laptop to 100% and keep your phone hotspot ready as backup Wi-Fi.
- Turn on **Do Not Disturb** so no personal messages pop up on screen.
- Open your code editor in this project folder (`ruit-ai-engineer`).
- Keep your terminal open at the root folder (`.venv` is already installed here so `pytest` works offline).

---

## 2. How to Show Your Setup in 3 Minutes (Bullet Script)

### Step A: Show How You Keep Project Context (`ai-state.md` & `master-prompt.md`)
- **What to show:** Open [`ai-state.md`](../../docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md).
- **What to say:**
  - *"Before I ask an AI agent to write code, I create a state file (`ai-state.md`) and a master prompt."*
  - *"This file tracks the project goals, folder structure, rules, and current progress."*
  - *"Every time an agent finishes a step, it updates this state file and makes a Git commit. That way, if I start a new chat session, the AI never loses context."*

### Step B: Explain How You Use Skills, Rules, and Plugins
- **Rules (Always Active):**
  - Short instructions that the AI must follow on every turn.
  - Example: *"Keep Python code simple and easy to read, add clear comments, run `pytest` after every change, and commit to Git."*
- **Skills (`SKILL.md` — Loaded When Needed):**
  - Step-by-step guides for specific repeatable tasks.
  - Example for Ruit: A skill for **building a marketplace integration** (1. check raw JSON payload, 2. create a basic Pydantic model to validate fields, 3. write an HTTP function with timeouts and retries, 4. write `pytest` tests).
- **Plugins / MCP Servers:**
  - Tools that let the AI agent read documentation, inspect browser pages (DevTools/Playwright), or run terminal tests directly instead of guessing.

### Step C: Explain How You Run Agent Sessions in Parallel
- **Why run sessions in parallel:** One single chat window gets slow and messy if you ask it to research, code, and write tests all at the same time.
- **How you split work across 3 parallel sessions / subagents:**
  - **Session 1 (Research Agent):** Looks at the raw API network traffic or JSON sample, finds the required headers, and lists tricky fields (like prices formatted as strings).
  - **Session 2 (Coding Agent):** Writes the main Python function and Pydantic data model.
  - **Session 3 (Testing Agent):** Writes `pytest` tests for normal responses, broken JSON, and `429` rate limits.
- **How you avoid conflicts:**
  - First, you agree on the **input and output data shape** (for 2 minutes) before starting the parallel sessions.
  - For bigger features, you can also use **separate Git branches / worktrees** so two agents never edit the same file at the same time.
