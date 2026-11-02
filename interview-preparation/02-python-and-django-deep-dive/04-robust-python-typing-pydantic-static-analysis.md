# Making Robust Python: Type Hints, Pydantic v2 & Static Analysis

> **Luis's Cheat Sheet Topic:** *"how to make robust Python through type hints, static analysis, etc. ... json validation"*

---

## 1. Philosophy: Why Dynamic Python Needs Strict Guardrails

Python's dynamic nature makes prototyping fast, but in an integrations-heavy backend like Ruit—where 15+ external marketplaces return inconsistent types (`"19.99"` vs `19.99` vs `null`)—untyped dict-passing (`data["item"]["price"]`) leads to production `KeyError`, `TypeError`, and `AttributeError` crashes.

To make Python as rock-solid as TypeScript or Rust, senior Python teams combine **two complementary layers**:
1. **Compile-Time / CI Static Analysis (`typing` + `mypy`/`pyright` + `ruff`):** Guarantees internal functions, ORM models, and connectors pass the right types before code is ever deployed.
2. **Runtime Boundary Validation (`Pydantic v2`):** Guarantees untrusted external I/O (marketplace JSON responses, webhooks, LLM outputs, Celery task payloads) conforms to strict schemas at the edge of the system.

---

## 2. High-Signal Python Type Hints (`typing`) You Should Use Fluently

### 2.1 Structural Subtyping (`typing.Protocol`) vs Inheritance (`abc.ABC`)
Coming from TypeScript, `typing.Protocol` is your best friend. Unlike `abc.ABC` (which requires explicit subclassing), `Protocol` checks **structural compatibility** (duck typing verified by `mypy`/`pyright`):

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsInventorySync(Protocol):
    marketplace_slug: str

    async def push_stock(self, sku: str, quantity: int) -> bool: ...
```
Any class implementing `marketplace_slug` and `async def push_stock(self, sku: str, quantity: int) -> bool` automatically satisfies `SupportsInventorySync` without inheriting from it!

### 2.2 `TypedDict`, `Literal`, `Annotated`, and `Generic`
- **`TypedDict`:** Gives static type-checking to plain Python `dict`s (zero runtime overhead—great for raw headers or legacy dict payloads before Pydantic parsing).
- **`Literal`:** Restricts values to specific constants, just like TypeScript string literal unions (` MarketplaceSlug = Literal["wallapop", "vinted", "ebay", "depop"]`).
- **`Annotated[T, ...]`:** Attaches metadata or validation constraints directly to a type alias:
  ```python
  from typing import Annotated
  from pydantic import Field

  PositiveCents = Annotated[int, Field(gt=0, description="Price in euro cents")]
  ```
- **`Generic[T]` & `TypeVar`:** Lets you build reusable typed wrappers (like a paginated response `PaginatedResult[Listing]` or a Rust-style `Result[T, E]`).

---

## 3. Pydantic v2 Deep Dive (Your Python Equivalent of TS + AJV)

At QueryLaw, you achieved 95%+ AI accuracy using multi-layer JSON Schema (AJV) validation. In Python, **Pydantic v2** is the gold standard (its core validation engine, `pydantic-core`, is written in **Rust**, making it 5x–50x faster than Pydantic v1).

### Key Pydantic v2 Features to Highlight
1. **`model_validate_json(raw_bytes_or_str)` vs `model_validate(dict)`:**
   - **Pro Tip:** Never do `Model.model_validate(json.loads(response.content))` on large responses! Calling `Model.model_validate_json(response.content)` parses the JSON and validates types in **one single pass inside Rust (`jiter`)** without creating intermediate Python dictionaries!
2. **`mode="before"` vs `mode="after"` Validators:**
   - `@field_validator("price", mode="before")`: Runs on the raw untrusted input *before* Pydantic's internal Rust type parser (ideal for normalizing dirty marketplace strings like `"12,50 €"`).
   - `@field_validator("price", mode="after")`: Runs *after* Pydantic has already guaranteed the value is a valid `Decimal` or `int`.
   - `@model_validator(mode="after")`: Cross-field invariants (e.g., verifying `discount_price < original_price`).
3. **Handling Extra / Changing Marketplace Fields (`ConfigDict`):**
   - `extra="forbid"`: Raises `ValidationError` if unknown fields appear (great for internal APIs / strict webhooks).
   - `extra="ignore"`: Drops unknown fields silently.
   - `extra="allow"`: Stores unknown fields in `self.__pydantic_extra__`—allowing Ruit to succeed on the seller's request while logging a **schema-drift telemetry event** when a marketplace adds new fields!

---

## 4. Static Analysis & Linting Stack (`Ruff` + `Mypy` / `Pyright`)

- **Ruff (`ruff check` & `ruff format`):**
  - Written in Rust by Astral; replaces `Flake8`, `Black`, `isort`, `pyupgrade`, `flake8-bugbear` (`B`), and `flake8-async` (`ASYNC`) in <50ms.
  - Specifically mention enabling **`flake8-bugbear` (`B`)** and **`flake8-async` (`ASYNC`)** rules in Ruff—they automatically catch blocking calls inside `async def` functions and mutable default arguments!
- **Mypy (`mypy --strict`) / Pyright:**
  - Enforces `--disallow-untyped-defs`, `--no-implicit-optional`, `--warn-return-any`, and exhaustive union checking (`assert_never`).
  - For Django, **`django-stubs`** provides static type stubs for dynamic Django `QuerySet` and `Model` attributes.

---

## 5. Classic Python Footguns Static Analysis Catches

Be ready if Luis or Alonso asks about subtle Python language quirks:

1. **Mutable Default Arguments:**
   ```python
   # BAD: The default list `[]` is evaluated ONCE at function definition time (`def`),
   # so every call shares the exact same list across requests!
   def add_tag(tag: str, tags: list[str] = []) -> list[str]: ...

   # GOOD:
   def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
       resolved_tags = list(tags) if tags is not None else []
       resolved_tags.append(tag)
       return resolved_tags
   ```
2. **Late-Binding Closures in Loops:**
   ```python
   # BAD: All lambdas capture the variable name `mp`, which equals "ebay" at the end of the loop!
   handlers = [lambda: sync(mp) for mp in ["wallapop", "vinted", "ebay"]]

   # GOOD: Bind current value as a default argument `m=mp` (or use `functools.partial`)
   handlers = [lambda m=mp: sync(m) for mp in ["wallapop", "vinted", "ebay"]]
   ```
