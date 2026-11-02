# TypeScript / Node.js $\rightarrow$ Python / Django Mental Bridge for Simin

> **Why This Guide Exists:** You have 9+ years of senior engineering experience building high-concurrency Node.js/TypeScript backends (60K+ concurrent users), crawlers (150+ sites), and AI validation pipelines (QueryLaw). Luis already knows your background and invited you to the final round in Valencia because your systems & integrations experience is strong.  
> This guide maps your exact Node.js/TypeScript knowledge onto **Python & Django** so you can answer Python-specific questions with senior architectural authority.

---

## 1. Side-by-Side Ecosystem & Tooling Translation

| Concept / Layer | Your TypeScript / Node.js Stack | Ruit's Python / Django Stack | Key Nuance to Highlight in the Interview |
| :--- | :--- | :--- | :--- |
| **Runtime & Concurrency** | V8 Single-Threaded Event Loop (`libuv`) + `Worker Threads` | CPython (`GIL`) + `asyncio` Event Loop / `threading` / `multiprocessing` | Node.js is async-by-default on 1 thread; Python is sync-by-default, releases the **GIL** on I/O (network/disk), and uses `asyncio` for high-concurrency I/O or `multiprocessing` for CPU-bound work. |
| **Web Frameworks** | NestJS / Fastify / Express | **Django** (WSGI/ASGI) + Django REST Framework (DRF) / **Django Ninja** / FastAPI | Django is "batteries-included" (ORM, migrations, auth, admin) like NestJS, whereas FastAPI/Django Ninja feel like Fastify + Zod/TypeScript. |
| **Server Protocol** | Node HTTP Server / uWebSockets | **WSGI** (`Gunicorn` — sync) vs **ASGI** (`Uvicorn` / `Daphne` — async + WebSockets) | ASGI is Django's bridge to async HTTP and WebSockets (`Django Channels`), analogous to upgrading Express to support async streams & Socket.IO. |
| **Runtime JSON Validation** | **AJV** (JSON Schema) / **Zod** / `class-validator` | **Pydantic v2** (`BaseModel`, `TypeAdapter`, Rust `pydantic-core`) | Your multi-layer AJV validation at QueryLaw maps 1:1 to **Pydantic v2** (`model_validate`, `@field_validator`, `@model_validator`, `ConfigDict(extra='ignore')`). |
| **Static Type System** | TypeScript (`interface`, `type`, generics, `tsc`) | Python Type Hints (`typing`, `Protocol`, `TypedDict`, `Generic`) + **`mypy` / `pyright`** | Python type hints are erased at runtime (like TS!), except **Pydantic** uses runtime type annotations (`__annotations__`) to validate payloads automatically! |
| **Linter & Formatter** | ESLint + Prettier / Biome | **Ruff** (written in Rust — replaces Flake8, Black, isort in milliseconds) | Ruff + Mypy/Pyright is the modern Python equivalent of Biome/ESLint + `tsc --noEmit`. |
| **ORM & Migrations** | Prisma / TypeORM / Sequelize | **Django ORM** (`models.Model`, `makemigrations`, `migrate`) / SQLAlchemy | Unlike Prisma/TypeScript where `await` is required on every DB call, classic Django ORM performs **lazy evaluation** and **implicit synchronous queries** on attribute access unless prevented! |
| **N+1 Query Prevention** | Prisma `include` / TypeORM `leftJoinAndSelect` | `select_related()` (SQL `JOIN` for FK/1:1) & `prefetch_related()` (2nd query + Python join for M2M/Reverse FK) | One of the most common Django interview questions—always distinguish `select_related` vs `prefetch_related`. |
| **Background Queues** | BullMQ (Redis) / RabbitMQ (`amqplib`) | **Celery** (with **Redis** or **RabbitMQ** broker) | Celery workers are separate OS processes consuming serialized task messages from Redis/RabbitMQ, just like BullMQ worker processes. |
| **HTTP Client** | `fetch` / `axios` / `undici` | **`httpx`** (sync & async, HTTP/2) / `aiohttp` / `requests` (`Session`) / **`curl_cffi`** (TLS impersonation) | Never use bare `requests.get()` in a loop (creates a new TCP+TLS connection every time!). Always reuse `httpx.AsyncClient()` or `requests.Session()`. |
| **Real-Time / WebSockets** | **Socket.IO** + Redis Adapter (your 60K+ user architecture) | **Django Channels** (ASGI) / FastAPI WebSockets + **Redis Channel Layer (Pub/Sub)** | Identical architecture: stateless ASGI workers hold WS connections and broadcast across nodes via Redis Pub/Sub! |
| **Browser Automation** | Puppeteer / Playwright (TS) | **Playwright for Python** (`playwright.async_api`) / Selenium / CDP | Identical Playwright API (`async with async_playwright() as p:`), same browser contexts, stealth evasions, and network interception (`page.route`). |
| **Structured Logging** | `pino` / `winston` | **`structlog`** / `python-json-logger` + `contextvars` | `contextvars.ContextVar` in Python is the exact equivalent of Node.js `AsyncLocalStorage` for propagating correlation/trace IDs across `async` calls! |

