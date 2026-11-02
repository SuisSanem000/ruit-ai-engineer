# The GIL, Concurrency & Async Python

> **Luis's Cheat Sheet:** *"concurrency, async ... gauge the extent of your Python and Django knowledge, especially around the GIL"*

---

## 1. What Is the GIL (Global Interpreter Lock)?

- **Definition:** The GIL is a lock inside standard Python (CPython) that allows **only one thread to run Python code at a time** inside a single process.
- **Why Python has it:**
  - Python frees memory by counting how many variables point to each object (**reference counting**).
  - If two threads changed that reference count at the exact same moment without a lock, memory would get corrupted and crash.
  - Instead of putting slow locks on every single variable, Python uses one global lock (the GIL).

---

## 2. How the GIL Affects Different Types of Work

- **I/O-Bound Work (API Calls, Database Queries, Reading Files):**
  - While Python is waiting for the network or database to respond, **it releases the GIL**.
  - Because the GIL is released during network waits, **`asyncio` and threads work very well** for calling 10+ marketplaces at the same time.
- **CPU-Bound Work (Heavy Math, Image Resizing, Huge Loops):**
  - CPU work never waits for the network, so it keeps holding the GIL (switching threads every 5ms).
  - Running 4 threads on CPU work is often **slower** than 1 thread because threads waste time fighting over the lock.
- **How to speed up CPU-bound work in Python:**
  - **Multiple Processes (`multiprocessing` or multiple Celery workers):** Starts separate OS processes. Each process has its own separate memory and **its own separate GIL**, so it uses all CPU cores.
  - **C / Rust libraries:** Tools like **Pydantic** or **Pillow** run heavy work in compiled C/Rust code outside the GIL.
  - **Python 3.13+ Update (Good bonus point):** Newer Python versions (3.13/3.14) added an experimental **free-threaded mode** that can turn off the GIL.

---

## 3. When to Use `asyncio` vs `threading` vs `multiprocessing`

- **`asyncio` (Event Loop — Single Thread):**
  - Works just like Node.js `async / await`.
  - Uses very little memory and can handle **thousands of concurrent HTTP or WebSocket connections**.
  - **Main rule:** Never put a blocking call (like `time.sleep()` or `requests.get()`) inside an `async def` function, because it freezes the entire event loop.
- **`threading` (Multiple Threads in 1 Process):**
  - Good when you have to use an older synchronous library that does not support `async / await`.
  - Higher memory cost than `asyncio` (~8 MB per thread) and risk of race conditions on shared variables.
- **`multiprocessing` (Multiple Processes):**
  - Best for heavy CPU tasks.
  - Uses the most memory because each process loads a full copy of Python.

---

## 4. Simple Code Examples

- See [test_python_deep_dive_labs.py](./python-django-labs/test_python_deep_dive_labs.py) for basic, commented examples of `async / await` in Python.
