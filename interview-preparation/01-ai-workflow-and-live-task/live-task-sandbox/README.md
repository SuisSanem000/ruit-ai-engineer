# Ruit Live AI Task Practice Sandbox

This folder contains a **runnable, zero-external-network Python sandbox** designed to practice the 15–20 minute live AI coding task with Luis.

## Files in This Sandbox
- `marketplace_connector.py`: Reference implementation demonstrating:
  1. **Pydantic v2 Boundary Validation & Proactive Schema Drift Detection** (detecting when a marketplace silently adds/changes fields before it breaks sellers).
  2. **Explicit Integration Error Taxonomy** (`RetryableMarketplaceError`, `SellerAuthExpiredError`, `UpstreamSchemaBreakageError`).
  3. **Resilient Async HTTP Client (`httpx.AsyncClient`)** with connection pooling, `Retry-After` header support, exponential backoff + full jitter, and `asyncio.Semaphore` bounded concurrency for multi-marketplace delisting.
- `test_marketplace_connector.py`: Full `pytest` suite using `httpx.MockTransport` (runs in <0.5s offline with zero flakiness).

---

## 3 Realistic 20-Minute Live Task Prompts to Practice

### Practice Prompt 1: Rebuilding & Hardening a Marketplace Listing Client
> *"Here is a sample JSON response captured from Vinted's mobile API when fetching a seller's wardrobe items. Notice that prices sometimes come as strings (`'19.50'`) or dicts (`{'amount': '19.50', 'currency': 'EUR'}`), and occasionally Vinted adds new undocumented fields. Build an async Python client that fetches paginated items, normalizes them into a strict Pydantic model, logs a schema-drift warning if unknown fields appear, and retries on 429/503 with backoff."*

### Practice Prompt 2: Multi-Marketplace Instant Delister (Double-Sell Prevention)
> *"When an item sells on Wallapop, we need to immediately delist it from Vinted, eBay, and Depop concurrently. Write an async coordinator that takes a list of marketplace connectors, executes the delist calls with bounded concurrency, isolates partial failures (so if eBay returns a 503, Vinted and Depop still succeed), and returns a structured reconciliation report telling Celery which specific marketplace needs a retry."*

### Practice Prompt 3: Streaming Generator Pipeline for Large Seller Catalogs
> *"A professional vintage store has 50,000 items in an NDJSON/paginated feed. Write a memory-efficient generator pipeline (`yield` / `async for`) that streams raw records, validates them with Pydantic v2, filters out invalid/sold items without crashing the stream, and yields fixed-size batches of 100 valid items for bulk DB insertion."*

---

## How to Run the Tests Locally

```bash
pytest interview-preparation/01-ai-workflow-and-live-task/live-task-sandbox/
```
