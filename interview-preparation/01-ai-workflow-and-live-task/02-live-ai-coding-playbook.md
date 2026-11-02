# 20-Minute Live AI Task Playbook

> Follow these 5 simple steps when Luis gives you the short live task on your laptop.

---

## Step 1: Ask 2 Quick Questions First (Minutes 0–3)

- Do not type a prompt immediately—ask Luis 2 short questions to show how you think:
  - *"What errors should we expect here—should we retry on network timeouts and `429` rate limits, and stop immediately on `401` auth errors or bad JSON?"*
  - *"Do we need to run one request at a time, or many requests at once with a concurrency limit?"*

---

## Step 2: Define the Data Model & Error Types First (Minutes 3–6)

- Ask the AI to create the data validation model (`Pydantic BaseModel`) and simple custom error classes first.
- Review the fields with Luis to confirm the inputs and outputs match what he wants.

---

## Step 3: Generate Code & Tests in Parallel (Minutes 6–12)

- **Agent Task A (Implementation):** Ask the AI to write a simple, well-commented Python function/class that calls the API, validates the JSON, and retries on temporary errors.
- **Agent Task B (Tests):** Ask a parallel subagent (or second step) to write `pytest` tests covering:
  - Normal valid response.
  - Messy data (like price sent as `"19,50 €"` instead of a number) and unexpected extra fields.
  - Temporary `429` rate-limit error that succeeds on retry.
  - Permanent `401` login error that fails right away without retrying.

---

## Step 4: Check the AI's Code & Run Tests (Minutes 12–17)

- Run `.venv/bin/pytest` and `.venv/bin/ruff check` in the terminal.
- Tell Luis what you always check in AI-generated code:
  - **Connection Reuse:** Did the AI pass a shared `httpx.AsyncClient` instead of opening a new client inside a loop?
  - **Timeouts:** Did the AI set a clear request timeout so a slow marketplace never hangs the worker forever?
  - **No Silent Errors:** Did the AI catch specific errors instead of hiding bugs with a bare `except Exception: pass`?
  - **Async Sleep:** Inside `async def`, did the AI use `await asyncio.sleep()` instead of blocking `time.sleep()`?

---

## Step 5: Commit to Git & Explain Next Steps (Minutes 17–20)

- Commit the tested code to Git (`git add -A && git commit -m "..."`).
- Briefly mention how this code would run in production at Ruit (inside a Celery background worker with Redis rate limits and error alerts).
