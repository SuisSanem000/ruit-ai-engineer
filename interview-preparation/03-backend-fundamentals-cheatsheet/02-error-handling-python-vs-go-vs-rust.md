# 02 — Error Handling Philosophy: Python vs. Go vs. Rust

> **Why This Question:** Founding Engineer Alonso Veliz Garcia works with Python and **Rust**. Understanding how different languages handle errors shows deep software engineering maturity.

---

## 1. Comparing Error Handling Philosophies

| Dimension | Python | Go | Rust |
| :--- | :--- | :--- | :--- |
| **Mechanism** | Exceptions (`try / except / finally / raise`) | Explicit return values `(result, err)` | Algebraic Data Types: `Result<T, E>` and `Option<T>` |
| **Control Flow** | Unwinds the call stack until a matching `except` block catches it. | Normal linear flow with `if err != nil` checks. | Pattern matching (`match`) or `?` operator to propagate errors early. |
| **Visibility** | Implicit: Looking at a function signature does not tell you what exceptions it might raise. | Explicit: The function signature clearly returns an `error` type. | Strictly explicit: The return type is `Result<Value, Error>`. |
| **Compiler Enforcement** | None. Uncaught exceptions crash the process at runtime. | Weak. You can technically ignore errors with `_`. | **Absolute.** The compiler refuses to compile if you don't handle both `Ok` and `Err`. |

---

## 2. Best Practice in Python Marketplace Integrations

Because Python exceptions can be implicit, structure integration errors explicitly:

1. **Custom Exception Hierarchy:**
   - Define a base `MarketplaceError(Exception)` and derive specific subclasses:
     - `RetryableError(MarketplaceError)`: Network timeouts, 429 rate limits, 503 maintenance.
     - `AuthExpiredError(MarketplaceError)`: 401 Unauthorized $\rightarrow$ abort retries, refresh token, or notify seller.
     - `SchemaDriftError(MarketplaceError)`: Marketplace changed response fields $\rightarrow$ log scrubbed diff, notify engineers.
2. **Explicit Result Pattern (Rust/Go-Style in Python):**
   - For batch synchronization across 5 marketplaces, returning an explicit `Result(success=True/False, error_code=...)` avoids crashing the entire batch when one marketplace is down.
3. **No Bare Exceptions:** Never write `except Exception: pass`. Catch specific errors, log context (item ID, marketplace), and handle or re-raise.

