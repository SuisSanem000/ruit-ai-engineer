# 05 — Interview Q&A Script: Questions Luis Will Ask About AI & My Ready Answers

> **How to Practice:** Read each question and speak the answer out loud in your own natural voice. All answers are written in clear **Upper-B2 English** and match your real experience.

---

## Q1: "Walk us through how you work with AI on a daily basis when coding."

**Your Answer:**
> *"I work with AI every day using a structured workflow that I call **Harness Engineering**. I don't just type a vague prompt and copy-paste code. Instead, I use three main tools together:*
> *1. **Antigravity IDE** and **Claude Code in VS Code** (which I connect through my **OpenRouter token**) as my main coding agents.*
> *2. A living project state and rules file—like `CLAUDE.md` or `ai-state.md`—so the agent always knows our architecture and rules before it touches any file.*
> *3. **GitHub Copilot Code Review** as an independent reviewer on my Git diffs before I commit.*
>
> *For every feature, I start in **Plan Mode** to agree on a small step-by-step plan, define the data schemas first, let the agent write the code and run tests in the terminal until they pass, and then review the diff with Copilot before committing."*

---

## Q2: "On your resume, you worked with AI at QueryLaw and Parsaiane. Did you do RAG, fine-tuning, or model deployment?"

**Your Answer:**
> *"I want to be 100% transparent: I did not do fine-tuning, vector RAG pipelines, or ML model deployment. My experience is on the **application and reliability engineering side of AI**.*
>
> *At **Parsaiane**, I built a news crawler for over **150 websites** serving 60,000 daily users, where we cleaned messy HTML/JSON from all those sites and integrated the OpenAI API to summarize articles.*
>
> *And at **QueryLaw**, our legal platform needed 95%+ accuracy because legal tools cannot afford hallucinated or broken JSON outputs. So I built a strict **validation harness** around the LLM: structured prompts, **JSON Schema and AJV validation checks** on every response, automated retry loops when the AI output failed schema validation, and error monitoring. That exact pattern—turning messy data or AI outputs into strict, validated schemas—is what I love doing."*

---

## Q3: "What do you mean by 'Harness Engineering', and how do you use it to build a new feature or project from scratch?"

**Your Answer:**
> *"Harness Engineering means building the guardrails around the AI so it cannot hallucinate or break existing code. When I implement a new feature or marketplace integration from scratch, I follow 5 steps:*
> *1. **Context & Spec:** I write a short 10-line spec in markdown with the inputs, outputs, and error cases like `401` or `429`.*
> *2. **Schemas First:** Before writing business logic, I have the agent write the strict data schemas—like `AJV` in TypeScript or `Pydantic` in Python—and I review them line by line.*
> *3. **Offline Fixtures & Tests:** We create local test fixtures from real network responses and write unit tests first.*
> *4. **Agent Self-Verification Loop:** The agent writes the implementation and runs the test suite and linter in the terminal automatically until every check is green.*
> *5. **Diff Review & Checkpoint:** I run GitHub Copilot Code Review on the diff, verify the code myself, update my state file, and commit to Git."*

---

## Q4: "How do you use Claude Code with OpenRouter, and what commands or features do you use inside it?"

**Your Answer:**
> *"I use **Claude Code** both in the terminal and through the **VS Code extension**, connected to my **OpenRouter API token** via environment variables (`ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`). That lets me route requests flexibly while keeping all of Claude Code's agent features.*
>
> *Inside Claude Code, I rely heavily on:*
> *- **`CLAUDE.md`:** Which I generate with `/init` and refine with our exact test commands and code style rules.*
> *- **Plan Mode (`Shift + Tab`):** So the agent investigates the codebase and shows me a plan before editing files.*
> *- **Context Management (`/compact` and `/clear`):** When a session gets long, I run `/compact` so the model doesn't lose focus or waste tokens, and `/clear` between unrelated tasks.*
> *- **Custom Slash Commands (`.claude/commands/`):** I save reusable prompt checklists—like `/check-schema` or `/pre-commit-check`—so I can trigger complex workflows with one command."*

---

## Q5: "How do you use Skills and Plugins in your AI setup?"

**Your Answer:**
> *"I separate **Rules**, **Skills**, and **Plugins** so my agent stays fast and doesn't fill up its context window:*
> *- **Rules (`CLAUDE.md` / `AGENTS.md`)** are short and loaded on every turn for global project rules.*
> *- **Skills (`SKILL.md` folders)** are for detailed, multi-step workflows. The agent only sees the skill name and a one-line description at first, and it loads the full `SKILL.md` file **on demand** only when the task needs it. For example, at Ruit, a skill could be a step-by-step playbook for turning a `.har` capture into a new marketplace connector.*
> *- **Plugins** bundle skills, rules, and **MCP tools** together into one package that the whole team can install and share easily."*

---

## Q6: "How do you use multiple agents or sessions in parallel?"

**Your Answer:**
> *"I run parallel sessions in three main ways, with one strict rule: **two agents never edit the same file at the same time**.*
> *1. **Builder + Test Agent in Parallel:** While Session 1 writes the connector code, Session 2 reads the spec and raw JSON samples to build `pytest` fixtures for edge cases like rate limits and missing fields.*
> *2. **Main Agent + Read-Only Research Subagent:** In Antigravity or Claude Code, if I need to analyze a huge JSON payload or read docs, I delegate that to a read-only **research subagent**. It returns a short 10-line summary so my main coding session stays clean.*
> *3. **Separate Folders or `git worktree`:** If I'm working on two separate marketplace connectors or a hotfix while a feature is running, I open two workspaces on separate folders or Git worktrees so both agents can run tests in parallel without conflicts."*

---

## Q7: "Why do you use GitHub Copilot Code Review if you already use Claude Code and Antigravity?"

**Your Answer:**
> *"Because the agent that writes the code has the same blind spots as the prompt I gave it. Before I commit or open a PR, I open the VS Code Source Control diff and click **GitHub Copilot Code Review**, and I also use Copilot Review on GitHub Pull Requests. Having an independent model review only the Git diff is great at catching edge cases—like a missing timeout, an unhandled `None` value, or a security issue—before my teammates ever see the PR."*

---

## Q8: "Since you haven't used Python or Django in production, how does your AI workflow help you write safe Python at Ruit?"

**Your Answer:**
> *"I'm very open that my 9+ years of production backend experience are in Node.js, TypeScript, SQL, Redis, and Delphi, and I've only used Python in basic side projects. But the backend problems—like race conditions, database locks, background queues, and API schema validation—are the exact same problems I've solved for years.*
>
> *When I write Python, I instruct my agent in `CLAUDE.md` and `AGENTS.md` to write **simple, basic Python** with clear comments—no overly clever one-liners—and I enforce a strict harness with **Pydantic validation, `pytest`, `ruff`, and `mypy`**. That way, I can read and understand every single line of Python I ship, and the test suite proves it works."*

