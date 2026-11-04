# Laptop Setup & How You Work with AI

> **From Luis's Email:** *"We will ask you to fire up your laptop, show us your setup and complete a brief task with AI ... how do you use agents, skills, plugins... How do you use sessions in parallel, and so on."*  
> **Study Context:** This guide walks you through the exact 3-minute screen-sharing walkthrough to present your AI setup to Luis. For deep dives on Harness Engineering and tools, see files `01` through `04` in this folder.

---

## 1. Before You Enter the Office (5-Minute Checklist)

- Charge your laptop to 100% and keep your phone hotspot ready as backup Wi-Fi.
- Turn on **Do Not Disturb** so no personal messages pop up while sharing your screen.
- Open this project in your editor with the terminal ready (`.venv` already has `pytest`, `pydantic`, `httpx`, `ruff`, and `mypy` installed so it works even without internet).

---

## 2. How to Show Your AI Setup (3-Minute Walkthrough)

- **Step 1 — Project Context & State File (`ai-state.md`):**
  - Show [`ai-state.md`](../../docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md).
  - Explain: *"Before I ask AI to write code, I create a state file that lists the project context, folder rules, and task checklist. Every AI session reads this file first and updates it after finishing a step, so the AI never loses track of what we are building."*
- **Step 2 — Master Prompt & Rules (`master-prompt.md`):**
  - Show [`master-prompt.md`](../../docs/ai-assitant-analysis/the-context-of-the-project/master-prompt.md).
  - Explain: *"I set strict rules for the AI: keep code simple, write clear comments inside the code files, run automated tests after every change, and make a small Git commit after each step."*
- **Step 3 — Skills (`SKILL.md`) & Plugins (MCPs):**
  - **Skills:** Reusable instruction files (`SKILL.md`) for tasks you repeat often—like turning a raw marketplace JSON response into a validated Python model with retry logic and tests.
  - **Plugins / MCPs:** Tools that let the AI read documentation, inspect browser pages (DevTools/Playwright), and run terminal tests directly.
- **Step 4 — Running AI Sessions in Parallel:**
  - Explain how you split work so multiple AI sessions do not overwrite each other's files:
    - **First, agree on the data shape:** Spend 2 minutes defining the input/output fields.
    - **Session 1 (Research / Traffic Analysis):** Reads raw API JSON or network logs and lists edge cases (like missing fields, price formats, or rate-limit headers).
    - **Session 2 (Main Code):** Writes the API client and validation logic.
    - **Session 3 (Testing):** Writes `pytest` tests for normal cases, broken JSON, `429` rate limits, and `401` login errors.
    - **Git Worktrees for Bigger Features:** When working on two separate marketplace integrations at the same time, run each AI session in its own Git branch/folder (`git worktree`) so their files and tests stay completely separate.
- **Step 5 — Always Verify & Review AI Code:**
  - Explain: *"Because I am open that my production background is Node.js/TypeScript and my Python is from basic side projects, I use AI to write the Python syntax fast, and then I apply my senior backend checklist: I check timeouts, retry loops, error handling, and run `pytest` and `ruff` to prove the code works."*
