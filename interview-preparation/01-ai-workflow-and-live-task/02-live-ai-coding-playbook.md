# The 20-Minute Live AI Coding Task Playbook

> **Context:** In Part 1 of the interview (`13:00–14:00`), Luis will ask you to complete a **brief task with AI** on your laptop while they watch and chat with you.  
> **What They Are Really Evaluating:**
> 1. Do you just paste a vague prompt and pray, or do you **engineer the problem** (clarify requirements, define types/schemas first, decompose)?
> 2. Do you use AI features effectively (context pinning, parallel subagents/tasks, automated test/lint loops)?
> 3. Do you **critically audit** the AI's code for production edge cases (timeouts, retries, race conditions, dirty JSON, types)?

---

## The 5-Step Live Execution Protocol (15–20 Minutes Total)

### Step 1: Clarify & Lock the Contract (Minutes 0 – 3) — *Talk Out Loud!*
Before typing a prompt, ask Luis 2–3 sharp, senior clarifying questions:
- *"What are the expected failure modes here—should we distinguish between transient network/rate-limit errors (retryable) and schema/auth breakages (non-retryable)?"*
- *"Are we optimizing for single-item latency (like instant delisting when an item sells) or high-throughput batch syncing (where we need bounded concurrency with a Semaphore)?"*
- *"Should we validate external JSON strictly with Pydantic and log unexpected/missing fields for breakage detection?"*

**Action:** Write (or ask the agent to generate) **only the data contracts & error types first** (`schemas.py` / `exceptions.py`):
- `typing.Protocol` or abstract base interface.
- `pydantic.BaseModel` for inputs/outputs.
- Custom exception hierarchy (`IntegrationError` $\rightarrow$ `RetryableError`, `AuthError`, `SchemaDriftError`).

---

### Step 2: Parallelize Implementation & Adversarial Tests (Minutes 3 – 10)
Demonstrate your **parallel workflow** live!
- **Main Session / Agent 1 (Implementation):**
  > *"Implement the async connector/service matching `schemas.py`. Use `httpx.AsyncClient` with explicit connect/read timeouts, `asyncio.Semaphore` for bounded concurrency, and exponential backoff with jitter on 429/5xx responses. Respect `Retry-After` headers."*
- **Parallel Subagent / Agent 2 (Adversarial Pytest Suite):**
  > *"In parallel, generate `test_task.py` using `pytest` and `httpx.MockTransport`. Cover: (1) valid payload parsing, (2) dirty/drifted JSON payload (extra unknown fields + type coercion), (3) 429 rate-limit recovery using `Retry-After`, (4) permanent 401 auth failure without useless retries, and (5) bounded concurrency."*

---

### Step 3: Run the Closed-Loop Verification Gate (Minutes 10 – 14)
Have the agent (or terminal) run:
```bash
pytest -v
ruff check .
mypy .
```
If anything fails, show how you feed the exact traceback/type error back to the agent with a targeted fix rather than rewriting everything from scratch.

---

### Step 4: The "Senior Engineer Audit" of AI Output (Minutes 14 – 17)
**This is the moment that separates Senior Engineers from Junior AI users.**  
Point at the generated code on screen and tell Luis what you specifically check for in AI-generated Python code:

1. **Connection Pooling & Resource Leaks:** Did the AI instantiate `httpx.AsyncClient()` *inside* a loop (bad—creates new TCP/TLS handshakes per request!) instead of reusing a single client via `async with` or dependency injection?
2. **Timeouts:** Did the AI forget `timeout=httpx.Timeout(...)`? (Though `httpx` defaults to 5s, `requests` defaults to `None` = infinite hang!).
3. **Exception Swallowing:** Did the AI write `except Exception: return None`? Replace with explicit exception catching (`except httpx.TimeoutException as exc: raise RetryableError(...) from exc`).
4. **Idempotency & Mutability:** Did the AI use mutable default arguments (`def fn(items: list = [])`) or forget idempotency keys on POST requests?
5. **Async Blocking Traps:** Did the AI call `time.sleep()` instead of `await asyncio.sleep()` inside an `async def` function? (Huge catch!).

---

### Step 5: Atomic Git Commit & Extension Discussion (Minutes 17 – 20)
Commit the working, tested code cleanly:
```bash
git add -A && git commit -m "feat(task): implement resilient async connector with Pydantic validation and retry tests"
```
Then summarize in 30 seconds how this would plug into Ruit's production stack (e.g., *"In production at Ruit, this client would be invoked by a dedicated Celery queue per marketplace with Redis rate-limiting, emitting Prometheus metrics on schema drift and 429 rates"*).

