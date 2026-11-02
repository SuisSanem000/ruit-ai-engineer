# Making Robust Python: Type Hints, Pydantic & Static Analysis

> **Luis's Cheat Sheet:** *"how to make robust Python through type hints, static analysis, etc. ... json validation"*

---

## 1. Why Python Needs Extra Safety Checks

- By default, Python is dynamically typed: it does not check types until a line of code actually runs.
- In marketplace integrations, passing raw untyped dictionaries (`data["item"]["price"]`) causes sudden production crashes (`KeyError`, `TypeError`) when a marketplace changes a field or sends `None`.
- To make Python as safe as TypeScript, we use **two layers**:
  1. **Type Hints + Static Analysis (`mypy` & `ruff`)** before code runs.
  2. **Runtime Data Validation (`Pydantic`)** when external JSON arrives.

---

## 2. Layer 1: Type Hints & Static Analysis (`mypy`, `pyright`, `ruff`)

- **Type Hints:**
  - Adding types to variables and function arguments/returns (like `def get_price(sku: str) -> float:`).
  - Important note: **Python ignores type hints at runtime**—they do not slow down your code, and Python alone will not stop you from passing the wrong type.
- **Static Type Checkers (`mypy` or `pyright`):**
  - Tools that read your type hints in your editor and CI pipeline (just like `tsc` in TypeScript).
  - They catch bugs—like forgetting to handle `None` (`Optional`) or passing a `str` instead of an `int`—before you deploy.
- **Linter & Formatter (`ruff`):**
  - A very fast tool (written in Rust) that replaces older tools like Flake8, Black, and isort.
  - Catches unused imports, bad formatting, and common Python mistakes in milliseconds.

---

## 3. Layer 2: Runtime JSON Validation (`Pydantic`)

- **Why Type Hints are not enough for external APIs:**
  - `mypy` only checks your own code before runtime. It cannot know what Vinted or Wallapop's server will send at 3 AM.
- **How Pydantic works (Your Python version of AJV / Zod):**
  - You define a class inheriting from `pydantic.BaseModel` with type hints.
  - Unlike normal Python classes, **Pydantic reads those type hints at runtime** to validate and clean incoming JSON data!
  - If a required field is missing or cannot be converted to the right type, Pydantic immediately raises a clear `ValidationError` showing the exact broken field.

---

## 4. Two Classic Python Mistakes to Avoid

- **Mistake 1 — Mutable Default Arguments:**
  - Never use a list or dict as a default argument in a function (like `def add_item(x, items=[]):`).
  - Python creates that default list **only once** when the file loads, so every function call shares the exact same list!
  - **Fix:** Use `items=None` as the default, and create a new `[]` inside the function.
- **Mistake 2 — Catching Everything Silently:**
  - Never write `except Exception: pass`. Always catch specific errors and log them.

---

## 5. Simple Code Examples

- See [django_concepts_examples.py](./python-django-labs/django_concepts_examples.py) and [test_python_deep_dive_labs.py](./python-django-labs/test_python_deep_dive_labs.py) for basic, commented examples.
