# 03 — Spoken Q&A Scripts: How I Work with AI & Claude Code

> **Practice Out Loud (Upper-B2):** 6 ready-to-speak answers covering Luis's exact email cheat sheet questions, reflecting your honest background.

---

### Q1: "Walk us through how you work with AI on a daily basis when coding."
> *"I work with AI using a structured workflow I call **Harness Engineering**. I don't just type a prompt and copy code. I use **Antigravity IDE** and **Claude Code in VS Code** (connected via an **OpenRouter token**) as my primary builders. I maintain a living state file (`ai-state.md` or `CLAUDE.md`) so the agent knows the project rules. For every feature, I start in **Plan Mode**, define data schemas and error types first, let the agent write code and iterate on terminal test suites until they pass, and review the Git diff with **GitHub Copilot Code Review** before committing."*

---

### Q2: "You worked with AI at QueryLaw and Parsaiane. Did you do RAG, fine-tuning, or model deployment?"
> *"I want to be 100% transparent: I did not do fine-tuning, vector RAG pipelines, or ML model deployment. My experience is on the **application reliability engineering side of AI**. At **Parsaiane**, I built a news crawler for 150+ sites with OpenAI summarization. At **QueryLaw**, our legal platform required 95%+ accuracy because legal tools cannot afford broken or hallucinated outputs. I built a strict validation harness: prompt engineering, **JSON Schema and AJV validation checks** on every response, and automated self-repair retry loops when output violated the schema."*

---

### Q3: "What is your setup with Claude Code and OpenRouter?"
> *"I run Claude Code in both the terminal and VS Code, routed through my **OpenRouter API token** using environment variables. This gives me unified billing, cost controls, and access to models like Claude 3.7 Sonnet. In my active project, I use `CLAUDE.md` at the root as the memory bank, Plan Mode (`Shift + Tab`) to approve architecture before any edits, and custom slash commands in `.claude/commands/` for reusable validation workflows."*

---

### Q4: "How do you use Skills, Plugins, and parallel sessions?"
> *"I keep context windows small and focused. **Rules** are always on for style and test commands. **Skills (`SKILL.md`)** are on-demand playbooks that load only when needed, like a checklist for scaffolding a new marketplace adapter. When running in parallel, I follow one strict rule: **two agents never edit the same file**. I run a Builder agent on code while a Test agent creates mock fixtures, or I use a read-only research subagent for large payloads."*

---

### Q5: "Why use GitHub Copilot Code Review if you already have Claude Code or Antigravity?"
> *"Because the agent that writes the code shares the same blind spots as the prompt I gave it. Before I commit or open a PR, I open the VS Code Git diff and click **GitHub Copilot Code Review**. Having an independent second model audit the diff is great at catching edge cases—like an unhandled null value, missing timeout, or security risk—before my teammates see the code."*

---

### Q6: "You applied for a Python backend role, but your background is Node.js and you don't know Python. How will you work here?"
> *"I want to be 100% transparent: **I do not know Python, and I have never used it in production.** My expertise is 9+ years of backend systems in Node.js, TypeScript, SQL, and distributed architectures.
>
> In today's software engineering, an elite engineer doesn't need to manually type syntax for every language. When working in Python, I direct my AI agents using **Harness Engineering**. I define the architectural boundaries, API schemas, concurrency model, and automated test requirements. The AI generates the implementation, runs the test suite in the terminal, and self-repairs until green. I audit the system invariants—like row locking, idempotency, and timeouts—and verify the diff with Copilot. My core value is senior systems thinking, not language memorization."*
