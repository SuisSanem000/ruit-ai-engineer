# The GIL, Concurrency & Async in Python

> **Code examples with detailed comments:** [test_python_deep_dive_labs.py](./python-django-labs/test_python_deep_dive_labs.py)

---

## 1. What Is the GIL (Global Interpreter Lock)?

- **Simple Definition:** The GIL is a lock inside standard Python (CPython) that allows **only one thread to execute Python code at a time** inside a single process.
- **Why Python Has It:**
  - Python cleans up memory by counting how many variables point to each object (**reference counting**).
  - If two threads changed that reference count at the exact same time without a lock, memory would get corrupted or crash.
  - Putting one global lock around the Python interpreter kept single-threaded code fast and simple.

---

## 2. Network I/O vs Heavy CPU Work (The Most Important Rule)

- **Network & Disk I/O (API calls, Database queries, Redis, File reads):**
  - While waiting for a network response from Vinted or PostgreSQL, **Python releases the GIL**.
  - This means other threads or `async` tasks can run while waiting for the network.
- **Heavy CPU Work (Resizing images, parsing huge HTML/JSON in pure Python, math):**
  - CPU work **holds onto the GIL**.
  - Running 4 threads on 4 CPU cores for heavy CPU work will NOT run 4x faster—in fact, it is slightly slower because the threads fight over the lock.
- **How to Speed Up CPU Work in Python:**
  - **Multiple Processes (`multiprocessing` or Celery workers):** Starts separate OS processes. Each process has its own Python interpreter and its own independent GIL, so they run on all CPU cores at the same time.
  - **Fast C/Rust Libraries:** Tools like `Pydantic` (written in Rust) do the heavy work in compiled code outside Python.
  - **Python 3.13+ Update:** Recent Python versions added an optional **free-threaded mode** (`--disable-gil`) that removes the GIL, though most production teams still use `asyncio` + multiple processes today.

---

## 3. When to Use `asyncio` vs `threading` vs `multiprocessing`

- **`asyncio` (Event Loop — Single Thread):**
  - **Best for:** Making hundreds or thousands of network calls at the same time (like calling 10 marketplace APIs or holding WebSockets).
  - **How it works:** Works just like the **Node.js Event Loop** you know well. One thread switches between tasks whenever it hits an `await`.
  - **Main Rule:** Never call a blocking function like `time.sleep()` or `requests.get()` inside an `async def` function, because it freezes the entire event loop. Always use `await asyncio.sleep()` and `httpx.AsyncClient`.
- **`threading` (Multiple Threads in 1 Process):**
  - **Best for:** Running older synchronous libraries (like a sync database call or sync SDK) in the background without blocking the main thread.
  - **Downside:** Each thread uses more RAM (~8 MB) than an `async` task (~2 KB), and sharing variables between threads requires locks (`threading.Lock`) to avoid race conditions.
- **`multiprocessing` (Multiple OS Processes):**
  - **Best for:** Heavy CPU work that needs multiple CPU cores.
  - **Downside:** Uses the most RAM because each process loads a full copy of Python.

---

## 4. Can Single-Threaded `asyncio` Still Have Race Conditions?

- **Yes!** Even though `asyncio` runs on one single thread, a function pauses every time it hits `await`.
- If Task A reads an item's stock (`stock = 1`), pauses at an `await`, and Task B also reads `stock = 1` before Task A saves `stock = 0`, both tasks think the item is available.
- **Fix:** Use `asyncio.Lock` inside one process, and use **PostgreSQL row locks** or **Redis locks** across multiple worker servers.