---

## 2. How to Frame Your Background Confidently to Luis

If Luis or the team asks about your primary production experience being TypeScript/Node.js vs Python/Django, use this honest, high-leverage framing:

> *"Across my 9+ years of backend and systems work, my heaviest high-load production APIs (60K+ concurrent users) and my 150-site crawler were built in Node.js/TypeScript alongside PostgreSQL, Redis, RabbitMQ, and Docker, while my recent work has been heavily focused on AI systems, structured validation pipelines, and Python tooling. Because the hard parts of integrations—concurrency bottlenecks, DB locking, Celery/queue idempotency, TLS/anti-bot evasion, schema validation at boundaries, and catching upstream breakages—are language-agnostic systems problems, and because I work with AI agents every day paired with strict static analysis (`ruff`, `mypy`, `pydantic`, `pytest`), I ramp cleanly on Django idioms while bringing battle-tested integration architecture."*

---

## 3. Code Idiom Translation: TS/Node vs Python/Django

### 3.1 Interface / Structural Typing (`interface` $\rightarrow$ `typing.Protocol`)
In TypeScript, interfaces are structural (duck-typed at compile time). In Python, `abc.ABC` is nominal (requires inheritance), whereas **`typing.Protocol`** is structural (just like TypeScript interfaces!):

```python
from typing import Protocol
from pydantic import BaseModel


class ListingPayload(BaseModel):
    sku: str
    title: str
    price_cents: int


# Equivalent to TypeScript: interface MarketplaceConnector { ... }
class MarketplaceConnector(Protocol):
    async def publish_listing(self, payload: ListingPayload) -> str: ...
    async def delist_item(self, external_id: str) -> bool: ...
```

### 3.2 Concurrent Bounded I/O (`Promise.all` + `p-limit` $\rightarrow$ `asyncio.TaskGroup` + `Semaphore`)
When syncing or scraping a marketplace, firing 1,000 unbounded `asyncio.gather()` calls will exhaust connection pools or trigger a `429 Too Many Requests` ban. Always bound concurrency with `asyncio.Semaphore`:

```python
import asyncio
import httpx


async def fetch_item(
    client: httpx.AsyncClient, sem: asyncio.Semaphore, item_id: str
) -> dict:
    async with sem:  # Equivalent to p-limit(10) in Node.js
        resp = await client.get(f"https://api.marketplace.example/items/{item_id}")
        resp.raise_for_status()
        return resp.json()


async def sync_batch(item_ids: list[str]) -> list[dict]:
    sem = asyncio.Semaphore(10)
    timeout = httpx.Timeout(10.0, connect=3.0)
    async with httpx.AsyncClient(http2=True, timeout=timeout) as client:
        # Python 3.11+ structured concurrency (cancels siblings on unhandled error)
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_item(client, sem, i)) for i in item_ids]
        return [t.result() for t in tasks]
```

### 3.3 Preventing Double-Sells in SQL (Django ORM `select_for_update`)
When a second-hand jacket sells on **Vinted**, Ruit must immediately lock the inventory row in PostgreSQL and delist it on **Wallapop** and **eBay** so a concurrent webhook doesn't trigger a double-sale:

```python
from django.db import transaction
from inventory.models import Item, ItemStatus


def mark_item_sold_and_enqueue_delist(item_id: int, sold_on_marketplace: str) -> bool:
    with transaction.atomic():
        # SELECT ... FOR UPDATE NOWAIT locks the row until transaction commits
        item = (
            Item.objects.select_for_update(nowait=True)
            .filter(id=item_id, status=ItemStatus.ACTIVE)
            .first()
        )
        if item is None:
            return False  # Already sold or being processed

        item.status = ItemStatus.SOLD
        item.sold_marketplace = sold_on_marketplace
        item.save(update_fields=["status", "sold_marketplace", "updated_at"])

        # Crucial Django pattern: Only enqueue Celery task AFTER Postgres transaction commits!
        transaction.on_commit(
            lambda: delist_from_other_marketplaces_task.delay(item.id)
        )
        return True
```
> **Pro Tip to Mention to Luis:** Using `transaction.on_commit(...)` before calling `.delay()` on a Celery task prevents a classic Django race condition where the fast Redis/Celery worker picks up the task *before* the PostgreSQL transaction commits, reading stale database state!

