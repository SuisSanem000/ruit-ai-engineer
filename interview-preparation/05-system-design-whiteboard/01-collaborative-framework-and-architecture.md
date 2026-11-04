# 01 — Collaborative Whiteboard Framework & Core Architecture

> **Email Cheat Sheet:** *"60' minute of a system design challenge: We have ~5 challenges for the following months. We will explain the challenges, and you will choose the one you like. We will design it together and see how it compares to our existing approach. This is teamwork!"*

---

## 1. The 4-Step Collaborative Structure (60 Minutes)

1. **Step 1 — Clarify Requirements & Define Scope (0–10 mins):**
   - Ask 4–5 questions before touching the board: current scale (sellers, listings/day), latency targets (real-time vs 15-second background), execution context (Chrome Extension vs cloud Celery workers), and failure tolerances.
2. **Step 2 — High-Level Architecture Diagram (10–25 mins):**
   - Draw 4 primary boxes: **Django API Gateway**, **PostgreSQL** (Source of Truth), **Redis** (Locks, Rate Limits, Broker), and **Celery Workers** (or Chrome Extension).
3. **Step 3 — Deep Dive on Hard Edge Cases (25–45 mins):**
   - Trace race conditions (double-sells), token expiry, network timeouts, and broken marketplace responses.
4. **Step 4 — Trade-offs, Scale & Observability (45–60 mins):**
   - Discuss database indexing, PgBouncer, cache invalidation, and metrics/alerts.

---

## 2. Key Spoken Phrases for Collaborative Whiteboarding (Upper-B2)

- *"Before I draw the boxes, let me ask a few quick questions to make sure I am solving the exact right problem."*
- *"Here is the basic flow from the Django webhook receiver to Celery and Redis. Does this match how your existing pipeline is structured, or would you like me to adjust anything?"*
- *"We have a clear trade-off here: Option A is faster to build today, while Option B scales better for 10x volume. For Ruit's current stage, I would recommend Option A and migrate when volume demands it."*
- *"Which edge case should we zoom into next—database row locking or the retry queue with rate limits?"*

---

## 3. High-Signal Architectural Blueprint for Any Ruit Challenge

- **Entry Point:** Django ASGI/WSGI endpoint receives webhook from marketplace or action from seller. Returns `200 OK` within 2 seconds.
- **Persistence & Locking:** PostgreSQL holds `listings`, `items`, and `orders`. Updates wrapped in `with transaction.atomic()` using `select_for_update()` to prevent race conditions.
- **Background Orchestration:** Celery worker processes job asynchronously from Redis queue (`delist_urgent` vs `bulk_sync`).
- **External Integration:** Python connector uses `httpx.AsyncClient` or `curl_cffi` with connection pooling, explicit timeouts, and exponential backoff retries.
- **Data Validation:** Strict Pydantic models validate raw JSON and trigger alerts if schema drift occurs.
