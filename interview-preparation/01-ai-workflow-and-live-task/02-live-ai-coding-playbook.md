# 20-Minute Live AI Coding Playbook

> **Your Honest Advantage:**  
> Tell Luis openly at the start: *"Since my production background is Node.js/TypeScript and I only used Python in basic side projects, I ask the AI to write clean, basic Python without clever tricks, so I can read and verify every single line myself."*

---

## The 5 Steps to Follow During the Live Task

### Step 1: Ask 2 Quick Questions Before Prompting (Minutes 0 – 2)
- Do not copy-paste the task into the AI immediately.
- Ask Luis 2 simple engineering questions first:
  - *"What should happen if the marketplace API returns an error—should we retry on `429` / `500` and stop immediately on `401` unauthorized?"*
  - *"What fields in the JSON response are required, and how should we handle dirty data like prices written as strings?"*

### Step 2: Prompt the AI for Data Validation & Basic Error Classes First (Minutes 2 – 5)
- Ask the AI to create the **Pydantic model** (to validate the JSON) and **basic custom error classes** first.
- Why: Once the data shape is clear, the rest of the code is much easier to write and test.

### Step 3: Run Coding & Test Generation in Parallel (Minutes 5 – 12)
- **In your main agent session:** Ask the AI to write the function using basic, readable Python with comments, explicit HTTP timeouts, and retry logic.
- **In a parallel subagent / second session:** Ask it to write `pytest` unit tests covering:
  1. A normal valid JSON response.
  2. A messy JSON response (like `"45,50 €"` or extra unknown fields).
  3. A `429` rate-limit response that succeeds on retry.
  4. A `401` auth error that fails right away without retrying.

### Step 4: Run Tests & Check the AI's Code Yourself (Minutes 12 – 17)
- Run `.venv/bin/pytest -v` in the terminal.
- Read the Python code on screen and tell Luis what you always check in AI code:
  - **Timeouts:** Did the AI include a timeout on the HTTP client so it never hangs forever?
  - **Connection Reuse:** Did the AI reuse the HTTP client (`AsyncClient` or `Session`) instead of opening a new connection inside a loop?
  - **No Silent Errors:** Did the AI catch specific errors instead of hiding bugs with a bare `except Exception: pass`?
  - **Async Sleep:** Inside an `async def` function, did it use `await asyncio.sleep()` instead of blocking `time.sleep()`?

### Step 5: Commit to Git (Minutes 17 – 20)
- Once tests pass, make a clean Git commit (`git add -A && git commit -m "..."`).
- See [marketplace_connector.py](./live-task-sandbox/marketplace_connector.py) and [test_marketplace_connector.py](./live-task-sandbox/test_marketplace_connector.py) for the complete, basic Python example.
