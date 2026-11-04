# 01 — TS/Node to Python/Django Bridge & Honest Story

> **Your Honest Positioning:** You have 9+ years in Node.js/TypeScript, SQL, Redis, and Delphi. You have **never used Python or Django in production**, only in basic side projects and syntax review. Core backend principles are identical.

---

## 1. Quick Concept Bridge: TypeScript/Node.js vs. Python/Django

| Concept | Node.js / TypeScript | Python / Django | What to Keep in Mind |
| :--- | :--- | :--- | :--- |
| **Runtime & Event Loop** | Single-threaded V8 event loop (libuv). Non-blocking I/O. | CPython has **GIL** (Global Interpreter Lock). `asyncio` runs single-threaded event loop. | For CPU work: Node uses worker threads/clusters; Python uses `multiprocessing` or Celery. |
| **Async Syntax** | `async function` / `await Promise` | `async def` / `await coroutine` | In Python, calling a coroutine without `await` does not run it; it just returns a coroutine object. |
| **Package Management** | `npm` / `pnpm`, `package.json`, `node_modules` | `pip` / `uv` / `poetry`, `pyproject.toml`, `.venv` | Python uses virtual environments (`.venv`) to isolate dependencies per project. |
| **Data Validation** | `Zod` / `AJV` (JSON Schema) | `Pydantic` (`BaseModel`) | Both validate at runtime, parse strings to types, and strip extra fields. |
| **Web Framework** | Express / Fastify / NestJS | Django (monolith) / FastAPI (microservices) | Django has built-in ORM, admin, auth, and migrations. |
| **Web Server Interface** | Native Node HTTP server | **WSGI** (sync, e.g. Gunicorn) vs **ASGI** (async, e.g. Uvicorn) | Django async views require ASGI server. |
| **ORM & Relations** | Prisma / TypeORM / Sequelize | Django ORM | `select_related` = SQL `JOIN` (1-to-1/FK). `prefetch_related` = 2 queries in Python memory (M2M). |
| **Row Locking** | `SELECT ... FOR UPDATE` via raw SQL or query builder | `Item.objects.select_for_update()` inside `transaction.atomic()` | Locks row until transaction commits to prevent double-selling. |
| **Background Queues** | BullMQ / Bee-Queue (Redis-backed) | Celery (Redis / RabbitMQ broker) | Celery workers run separate processes. Tasks need `acks_late=True` and idempotency keys. |

---

## 2. Classic Python Gotchas for Node.js Engineers

- **Mutable Default Arguments:** Never write `def add(item, items=[])`. The `[]` is created once at load time and shared across all calls. Use `items=None` and create `items = []` inside.
- **Synchronous Blocking in Async:** Never run blocking code (e.g., `requests.get()` or normal Django ORM queries) inside `async def` views. It freezes the entire event loop. Use `httpx.AsyncClient` or wrap with `sync_to_async`.
- **Indentation is Syntax:** Blocks are defined by whitespace, not `{}` braces.

---

## 3. How to Answer "What is your Python experience?" (Upper-B2)

> *"I want to be completely upfront: my 9+ years of production experience are in Node.js, TypeScript, SQL, and Redis. I have not used Python or Django in production—only in personal side projects and syntax review. However, the core backend challenges at Ruit—database locking, async job queues, race conditions, and API integrations—are problems I have solved at scale for years. With my strict testing habits and AI tools, I can write clean, safe Python immediately."*
