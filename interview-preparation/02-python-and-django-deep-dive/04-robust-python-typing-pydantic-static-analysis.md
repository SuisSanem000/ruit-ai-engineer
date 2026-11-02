# Making Robust Python: Type Hints, Pydantic & Static Analysis

> **Code examples with detailed comments:** [test_python_deep_dive_labs.py](./python-django-labs/test_python_deep_dive_labs.py)

---

## 1. Why Type Hints & Validation Matter in Python

- Python is dynamically typed, so without type hints or validation, passing raw dictionaries (`data["item"]["price"]`) from external APIs causes runtime crashes (`KeyError`, `TypeError`) in production.
- Coming from **TypeScript**, you make Python reliable by combining two steps:
  1. **Static Type Checking (before running code):** Python Type Hints + `mypy` / `pyright` + `ruff` (just like `tsc` + ESLint in TypeScript).
  2. **Runtime JSON Validation (when data arrives from outside):** **Pydantic** (just like AJV / Zod that you used at QueryLaw).

---

## 2. Basic Python Type Hints to Know

- **Basic Types:** `str`, `int`, `float`, `bool`, `Decimal`, `list[str]`, `dict[str, int]`.
- **Nullable Values (`Optional`):** `price: float | None = None` (or `Optional[float] = None`).
- **Fixed String Choices (`Literal`):** `Literal["wallapop", "vinted", "ebay"]` (just like TypeScript string union types `'wallapop' | 'vinted' | 'ebay'`).
- **Typed Dictionaries (`TypedDict`):** Lets you define expected keys and types for a plain Python `dict`.
- **Important Fact:** Normal Python type hints are **ignored by Python at runtime**—they only help your editor, AI agents, and `mypy`. To actually check data at runtime, you use **Pydantic**.

---

## 3. Runtime JSON Validation with Pydantic

- **What Pydantic Does:**
  - You define a class inheriting from `BaseModel` with typed fields.
  - When raw JSON arrives from a marketplace API or webhook, Pydantic checks every field, converts safe types (or runs your custom cleaning functions), and raises a clear `ValidationError` if required data is missing or broken.
- **Why Pydantic v2 Is Fast:**
  - Its core validation engine is written in **Rust**, so validating thousands of marketplace items is very fast.
- **Handling Extra Fields from Marketplaces:**
  - **`extra="ignore"`:** Quietly drops unknown fields.
  - **`extra="forbid"`:** Rejects the JSON if any unknown field is present.
  - **`extra="allow"`:** Keeps unknown fields in `__pydantic_extra__` so your code still works while logging a warning that the marketplace changed its JSON response.

---

## 4. Static Analysis Tools (`ruff` & `mypy`)

- **`ruff`:** Super-fast Python linter and code formatter (written in Rust). Catches unused imports, syntax bugs, and bad practices in milliseconds.
- **`mypy` / `pyright`:** Type checkers that read your type hints and catch bugs (like forgetting to check if a value is `None`) before code ever goes to production.

---

## 5. Two Classic Python Quirks That Linters Catch

- **1. Mutable Default Arguments (`def add_item(x, items=[]):`):**
  - In Python, a default list `=[]` is created **only once** when the file loads, NOT each time the function is called! Every call shares the exact same list in memory.
  - **Fix:** Always use `items=None`, and inside the function write `if items is None: items = []`.
- **2. Floating-Point Money Bugs (`0.1 + 0.2 != 0.3`):**
  - Never use `float` for product prices. Always use **`Decimal`** (or integer cents like `1999`) so prices never lose a cent due to binary rounding.
