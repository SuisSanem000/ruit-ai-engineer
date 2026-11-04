# 06 — The Elite Live AI Task: What to Show, What to Say & How to Run It Like a Pro

> **The Big Mistake Most Candidates Make:** They open a chat box, type a vague prompt, copy-paste code, hit an error, and copy-paste the error back into chat. That looks like an amateur who "just chats with AI."  
> **How You Win the Role:** You run the live task as a **Senior Harness Engineer** who directs AI agents with strict specs, offline tests, autonomous terminal loops, and senior code auditing.

---

## 1. Amateur Chatter vs. Elite AI Engineer

| What the Amateur Chatter Does (Do NOT Do) | What You Do as an Elite AI Engineer (Do THIS) |
| :--- | :--- |
| Types a prompt immediately into chat. | Asks 2 clarifying questions about failure modes and concurrency first. |
| Writes logic before knowing the data shape. | Defines strict **Pydantic models and error classes** before writing logic. |
| Copies and pastes errors back and forth manually. | Lets the agent run tests and linters in the terminal and **self-correct autonomously**. |
| Tests manually by hitting real internet APIs. | Tests completely offline using **`httpx.MockTransport`** fixtures. |
| Blindly trusts AI code. | Audits the code out loud for **timeouts, connection pools, and blocking calls**. |
| Leaves messy untracked files. | Runs **Copilot Code Review** on the Git diff and makes an atomic Git commit. |

---

## 2. Minute-by-Minute Live Task Execution Plan (20 Minutes)

### Phase 1: Clarify & Set Boundaries (Minutes 0–3)
- **What to Say Out Loud (Upper-B2):**
  > *"Before we write any code, let me clarify the failure modes and scale. What errors should we expect here—should we retry on network timeouts and `429` rate limits, and stop immediately on `401` authentication errors? And does this need to handle one request or batch requests with a concurrency limit?"*
- **Why this impresses them:** Shows you think about production reliability before typing.

### Phase 2: Define Data Models & Error Types First (Minutes 3–6)
- **What to Show on Screen:** In Antigravity or Claude Code, prompt the agent to define:
  1. Custom exceptions (`MarketplaceIntegrationError`, `RetryableMarketplaceError`, `SellerAuthExpiredError`).
  2. A strict `Pydantic` model with validators for dirty fields (like cleaning `"45,50 €"` into `Decimal("45.50")`).
- **What to Say Out Loud (Upper-B2):**
  > *"I always define data contracts and error categories first. In integration work, if your data model and error types are solid, 80% of downstream bugs disappear."*

### Phase 3: Parallel Implementation & Offline Tests (Minutes 6–12)
- **What to Show on Screen:**
  - Launch the task using **Plan Mode** (`/plan` in Antigravity or `Shift + Tab` in Claude Code).
  - Split the work:
    - **Session / Task A:** Writes the async HTTP function using `httpx.AsyncClient` with backoff retries.
    - **Session / Task B:** Writes offline `pytest` tests using `httpx.MockTransport` to simulate `200 OK`, `429 Rate Limit`, `401 Unauthorized`, and schema drift.
- **What to Say Out Loud (Upper-B2):**
  > *"Notice that I test this completely offline with mock fixtures rather than making live web requests. This makes our test suite instantaneous and deterministic."*

### Phase 4: Autonomous Terminal Self-Healing Loop (Minutes 12–16)
- **What to Show on Screen:** Let the agent execute `.venv/bin/pytest` and `.venv/bin/ruff check` in the terminal.
- If a test fails or linter complains:
  - Do **not** copy-paste the error.
  - Let the agent read the terminal output directly and edit the code to fix the test.
- **What to Say Out Loud (Upper-B2):**
  > *"Instead of me manually copying and pasting errors into a chat box, the agent inspects the terminal exit code and stack trace directly, iterates on the code, and verifies that all tests pass."*

### Phase 5: Senior Code Audit Out Loud (Minutes 16–18)
- **What to Show on Screen:** Open the generated file and review these 4 points out loud:
  1. **Connection Pooling:** *"I check that we reuse a single `httpx.AsyncClient` across calls instead of instantiating a new client in a loop, which would exhaust TCP sockets."*
  2. **Timeouts:** *"I verify that an explicit request timeout is set so a hanging marketplace server never freezes our worker."*
  3. **No Silent Exceptions:** *"I make sure we catch specific custom errors rather than using a blanket `except Exception: pass`."*
  4. **Non-Blocking Sleep:** *"Inside async functions, I verify we use `await asyncio.sleep()` rather than blocking `time.sleep()`."*

### Phase 6: Copilot Diff Review & Git Commit (Minutes 18–20)
- **What to Show on Screen:** Open the Git diff tab in VS Code / Antigravity, click **Copilot Code Review**, review any suggestion, and commit:
  - `git add -A && git commit -m "feat(integration): add resilient marketplace client with retry and offline tests"`
- **What to Say Out Loud (Upper-B2):**
  > *"All tests are green, Copilot code review is clean, and the feature is committed to Git. In production, this connector would be wrapped in a Celery task with Redis rate limits and Sentry alerting."*
