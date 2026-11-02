# Collaborative System Design Whiteboard Playbook (15:00 – 16:00 in Valencia)

> **What Luis Wrote in the Email:**  
> *"3. 60' minute of a system design challenge: We have ~5 challenges for the following months. We will explain the challenges, and you will choose the one you like. We will design it together and see how it compares to our existing approach. This is teamwork!"*

---

## 1. How to Choose Which of the ~5 Challenges to Tackle

When Luis and the team present their ~5 upcoming challenges, **choose the one that sits at the intersection of Ruit's hardest integration pain and your strongest battle-tested stories**:

1. **Top Pick A — Proactive Breakage Detection / Self-Healing Integrations / Reverse-Engineered Connector Engine:**
   - *Why pick it:* You built a **150+ site crawler** at Parsaiane AND built **brittle-logic telemetry + multi-layer schema validation** at QueryLaw. You can speak from genuine first-hand production experience!
2. **Top Pick B — AI-Powered Catalog Normalization, Category/Attribute Mapping, or Automated Scraper Repair:**
   - *Why pick it:* Plays directly to your **QueryLaw 95%+ accuracy LLM + JSON Schema validation pipeline** and your **630K-install Dadroit JSON Generator** expertise.
3. **Top Pick C — Real-Time Multi-Marketplace Inventory Sync / Double-Sell Prevention / Hybrid Chrome Extension Architecture:**
   - *Why pick it:* Plays directly to your **60K+ concurrent users Socket.IO/WebSocket + PostgreSQL + Redis + Queue** scaling experience and extension architecture knowledge.

---

## 2. The 60-Minute Collaborative Pacing Blueprint ("This is Teamwork!")

Because Luis explicitly emphasized **"We will design it together and see how it compares to our existing approach. This is teamwork!"**, **do NOT monologue at the whiteboard for 40 minutes**. Treat Luis and the team as your co-architects in a real Lanzadera design session:

### Phase 1: Clarify Scope, Invariants & Failure Modes (Minutes 0 – 10)
Before drawing boxes, write **3 small lists** in the corner of the whiteboard and ask the team to validate them:
1. **Core Functional Goal:** What does success look like for the professional seller?
2. **SLAs & Scale Numbers:**
   - *"How many active professional sellers and total active SKU listings are we designing for over the next 12 months (e.g., 1,000 sellers $\times$ 5,000 items = 5M listings across 10 marketplaces)?"*
   - *"What is our latency SLA? (e.g., < 5 seconds to delist a sold item across channels vs minutes for bulk catalog import?)"*
3. **Hardest External Constraints:**
   - *"Which marketplaces in this flow have official webhooks/APIs (eBay, Shopify) vs undocumented private APIs (Vinted, Wallapop, Depop) vs browser-only constraints?"*

### Phase 2: High-Level Architecture & Data Model (Minutes 10 – 25)
Draw the **5-block backbone** clearly on the whiteboard:
1. **Ingress Layer:** Django ASGI API / Webhook Receiver / Polling Scheduler / Chrome Extension WSS Gateway.
2. **Source of Truth (PostgreSQL):** Draw the 3–4 core tables (`SellerAccount`, `CanonicalItem`, `MarketplaceListing`, `SyncOutboxEvent`) with explicit **state machine statuses** and **idempotency keys**.
3. **Broker & Priority Queues (Redis + Celery):** Show separated queues (`q_critical_delist`, `q_api_sync`, `q_browser_workers`, `q_dlq`).
4. **Connector Execution Layer:** Pluggable `MarketplaceAdapter` (`Protocol`) + Rate Limiter (Redis Token Bucket) + Proxy/Session Manager (`curl_cffi` / Playwright).
5. **Observability & Circuit Breaker Loop:** Pydantic v2 schema-drift telemetry + Prometheus RED metrics + per-marketplace Redis Circuit Breaker.

*Pause and check in with the team:*  
> *"Does this high-level flow match how you separate your Django core from your marketplace workers today, or which part should we zoom into first?"*

### Phase 3: Deep Dive into Race Conditions & Edge Cases (Minutes 25 – 45)
Proactively walk through the **"What Goes Wrong at 3 AM"** scenarios (this is where senior engineers shine):
- **Race Condition:** What happens if two webhooks arrive 50ms apart? (`SELECT ... FOR UPDATE NOWAIT` / optimistic locking `version = version + 1` + `transaction.on_commit()`).
- **Partial Failure:** What if Vinted delists in 200ms, Wallapop succeeds in 400ms, and Depop returns `429 Too Many Requests`? (Per-channel `MarketplaceListing` state machine so only Depop retries with backoff+jitter without re-running Vinted or Wallapop).
- **Silent Upstream Change:** What if Wallapop renames a JSON field on Tuesday morning? (Pydantic `ValidationError` $\rightarrow$ `UpstreamContractBreakageError` $\rightarrow$ trips Circuit Breaker after $N$ failures so we don't get seller accounts banned!).

### Phase 4: Compare with Ruit's Existing Approach & Evolution Path (Minutes 45 – 60)
Ask open, curious questions to compare designs:
- *"How does this compare to your current implementation in production? Where did you hit unexpected bottlenecks with Wallapop or Vinted?"*
- *"If we were shipping a pragmatic v1 of this next Monday in 3 days vs hardening v2 for 15 marketplaces, here is what I'd build first and what I'd defer..."* (Shows startup pragmatism!).

