# TypeScript / Node.js to Python / Django Bridge

## 1. How to Be Open & Honest About Your Python Level

- **What to tell Luis and the team:**
  - *"I want to be completely open with you: I have never used Python or Django in production."*
  - *"My 9+ years of production experience are in TypeScript/Node.js, PostgreSQL, Redis, RabbitMQ, and Delphi. With Python, I have used it in basic side projects and I reviewed the core syntax and Django concepts before coming here."*
  - *"Because the hard problems in integrations—like async concurrency, database locks, background queues, API reverse engineering, and JSON validation—are the same across languages, and because I work with AI agents every day, I can understand, verify, and ship Python code quickly."*
- **Why this works:**
  - Luis already read your CV and knows your stack is Node.js/TypeScript.
  - Being honest builds huge trust.
  - When you explain **how** Python and Django work under the hood (GIL, async, generators, ORM queries) and map them to Node.js, you prove you are a strong senior engineer who learns fast.

---

## 2. Quick Tool Mapping: Your Stack vs Ruit's Stack

- **Runtime & Async:**
  - **Node.js:** Single-threaded Event Loop (`async/await`, `Promise.all`).
  - **Python:** CPython with the **GIL** + `asyncio` Event Loop (`async/await`, `asyncio.gather`).
- **Web Frameworks:**
  - **Node.js:** NestJS / Express / Fastify.
  - **Python:** **Django** (full framework with ORM, migrations, admin) or **FastAPI / Django Ninja** (fast modern APIs).
- **Web Server Protocol:**
  - **Node.js:** Built-in HTTP server + Socket.IO.
  - **Python:** **WSGI** (`Gunicorn` for normal sync requests) vs **ASGI** (`Uvicorn` for async requests and WebSockets).
- **JSON Validation:**
  - **Node.js:** **AJV** (JSON Schema) or **Zod** (which you used at QueryLaw).
  - **Python:** **Pydantic** (validates JSON data at runtime using Python type hints).
- **Type Checking & Linting:**
  - **Node.js:** TypeScript (`tsc`) + ESLint / Prettier.
  - **Python:** Type Hints (`typing`) + **`mypy` / `pyright`** (type checkers) + **`ruff`** (fast linter and formatter).
- **ORM (Database Layer):**
  - **Node.js:** Prisma / TypeORM / Sequelize.
  - **Python:** **Django ORM** (`Model.objects.filter(...)`).
  - **Important difference:** In Prisma, every DB query needs `await`. In classic Django ORM, queries are **synchronous and lazy**—Django can secretly run an extra SQL query when you access a property like `item.seller.name` if you did not pre-load it!
- **Background Queues:**
  - **Node.js:** BullMQ (Redis) / RabbitMQ.
  - **Python:** **Celery** (worker processes) using **Redis** or **RabbitMQ** as the message broker.
- **HTTP Client:**
  - **Node.js:** `fetch` / `axios`.
  - **Python:** **`requests`** (sync), **`httpx`** (sync and async), or **`curl_cffi`** (impersonates real Chrome TLS fingerprints to avoid bot blocks).
- **Code Examples:**
  - See [django_concepts_examples.py](../02-python-and-django-deep-dive/python-django-labs/django_concepts_examples.py) for basic, commented Python and Django examples.
