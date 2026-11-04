# 05 — Laptop Setup & AI Workflow Walkthrough Script

> **From Luis's Email:** *"We will ask you to fire up your laptop, show us your setup and complete a brief task with AI ... how do you use agents, skills, plugins... How do you use sessions in parallel, and so on."*

---

## 1. Laptop Layout & 5-Minute Checklist (Before Entering Lanzadera)

- **Power & Wi-Fi:** Charge laptop to 100% and have your phone hotspot tested and ready.
- **Do Not Disturb:** Turn on macOS Do Not Disturb so no notification banners appear while sharing your screen.
- **Window Layout to Have Open:**
  - **Window 1 (Antigravity IDE):** Open to this `ruit-ai-engineer` project. Sidebar shows `docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md` and the terminal with `.venv` active.
  - **Window 2 (VS Code with Claude Code via OpenRouter):** Open to a project folder with `CLAUDE.md`, showing the Claude Code panel and terminal connected via your OpenRouter API token.
  - **Window 3 (Git Source Control tab):** Showing pre-commit diffs and the GitHub Copilot Code Review button.
- **Offline Readiness:** The virtual environment (`.venv`) already has `pytest`, `pydantic`, `httpx`, `ruff`, and `mypy` installed so tests run instantly even if the office Wi-Fi is slow.

---

## 2. The 3-Minute Walkthrough: What to Show & What to Say

When Luis says, *"Show us your setup and how you work with AI,"* follow this exact 3-minute script:

### Step 1: Show the Context & State File (Minute 0:00 – 0:45)
- **What to Show on Screen:** Open `docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md`.
- **What to Say Out Loud (Upper-B2):**
  > *"I don't just open a chat box and start typing code. Professional AI development requires what I call **Harness Engineering**. Before I write any code, I maintain a living state file like `ai-state.md`. It holds the project architecture, strict boundaries, and an active task checklist. Every AI session reads this first so the model never loses context or hallucinates existing files."*

### Step 2: Show Antigravity IDE & Specialized Subagents (Minute 0:45 – 1:30)
- **What to Show on Screen:** Show the Antigravity agent panel and point to skills and rules.
- **What to Say Out Loud (Upper-B2):**
  > *"Here in **Antigravity IDE**, I use specialized subagents instead of one giant chat. For example, if I need to analyze a 5,000-line marketplace JSON payload or browse docs, I launch a read-only **Research Subagent**. It returns a short 10-line summary so my main coding session stays clean, fast, and token-efficient. I also use **Skills (`SKILL.md`)** for multi-step playbooks like scaffolding a new marketplace connector, which loads on demand without cluttering the prompt."*

### Step 3: Show Claude Code via OpenRouter Token in VS Code (Minute 1:30 – 2:15)
- **What to Show on Screen:** Switch to VS Code and show the Claude Code terminal and `CLAUDE.md`.
- **What to Say Out Loud (Upper-B2):**
  > *"In addition to Antigravity, I recently set up **Claude Code** running through my **OpenRouter API token** in VS Code and in my terminal. I use this daily for headless tasks and terminal commands. I configure it with a `CLAUDE.md` file for project rules, use **Plan Mode (`Shift + Tab`)** to approve architecture before any edits, and use custom slash commands in `.claude/commands/` for reusable validation workflows."*

### Step 4: Show the Pre-Commit Copilot Review & Verification Loop (Minute 2:15 – 3:00)
- **What to Show on Screen:** Show the terminal running `.venv/bin/pytest` (all green) and the Git diff tab with GitHub Copilot Review.
- **What to Say Out Loud (Upper-B2):**
  > *"My rule is that the AI never writes code in a vacuum. After every edit, the agent runs `pytest`, `ruff`, and `mypy` in the terminal in an automated loop. And before I commit, I run **GitHub Copilot Code Review** on the Git diff as an independent second model to catch subtle bugs or missing timeouts. That way, what reaches Git is verified, well-commented, and production-ready."*
