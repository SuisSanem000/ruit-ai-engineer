# 01 — Whiteboard Challenge 1: Proactive Breakage Detection & Fast Recovery

> **Why This Problem:** Unofficial marketplace APIs (Vinted, Wallapop, eBay, Vestiaire) change without warning. Ruit must detect breakages before sellers complain.

---

## 1. Clarifying Questions to Ask First
- *"Do we want to detect breakages only on real seller jobs, or also run scheduled test checks (synthetic canaries)?"*
- *"When one marketplace breaks, should we pause only the broken action (for example, publishing) while keeping other actions (like reading messages) running?"*
- *"How fast do we want to alert the engineering team on Slack when a schema changes?"*

---

## 2. High-Level Architecture (Boxes to Draw)
- **Marketplace Connector Layer:**
  - Sends HTTP requests and validates every JSON response through a strict **Pydantic** model.
- **Health Event Stream (Redis Counters):**
  - Tracks success rate, status codes (`403`, `429`, `5xx`), and Pydantic validation errors per `(marketplace, action)` over a 5-minute window.
- **Circuit Breaker (Redis Flag):**
  - If validation errors or `403` blocks pass a threshold (for example, >20% in 5 minutes), it flips the state for `(vinted, publish_item)` to `OPEN` (paused).
- **Synthetic Canary Runner (Celery Beat):**
  - Runs a lightweight test account check every 15 minutes during quiet hours to catch marketplace changes early.
- **Alert & Diff Service:**
  - Saves a scrubbed sample of the raw JSON that failed validation, compares it with the expected Pydantic fields, and sends a Slack alert showing the exact changed field.

---

## 3. How We Recover Fast Without Losing Seller Jobs
- **Hold Jobs Safely:**
  - When the circuit breaker is `OPEN`, user jobs are not dropped; they stay in a `PAUSED_INTEGRATION` state in PostgreSQL.
- **Hot-Fix Config or Versioned Adapter:**
  - Store simple field mappings or API version headers in the database/Redis so minor field renames can be fixed without a full code deploy.
- **Gradual Resume (`HALF_OPEN`):**
  - Once fixed, test 1 job first. If it passes, slowly drain the paused queue with rate limits so we don't flood the marketplace.

---

## 4. Key Trade-Offs to Mention
- **Strict Validation vs. Lenient Parsing:**
  - Using `extra="ignore"` in Pydantic ignores harmless new fields that marketplaces add, while strict checks on required fields (`id`, `price`, `status`) catch real breakages immediately.
- **Per-Action Circuit Breaker vs. Global Marketplace Breaker:**
  - Pausing `(vinted, publish)` instead of all of Vinted keeps stock delisting alive even if item creation is broken.
