# 02 — Harness Engineering: How to Turn an Idea or Feature into Reliable Code

> **Why Learn This Concept:** In modern AI engineering (2025–2026), **"Harness Engineering"** is one of the strongest terms you can use in an interview. It connects your **QueryLaw schema validation experience** directly to how you build features with coding agents today.

---

## 1. What is "Harness Engineering"? (Simple B2 Explanation)

- **The Core Idea:**
  - An AI model (like Claude or Gemini) is like a very fast engine, but by itself it can hallucinate, forget project rules, or break existing code.
  - **The "Harness"** is the system of **context files, strict schemas, automated tests, linters, and retry loops** that you build *around* the AI so its output is always safe, predictable, and production-ready.
- **How to explain it to Luis in 20 seconds:**
  > *"To me, working with AI isn't just writing clever prompts—it's **Harness Engineering**. Whether I am using AI inside our product like I did at QueryLaw, or using coding agents like Claude Code and Antigravity to build a feature, I wrap the AI in a strict harness: clear context files, strict schema validation, automated tests, and a review loop. The AI writes the draft fast, and the harness guarantees it actually works."*

---

## 2. Two Types of Harness Engineering You Know

### Type A: Product / Runtime AI Harness (What You Did at QueryLaw)
- When your application calls an LLM API in production (like QueryLaw generating legal data, or Ruit generating a Vinted listing from a photo):
  - **1. Structured Input Prompt:** Give the LLM clear instructions, allowed categories, and output format rules.
  - **2. Strict Schema Gate (AJV in Node.js / Pydantic in Python):** Never trust raw text from an LLM. Validate the JSON output against a strict schema immediately.
  - **3. Self-Correction Retry Loop:** If schema validation fails (for example, price is negative or a required field is missing), automatically send the exact validation error back to the LLM once to fix its own JSON.
  - **4. Fallback & Monitoring:** If it still fails, log the error and ask the user to fill in the missing field manually instead of crashing.

### Type B: Developer / Coding Agent Harness (How You Build Features Every Day)
- When you use **Antigravity IDE** or **Claude Code** to implement a new feature or project:
  - **1. Memory & Rules Harness (`ai-state.md`, `CLAUDE.md`, `AGENTS.md`):** Gives the agent persistent memory of the repo structure, coding style, and forbidden actions (for example: *"Never touch the resources folder"*).
  - **2. Specification Harness:** A short markdown spec defining inputs, outputs, and edge cases (`401`, `429`, missing fields) before any code is written.
  - **3. Verification Harness (`pytest` / `ruff` / `mypy`):** Automated terminal checks that the agent must run and pass after every edit.
  - **4. Review Harness (GitHub Copilot Code Review + Human Check):** Automated diff review before committing to Git.

---

## 3. Step-by-Step: How I Use Harness Engineering to Implement a New Feature

If Luis asks, *"How do you take a new idea or marketplace integration and build it with AI?"*, walk through these **5 steps**:

- **Step 1 — Write a 10-Line Spec & Constraints File:**
  - Define the exact input, expected output, and failure cases (rate limits, auth expiration, schema changes).
  - Save it in a markdown task file so the agent has a single source of truth.
- **Step 2 — Define the Data Contracts First (Schemas & Types):**
  - Before writing business logic, ask the agent to create the data models and validation schemas (like `AJV` schemas in TypeScript or `Pydantic` models in Python).
  - Review these schemas yourself line by line—if the data contract is right, 80% of bugs are prevented.
- **Step 3 — Build Offline Test Fixtures Before Live Code:**
  - Give the agent real sample JSON payloads (for example, from a browser `.har` network capture) including a normal `200 OK`, a `429 Rate Limit`, and a broken payload missing a required field.
  - Have the agent write unit tests against these local fixtures first.
- **Step 4 — Let the Agent Implement & Self-Verify in a Loop:**
  - Tell the agent: *"Implement the function to pass these tests, and run the test suite and linter in the terminal until all checks are green."*
  - Instead of me copying and pasting errors, the agent sees the test failure in the terminal and fixes its own code automatically.
- **Step 5 — Run Copilot Code Review & Commit to State:**
  - Run **GitHub Copilot Code Review** on the git diff to catch any subtle issues, read through the final code myself, update `ai-state.md`, and commit to Git.

