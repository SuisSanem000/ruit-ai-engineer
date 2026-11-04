# 02 — Multi-Agents, Laptop Setup & Elite Live Task Playbook

> **Interview 1 Goals (45–60 mins):** Screen share your AI setup (3 mins), complete a live task with AI (20 mins), and answer technical fundamentals.

---

## 1. Multi-Agent Workflows & Parallel Sessions

- **Core Building Blocks:**
  - **Rules (`CLAUDE.md`, `AGENTS.md`):** Always-on guidelines loaded every session (formatting, test commands, rules).
  - **Skills (`SKILL.md`):** On-demand playbooks. Only name and description load initially; full instructions load only when needed (saves 90% of tokens).
  - **Plugins / MCPs:** Bundle skills, rules, and external tool servers (database inspector, browser tool).
- **3 Parallel Session Patterns (Without Conflicts):**
  - **Pattern 1 (Builder + Tester):** Session A writes the connector implementation while Session B writes `pytest` unit tests with offline mock fixtures.
  - **Pattern 2 (Coder + Research Subagent):** Main agent codes the feature while a read-only research subagent parses a giant `.har` file and returns a 10-line schema summary.
  - **Pattern 3 (Separate Features / Hotfixes):** Use separate workspace folders or `git worktree` so parallel agents run tests independently without Git collisions.
- **The Golden Rule:** Never let two agents edit the same file simultaneously.

---

## 2. The 3-Minute Laptop Walkthrough Script (What to Show & Say)

- **Minute 1 — Project Context & State:**
  - *Show:* `ai-state.md` and `master-prompt.md`.
  - *Say:* *"I don't just chat with AI. I practice Harness Engineering. I maintain a living state file with architecture and tasks so the agent always knows the project state and strict rules."*
- **Minute 2 — Antigravity & Claude Code (OpenRouter):**
  - *Show:* Antigravity IDE with specialized subagents, then switch to VS Code showing Claude Code CLI with `CLAUDE.md`.
  - *Say:* *"Here in Antigravity, I use research subagents and on-demand skills. In parallel, I run Claude Code through an OpenRouter API token for terminal workflows and custom commands."*
- **Minute 3 — Automated Verification Loop & Copilot Review:**
  - *Show:* Terminal running green tests and the Git diff tab with Copilot Code Review.
  - *Say:* *"The agent executes tests in the terminal autonomously. Before committing, I run Copilot Code Review on the diff as an independent second model to catch edge cases."*

---

## 3. The 20-Minute Live Task: Senior Harness Engineer vs. Amateur Chatter

| What the Amateur Chatter Does (Avoid) | What You Do as an Elite AI Engineer (Your Playbook) |
| :--- | :--- |
| Types a prompt immediately into chat. | Asks 2 clarifying questions first about failure modes (`401`, `429`) and concurrency. |
| Writes logic before knowing the data shape. | Defines strict **Pydantic models and custom error classes** first. |
| Manually copies and pastes terminal errors back and forth. | Lets the agent run tests and linters in the terminal and **self-correct autonomously**. |
| Tests manually by making live web requests. | Tests completely offline using **`httpx.MockTransport`** fixtures. |
| Blindly accepts AI code without checking. | Audits the code out loud for **timeouts, connection pools, and blocking calls**. |
| Leaves messy, untested files. | Runs **Copilot Code Review** on the Git diff and makes a clean, atomic Git commit. |

### The 5 Senior Code Audit Checks to Mention Out Loud:
1. **Connection Pooling:** Reuse a single `httpx.AsyncClient` session (avoid creating clients inside loops).
2. **Explicit Timeouts:** Set connection and read timeouts on every HTTP call.
3. **No Silent Exceptions:** Catch specific custom exceptions (`RetryableError`, `AuthExpiredError`), never bare `except Exception: pass`.
4. **Non-Blocking Sleep:** Use `await asyncio.sleep()`, never blocking `time.sleep()`.
5. **Idempotency on Retries:** Send unique idempotency keys on non-idempotent calls (`POST`).

