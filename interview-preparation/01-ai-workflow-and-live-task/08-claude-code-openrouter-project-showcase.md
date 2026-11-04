# 08 — Claude Code + OpenRouter Project Showcase: What to Show & What to Say

> **Why This Impresses Luis & the Team:** Most candidates only use web chat or basic autocomplete. Showing that you set up **Claude Code in VS Code & terminal routed through an OpenRouter token** proves you are an advanced AI engineer who understands API gateways, custom tooling, and model orchestration.

---

## 1. Why You Use Claude Code with OpenRouter (The Strategy)

- **Why OpenRouter Token Routing:**
  - OpenRouter gives you a single API gateway with unified billing, budget limits, and access to top models (Claude 3.7 Sonnet, Claude 3.5 Sonnet) without being tied to a single provider subscription.
  - By pointing Claude Code's Anthropic endpoint to OpenRouter, you get the full terminal agent power of Claude Code (file editing, subagents, diffs, bash tool) powered by your OpenRouter balance.
- **How It Is Configured on Your Mac:**
  - Exported in your environment (`~/.zshrc`):
    - `export ANTHROPIC_BASE_URL="https://openrouter.ai/api"`
    - `export ANTHROPIC_AUTH_TOKEN="<your-openrouter-key>"`
  - You invoke it either in the terminal with `claude` or inside the VS Code Claude Code extension.

---

## 2. What Project to Talk About

- **The Project:** An **API Schema Drift & Marketplace Response Monitor**.
  - A tool that takes sample responses from e-commerce/marketplace endpoints, validates them against expected Pydantic models, and alerts when new fields or changed structures appear.
- **The Repo Structure You Can Show:**
  - **`CLAUDE.md` (Project Memory at Root):**
    - Contains instructions on Python version, virtual environment path, test commands (`pytest`), and coding rules (e.g., *"Use basic Python with explanatory comments and Pydantic validation"*).
  - **Plan Mode:**
    - Used via `Shift + Tab` before running any multi-file task so the model explains its plan first.
  - **Custom Slash Commands (`.claude/commands/`):**
    - `.claude/commands/check-schema.md`: Reusable prompt to compare incoming JSON against Pydantic schemas.
    - `.claude/commands/run-lint-test.md`: Runs `pytest` and `ruff` and fixes errors automatically.
  - **On-Demand Skills (`.claude/skills/`):**
    - Specific playbooks that only load when asked, saving tokens and keeping context small.

---

## 3. What to Show on Screen (Step-by-Step)

If Luis asks about your Claude Code setup, switch to VS Code and show these **3 things**:

1. **Show the `CLAUDE.md` file:**
   - Point out how clear, structured rules keep the agent on track without repeating long prompts.
2. **Show the Claude Code CLI in the Terminal:**
   - Show how you launch `claude` in your terminal and how it reads `CLAUDE.md` on startup.
3. **Show Plan Mode (`Shift + Tab`) or a Custom Command:**
   - Show how Plan Mode ensures the agent investigates the codebase in read-only mode first.

---

## 4. What to Say Out Loud (Spoken Upper-B2 Script)

> *"Along with Antigravity IDE, I recently set up **Claude Code** running through my **OpenRouter API token** in both VS Code and my terminal.*
>
> *I like routing through OpenRouter because it gives me full control over usage, cost tracking, and model selection through a single API gateway.*
>
> *In my project, I use three key features of Claude Code:*
> *First, **`CLAUDE.md`** at the project root acts as the memory bank. It tells the agent our architecture, test commands, and coding rules so I never have to repeat myself.*
> *Second, **Plan Mode** (`Shift + Tab`). Before letting the agent touch any files, I make it explore the codebase in read-only mode and propose a plan that I approve.*
> *And third, **Custom Slash Commands** in `.claude/commands/`. I created reusable prompt templates—like `/check-schema` and `/run-lint-test`—so complex multi-step validations run with a single command.*
>
> *Combined with Antigravity and Copilot Code Review, this gives me a complete agentic workflow that is fast, safe, and disciplined."*
