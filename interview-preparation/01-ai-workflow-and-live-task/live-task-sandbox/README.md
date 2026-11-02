# Live AI Task Sandbox

- **What is in this folder:**
  - [marketplace_connector.py](./marketplace_connector.py) — Basic, easy-to-read Python code with detailed comments on every section (cleaning messy marketplace JSON, detecting new unknown fields, retrying on `429`/`503`, stopping on `401`, and delisting items across multiple marketplaces at the same time).
  - [test_marketplace_connector.py](./test_marketplace_connector.py) — Simple `pytest` tests with comments explaining how each test works offline.

- **3 Practice Tasks You Can Try with AI (15–20 Minutes Each):**
  - **Task 1 (Clean & Validate Dirty Marketplace JSON):** Take raw JSON from Vinted or Wallapop where prices come as strings (`"45,50 €"`), convert them into clean numbers with Pydantic, and log a warning if the marketplace adds new unknown fields.
  - **Task 2 (Retry on Rate Limits, Stop on Auth Errors):** Fetch a listing from an API, retry up to 3 times if you get HTTP `429` or `503`, and stop immediately without retrying if you get HTTP `401`.
  - **Task 3 (Delist Sold Item Across Marketplaces):** When an item sells on one marketplace, call the delist endpoint on Vinted and eBay at the same time using `asyncio`, and return which ones succeeded and which ones need a retry.
