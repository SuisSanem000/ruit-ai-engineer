# 05 — Whiteboard Challenge 5: Hybrid Chrome Extension & Cloud Worker Execution

> **Why This Problem:** Ruit uses a Chrome Extension (`Ruit Chrome Extension`) alongside backend servers. Some marketplaces block data-center IPs strictly, so running actions through the seller's real browser or routing intelligently between browser and cloud is a major architectural advantage.

---

## 1. Clarifying Questions to Ask First
- *"Which actions run in the Chrome Extension today versus on the backend Celery workers?"*
- *"What happens when an item sells at 3:00 AM and the seller's laptop and Chrome browser are closed?"*
- *"Do we sync cookies/tokens from the extension to the backend so cloud workers can act as a backup?"*

---

## 2. High-Level Architecture (Smart Job Router)
- **Task Router in Django / Celery:**
  - Classifies every marketplace job by **Urgency** and **Anti-Bot Risk**:
    - **Low Urgency + High Anti-Bot Risk (e.g., bulk publishing 50 new listings):** Prefer the **Chrome Extension** when the seller's browser is online (uses the seller's residential IP and real browser fingerprint for free).
    - **High Urgency (e.g., delisting a sold item at 3:00 AM):** If the extension is offline for more than 15 seconds, automatically fall back to a **Cloud Worker + Residential Proxy** using the latest synced session token.
- **Extension Heartbeat & Job Polling:**
  - The Chrome Extension MV3 service worker sends a heartbeat every 30 seconds (`chrome.alarms`) or keeps a lightweight WebSocket connection while the seller's browser is open.
- **Encrypted Session Vault:**
  - When the seller logs into Vinted or Wallapop in Chrome, the extension securely syncs the fresh session token and `User-Agent` to the Ruit backend (encrypted at rest).

---

## 3. Handling Edge Cases Safely
- **Preventing Double Execution (Extension + Cloud Worker):**
  - Before either the extension or a cloud worker runs a job, it must claim a **Redis lease lock** (`job_lock:{job_id}` with a 60-second TTL).
  - If the extension closes mid-job, the lease expires after 60 seconds and a cloud worker can safely check if the listing exists and finish the job.
- **Rate-Limiting the Seller's Home IP:**
  - The extension enforces human-like delays with random jitter between requests so Ruit never gets the seller's home Wi-Fi IP blocked.
