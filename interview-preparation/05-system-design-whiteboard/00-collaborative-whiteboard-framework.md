# 00 — Collaborative Whiteboard Framework (45-Minute Structure)

> **Email Cheat Sheet Priority:** *"A real Ruit engineering problem — we'll define requirements together, sketch out a design, and talk through trade-offs. Collaborative, not an exam."*

---

## 1. My 4-Step Time Box (45 Minutes)
- **Step 1 — Ask Questions & Define Scope (Minutes 0–8):**
  - Ask 4–5 clear questions before drawing anything.
  - Agree on scale, failure modes, and what is out of scope.
- **Step 2 — Draw High-Level Architecture (Minutes 8–20):**
  - Draw 4–5 simple boxes on the board:
    - **API Gateway / Backend (Django):** Receives user requests and webhooks.
    - **Database (PostgreSQL):** Source of truth for sellers, items, and stock.
    - **Cache & Queue Broker (Redis):** Fast locks, rate-limit counters, and task queues.
    - **Background Workers (Celery) / Chrome Extension:** Runs marketplace requests in the background.
- **Step 3 — Deep Dive on Hard Edge Cases (Minutes 20–35):**
  - Walk through race conditions, rate limits, broken marketplace responses, and retries.
- **Step 4 — Trade-Offs & Monitoring (Minutes 35–45):**
  - Explain why this design works well today and what we would change at 10x scale.

---

## 2. 5 Questions to Ask at the Start of Any Ruit Design Problem
- **Scale:** *"How many active sellers and listings do we have right now, and what is our target for the next 12 months?"*
- **Latency:** *"Does this action need to happen in real time while the user waits, or can it run in the background within 10–30 seconds?"*
- **Execution Path:** *"Does this marketplace connector run from our cloud workers using proxies, or from the seller's Chrome Extension?"*
- **Failure Impact:** *"What is worse here: a short delay, or doing an action twice (like double-selling an item or double-posting a listing)?"*
- **Human-in-the-Loop:** *"When an integration fails or AI confidence is low, should we pause automatically and alert the seller or engineering team?"*

---

## 3. Useful Upper-B2 Phrases for Collaborative Whiteboarding
- **Starting:** *"Before I draw the boxes, let me ask a few quick questions to make sure I solve the right problem."*
- **Checking Alignment:** *"Here is the basic data flow from Django to Celery and Redis. Does this match how you structure it today, or would you like me to adjust anything?"*
- **Presenting Trade-Offs:** *"We have two options here. Option A is simpler to build today, while Option B handles higher traffic later. For Ruit's current stage, I would start with Option A."*
- **Inviting Feedback:** *"Which part of this diagram should we zoom into first—the database locking or the retry queue?"*
