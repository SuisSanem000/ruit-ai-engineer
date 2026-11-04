# 04 — Multi-Agents, Parallel Sessions, Skills & Plugins

> **Direct Match to Luis's Email Cheat Sheet:**
> *"And of course how do you work with AI: how do you use agents, skills, plugins... How do you use sessions in parallel, and so on."*

---

## 1. Clear Definitions: Agents vs. Rules vs. Skills vs. Plugins

If Luis asks how you organize your AI setup, explain these **4 building blocks**:

- **1. Agents ( & Subagents):**
  - Autonomous AI workers that can read files, edit code, and run terminal commands in a loop.
  - Instead of using one giant chat for everything, I use **specialized subagents**:
    - **Research Subagent (Read-Only):** Explores large folders, reads documentation, or inspects a big `.har` network log and returns a short 10-line summary. This keeps noisy data out of my main coding agent's memory.
    - **Main Coding Agent:** Takes that clean summary and writes the actual code and tests.
- **2. Rules (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`):**
  - Short, **always-on** rules loaded in every session (for example: *"Use Upper-B2 comments, validate all external JSON with Pydantic/AJV, never touch `docs/resources/`, run tests before finishing"*).
- **3. Skills (`skills/<name>/SKILL.md`):**
  - **On-demand playbooks** (progressive disclosure).
  - At the start of a chat, the agent only sees the skill's **name and 1-sentence description** so it doesn't waste tokens.
  - When I ask for a specific task (like *"create a new marketplace connector"* or *"check API schema drift"*), the agent automatically opens that `SKILL.md` file and follows its step-by-step checklist and templates.
- **4. Plugins & MCP Servers (`plugin.json` / `mcp_config.json`):**
  - A **Plugin** bundles related skills, rules, slash commands, and **MCP (Model Context Protocol)** tools into one installable package that the whole team can enable or disable with one click (for example: a GitHub/Linear plugin, a Postgres database inspector, or a Playwright browser tool).

---

## 2. How I Use Multiple Sessions & Agents in Parallel

Running 2 or 3 AI sessions at the same time is a huge speed boost—**if** you prevent them from editing the same file at the same time. Here are the **3 parallel patterns** I use:

### Pattern 1: Builder Agent + Test/Fixture Agent (2 Parallel Sessions)
- **Session A (Main Coding Agent):** Writes the implementation code (for example, `marketplace_connector.py`).
- **Session B (Test & Edge-Case Agent):** In parallel, reads the specification and sample JSON responses, and writes unit tests (`test_marketplace_connector.py`) covering `200 OK`, `429 Rate Limit`, `401 Unauthorized`, and broken schemas.
- **Merge Point:** Once both finish, I run `pytest` so Session A's code is immediately tested against Session B's independent tests.

### Pattern 2: Main Feature Work + Background Research Subagent
- While my **Main Session** is coding a feature, if I hit an unfamiliar library or need to inspect a 5,000-line JSON payload from Vinted or Wallapop, I spawn a **Research Subagent** (or second session) to analyze the payload and extract the exact fields.
- I keep coding in the main session without waiting, and when the research agent finishes, I paste only the clean 15-line schema into my main session.

### Pattern 3: Parallel Features Using Separate Folders or `git worktree`
- When working on two independent tasks at the same time (for example, fixing a bug on the **Vinted** connector while scaffolding a new **Wallapop** connector):
  - I open two separate VS Code / Antigravity windows—either in separate module folders or using **`git worktree add ../ruit-hotfix hotfix-branch`**.
  - Because each agent has its own isolated working directory (or folder) and its own terminal, they can run tests in parallel without creating Git conflicts or overwriting each other's files.

---

## 3. My Golden Rule for Multi-Agent & Parallel Work

- **Never let two agents edit the exact same file at the same time.**
- **Keep one shared state file (`ai-state.md`):** Each task has a clear owner and checklist, and every finished step is committed to Git immediately.

