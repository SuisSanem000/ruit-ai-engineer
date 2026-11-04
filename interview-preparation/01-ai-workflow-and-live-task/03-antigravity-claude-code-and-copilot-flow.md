# 03 — My AI Tool Stack: Antigravity IDE, Claude Code (OpenRouter), & Copilot Review

> **What You Use Every Day:**
> 1. **Antigravity IDE** (Agents, Skills, Rules, Subagents, Inline Edits)
> 2. **Claude Code in VS Code & Terminal** (Connected via your **OpenRouter token**, using `CLAUDE.md`, custom commands, and skills)
> 3. **GitHub Copilot Code Review** (Reviewing diffs in VS Code and Pull Requests before merging)

---

## 1. How I Use Antigravity IDE

- **Three Ways I Interact with AI in Antigravity:**
  - **Sidebar Agent & Planning Mode:** For multi-file tasks. The agent reads files, proposes a plan, edits code, and runs terminal tests (`pytest`, `ruff`, `mypy`) in a loop until they pass.
  - **Inline Command (`Cmd + I`):** For quick, targeted changes—I highlight one function and ask it to add comments, simplify logic, or add error handling without touching the rest of the file.
  - **Supercomplete (`Tab`):** Predicts my next edit or auto-imports packages as I type.
- **Project State & Context Files (What You Can Show Live on Your Laptop):**
  - Show Luis your [`ai-state.md`](../../docs/ai-assitant-analysis/the-context-of-the-project/ai-state.md) and [`master-prompt.md`](../../docs/ai-assitant-analysis/the-context-of-the-project/master-prompt.md) inside this repo.
  - Explain: *"Whenever I work on a project in Antigravity, I keep an `ai-state.md` file so if I start a new session or compact the chat, the agent immediately knows the project state, folder structure, and strict rules."*
- **Built-in Slash Commands I Use in Antigravity:**
  - `/plan` — Forces the agent to align on a step-by-step plan before touching code.
  - `/compact` — Summarizes a long conversation so the context window stays fast and accurate.
  - `/learn` — Saves a correction or rule so the agent remembers it next time.

---

## 2. How I Use Claude Code (In VS Code & Terminal via OpenRouter Token)

- **How My OpenRouter Setup Works:**
  - I run **Claude Code** inside **VS Code** (and in the terminal) connected through my **OpenRouter API token** by setting:
    - `ANTHROPIC_BASE_URL="https://openrouter.ai/api"`
    - `ANTHROPIC_AUTH_TOKEN="<my-openrouter-api-key>"`
  - **Why this is great:** It lets me use Claude Code's agentic workflow (file editing, bash tool execution, subagents, VS Code diff view) while routing requests through OpenRouter with full control over usage, budgets, and model selection.
- **Key Features I Use in Claude Code:**
  - **`CLAUDE.md` (Project Memory):** Lives at the root of the repo. Stores the tech stack, test commands, folder layout, and coding rules so Claude loads them automatically at the start of every session.
  - **Plan Mode (`Shift + Tab`):** Switches Claude Code into read-only planning mode first so it explores the codebase and agrees on the design with me before making edits.
  - **Built-in Slash Commands:**
    - `/init` — Scans a repo and generates the initial `CLAUDE.md` file.
    - `/compact` — Compresses chat history when context gets above 60–70% full so the model stays sharp.
    - `/clear` — Wipes context cleanly when switching to a brand-new task.
    - `/review` — Reviews current changes or a pull request for bugs.
  - **Custom Slash Commands (`.claude/commands/*.md`):**
    - Reusable markdown prompt templates stored in `.claude/commands/`.
    - Example: `.claude/commands/check-schema.md` or `/fix-tests`—typing `/check-schema` runs our standard validation and test checklist without retyping a long prompt.
  - **Claude Skills (`.claude/skills/<skill-name>/SKILL.md`):**
    - Folders containing a `SKILL.md` instruction file (plus optional helper scripts or templates).
    - Unlike `CLAUDE.md` (which is loaded every time), **Skills load on-demand** only when the task needs them—keeping the context window small and cheap.

---

## 3. How I Use GitHub Copilot Code Review Flow

- **Why I Use a Separate AI for Code Review:**
  - When one AI agent writes code, it can be blind to its own mistakes. Using **GitHub Copilot Code Review** gives me an independent second check before I commit or merge.
- **Step 1 — Local Pre-Commit Review in VS Code:**
  - After Claude Code or Antigravity finishes a task and tests pass, I open the **Source Control (Git) tab in VS Code**.
  - I click the **Copilot Code Review** button on my staged/unstaged changes.
  - Copilot highlights inline issues directly in the editor diff (for example: an unhandled `None`/`null` value, missing timeout on an HTTP call, or an accidental hardcoded value), and I can apply or dismiss each comment in one click.
- **Step 2 — Pull Request Review on GitHub:**
  - When I open a Pull Request, I assign **Copilot** as a reviewer.
  - Copilot reads our repo rules (`.github/copilot-instructions.md`), checks the full PR diff, leaves line-by-line review comments, and suggests exact code fixes before a human teammate even looks at the PR.
- **How to Summarize This to Luis:**
  > *"I use Antigravity and Claude Code (via OpenRouter in VS Code) as my **builders**, and I use **GitHub Copilot Code Review** as my **automated reviewer** on every Git diff before committing. That way, my teammates only review clean, pre-checked code."*
