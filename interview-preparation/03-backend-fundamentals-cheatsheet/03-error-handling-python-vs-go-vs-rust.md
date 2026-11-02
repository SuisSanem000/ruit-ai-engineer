# Error Handling Philosophy: Python vs Go vs Rust

> **From Luis's Email Cheat Sheet:** *"error handling and the philosophy behind them (python vs go vs rust for example)"*  
> **Code examples with detailed comments:** [test_concurrency_locks_and_errors.py](./fundamentals-labs/test_concurrency_locks_and_errors.py)

---

## 1. Comparing Python, Go, and Rust Error Handling

- **Python — Exceptions (`try / except` — "Ask Forgiveness, Not Permission"):**
  - **How it works:** Functions return the happy-path value directly and `raise` an exception when something goes wrong. If not caught, the exception bubbles up the call stack.
  - **Pros:** Very clean and readable code when everything succeeds; no error-checking boilerplate on every line.
  - **Cons:** **Hidden failure modes.** Looking at a function signature (`def fetch_item(id: str) -> Item:`), you have no idea what exceptions it might raise without reading all its internal code. It is also too easy to write `except Exception:` and accidentally hide real bugs.
- **Go — Errors as Values (`val, err := fn()`):**
  - **How it works:** Functions return both the result and an `error` value. You check `if err != nil` right after calling the function.
  - **Pros:** Very explicit—you are forced to think about what can go wrong at every network or database call.
  - **Cons:** Repetitive `if err != nil` boilerplate everywhere, and because Go does not have sum types (enums with data), the compiler does not force you to handle every specific error type.
- **Rust — Algebraic Result Types (`Result<T, E>` & `Option<T>`):**
  - **How it works:** Functions that can fail return `Result<T, E>`, which is either `Ok(value)` or `Err(error)`. Missing values use `Option<T>` (`Some(value)` or `None`). The `?` operator passes errors up cleanly.
  - **Pros:** **Compile-time safety.** The errors are right in the function's return type, and the Rust compiler refuses to compile your code if you forget to handle the error or `None` case!
  - **Cons:** Stricter learning curve and more upfront type design.

---

## 2. How to Apply the Best of Go & Rust Inside Python Integrations

- When building marketplace integrations in Python, do not let raw low-level errors (`KeyError`, `httpx.HTTPError`, `ValidationError`) fly around randomly.
- **1. Group Exceptions by What the System Should Do Next:**
  - **`RetryableError` (`429`, `502`, `503`, network timeout):** Tell Celery to wait and retry automatically with backoff.
  - **`SellerAuthExpiredError` (`401`, `403`):** Do NOT retry—refresh the seller's login token or notify the seller to reconnect their account.
  - **`UpstreamBreakageError` (`ValidationError`, missing JSON field, unexpected `400`):** Do NOT retry—pause the marketplace queue (circuit breaker) and alert engineers that the marketplace changed its API!
- **2. Always Chain Exceptions (`raise CustomError(...) from exc`):**
  - In Python, using `from exc` keeps the original error traceback attached so you can still see the exact line or JSON field that failed in your logs/Sentry.
- **3. Return Explicit `Outcome` / `Result` Objects for Batch Work:**
  - Just like Go and Rust treat errors as normal data values, when delisting an item across 5 marketplaces at once, return a simple `Result` / `Outcome` object (`success=True/False`, `retryable=True/False`, `error_message=...`) for each marketplace instead of crashing the whole batch when 1 marketplace fails.
