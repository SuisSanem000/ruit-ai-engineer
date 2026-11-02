# API Integrations, Reverse Engineering & Keeping Them Alive

> **From Luis's Email Cheat Sheet:** *"api integrations and reverse engineering"*

---

## 1. How to Rebuild an Undocumented API from Network Traffic

- **Step 1 — Capture Traffic (Web vs Mobile App):**
  - **Web App:** Open Chrome DevTools (**Network** tab $\rightarrow$ filter `Fetch/XHR`, check `Preserve log`), perform the seller actions (*Login $\rightarrow$ Upload Photo $\rightarrow$ Publish Item $\rightarrow$ Edit Price $\rightarrow$ Delete*), and export a **`.har` file**.
  - **Mobile App (Why Mobile APIs Are Often Better):** Mobile app APIs change much less often than websites because marketplaces cannot break old iOS/Android app versions that users have not updated yet!
  - **Inspecting Mobile Traffic:** Route an Android emulator through **`mitmproxy`** (or Proxyman/Charles). If the mobile app blocks proxy certificates (**SSL Pinning**), use **Frida** on a rooted test emulator to disable the SSL certificate check while capturing the endpoints.
- **Step 2 — Find the Exact Call Sequence & Minimal Headers:**
  - Often, publishing an item is a **2 or 3-step sequence**: (1) request an upload URL, (2) upload the photo bytes to S3/cloud storage and get a `photo_id`, and (3) send the listing JSON with that `photo_id`.
  - Use an AI agent to read the `.har` log and find which headers are truly required (`Authorization`, `Cookie`, `X-CSRF-Token`, `X-Device-Id`, `User-Agent`).
- **Step 3 — Handle Token Refresh Safely (The Redis Lock Trick):**
  - Many marketplaces use short-lived access tokens (15 mins) and **single-use refresh tokens**.
  - **Common Bug:** If 5 Celery workers see an expired token at the same time and all 5 try to refresh it, the first worker succeeds and the other 4 reuse an old refresh token—causing the marketplace to think the token was stolen and **logging the seller out completely!**
  - **Fix:** Put a **Redis lock** around token refresh per seller (`lock:refresh:seller_123:vinted`) so only 1 worker refreshes the token while the other 4 wait and use the new token.
- **Step 4 — Use Sticky Residential Proxies:**
  - Always route requests for a specific seller through the **same sticky residential IP in their country** (e.g., a Spanish residential IP for a seller in Madrid) so the marketplace does not flag logins coming from 10 different datacenter countries.

---

## 2. Keeping Integrations Alive (Catching Breakages Before Sellers Do)

- Connect this directly to **your 150-site news crawler** and **your QueryLaw error telemetry**:
- **1. Scheduled Canary Checks (Every 15 Minutes):**
  - Run an automated background check using a Ruit test account on each marketplace every 15 minutes (*Create Draft $\rightarrow$ Edit Price $\rightarrow$ Delete*) to verify the API still works.
- **2. Two-Level Pydantic Validation (Hard Errors vs Soft Drift Warnings):**
  - **Hard Breakage:** If a required field (`external_id`, `price`) is missing or fails validation, raise a breakage error and alert engineers immediately.
  - **Soft Drift Warning:** Use `extra="allow"` in Pydantic to spot when a marketplace quietly adds new fields to its JSON response, logging a warning so you can update your code early.
- **3. Per-Marketplace Circuit Breaker (Protecting Seller Accounts):**
  - If Vinted changes its API and 5 different sellers get `400` or `403` errors within 2 minutes, **stop the Vinted queue automatically (open the circuit breaker)**!
  - Continuing to fire 5,000 broken requests will get your sellers' accounts banned. Pause the queue, save a sample of the failed JSON response, fix the parser with AI, and resume.
