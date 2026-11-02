# 02 — Whiteboard Challenge 2: Multi-Marketplace Inventory Sync & Preventing Double-Sells

> **Why This Problem:** Ruit cross-lists a single physical second-hand item across Vinted, Wallapop, eBay, and Vestiaire. When it sells on one platform, Ruit must delist it everywhere else immediately so the seller never sells the same item twice.

---

## 1. Clarifying Questions to Ask First
- *"Are most items single-quantity (quantity = 1, typical for second-hand fashion), or do sellers also have multi-quantity SKUs?"*
- *"How do we learn that an item sold—via email/push webhooks, Chrome Extension polling, or cloud worker polling?"*
- *"What should happen if delisting fails on one marketplace because that marketplace is temporarily down?"*

---

## 2. High-Level Architecture (Boxes to Draw)
- **Sale Detection Ingestor:**
  - Receives sale events from webhooks, email parsers, or polling workers.
- **PostgreSQL Inventory Table (Source of Truth):**
  - Stores `item_id`, `available_quantity`, `version`, and `status` (`ACTIVE`, `RESERVED`, `SOLD`), plus a `marketplace_listings` table linking each marketplace listing ID to the master `item_id`.
- **Atomic Reservation Service (Django):**
  - Uses PostgreSQL `SELECT ... FOR UPDATE` (or optimistic `version` update) inside `transaction.atomic()` so only the first sale event wins.
- **Transactional Outbox & High-Priority Celery Queue:**
  - Writes `DELIST_LISTING` jobs for all other marketplaces in the same database transaction, then pushes them to a high-priority Celery queue (`delist_urgent`).
- **Delist Workers:**
  - Execute the delist calls in parallel across the remaining marketplaces.

---

## 3. Handling Race Conditions & Partial Failures
- **Two Buyers Click Buy at the Same Second (Vinted + Wallapop):**
  - Event 1 locks the PostgreSQL row, changes status from `ACTIVE` to `SOLD`, and queues delist jobs for Wallapop, eBay, and Vestiaire.
  - Event 2 arrives 200ms later, sees status is already `SOLD`, records a `DOUBLE_SELL_CONFLICT` alert in PostgreSQL, and immediately notifies the seller via WhatsApp/email/dashboard to cancel the second order quickly.
- **Target Marketplace Is Down During Delist:**
  - Retry with exponential backoff + jitter.
  - If still failing after 3 tries, set the listing price/visibility to hidden if supported, or send an urgent alert to the seller to delist manually on their phone.
- **Idempotency:**
  - If a listing is already deleted on Wallapop (`404 Not Found`), treat `404` as a **success** (`ALREADY_DELISTED`) so retries stop cleanly.
