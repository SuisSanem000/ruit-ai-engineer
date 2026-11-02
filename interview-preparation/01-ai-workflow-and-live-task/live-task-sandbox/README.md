# Live AI Task Practice Sandbox

- **What is in this folder:**
  - [marketplace_connector.py](./marketplace_connector.py) — Basic, easy-to-read Python code with detailed comments on every block.
  - [test_marketplace_connector.py](./test_marketplace_connector.py) — Basic `pytest` tests with comments explaining how each test works.

---

## 3 Practice Tasks You Might Get in the Interview

- **Task 1 — Fetch & Validate a Marketplace Item:**
  - Fetch item JSON from an API, clean up messy price strings (like `"45,50 €"`), validate required fields with Pydantic, log a warning if the marketplace added new unknown fields, and retry on `429` / `503` errors.
- **Task 2 — Delist a Sold Item Across Marketplaces:**
  - When an item sells on one marketplace, send delist requests to the other marketplaces concurrently. If one marketplace fails with `503`, let the others finish and return a simple report showing which one needs a retry.
- **Task 3 — Stream Large Catalogs with a Generator:**
  - Read a large list of items one by one using `yield` so memory stays low, validate each item, and group them into small batches.
