# 02 — Generators, Streaming, Pydantic & Robust Typing

> **Luis's Focus:** Generators, streaming large datasets without memory spikes, and making robust Python via type hints, Pydantic, and static analysis.

---

## 1. Generators (`yield`) & Memory-Safe Streaming

- **What is a Generator?**
  - A function containing `yield` instead of `return`. Calling it returns a lazy iterator that produces one item at a time on demand.
  - State is paused at `yield` and resumed on `next()`.
- **Why It Matters for Ruit:**
  - When syncing a seller with 50,000 listings or streaming a 500MB JSON catalog export, building a list `[item for item in ...]` consumes hundreds of megabytes of RAM and risks out-of-memory crashes.
  - Generators keep memory usage flat (a few kilobytes) regardless of catalog size.
- **`yield from` for Nested Trees:**
  - Simplifies recursion when flattening nested category trees: `yield from flatten_category(child)`.
- **Async Generators (`async def` + `yield`):**
  - Stream paginated HTTP responses page-by-page. The consumer processes Page 1 while Page 2 is being fetched over the network.
- **Django ORM `.iterator(chunk_size=2000)`:**
  - Streams database rows in server-side batches rather than loading the entire queryset into memory.

---

## 2. Robust Python: Type Hints, Pydantic & Static Analysis

- **Why Type Hints Matter:**
  - Python is dynamically typed, but type hints (`def fetch(item_id: int) -> Optional[dict]:`) allow tools like **`mypy`** and **`pyright`** to catch type errors before deployment.
  - They also give AI coding agents strict contracts so they don't hallucinate wrong parameters.
- **Runtime Validation with Pydantic (`BaseModel`):**
  - Type hints are only checked before runtime. **Pydantic** validates untrusted JSON from external marketplaces at runtime.
  - Features used:
    - **`field_validator`:** Parses and sanitizes messy marketplace data (e.g. converting string `"45,50 €"` into `Decimal("45.50")`).
    - **`model_validator(mode="after")`:** Validates cross-field business logic (e.g., verifying `discount_price < price`).
    - **Extra Field Tracking:** Uses `extra="ignore"` to safely accept harmless new fields while logging schema drift.
- **Static Analysis Tooling:**
  - **`ruff`:** Extremely fast linter and formatter that replaces Flake8, Black, and isort.
  - **`mypy`:** Static type checker enforcing type safety across the codebase.

