# 03 — Whiteboard Challenge 3: Rapid New Marketplace Connector Architecture

> **Why This Problem:** Ruit expands to new marketplaces (Todocolección, Milanuncios, Depop, Chrono24). Adding a new marketplace should take days, not months, without touching core business logic.

---

## 1. Clarifying Questions to Ask First
- *"What are the core operations every marketplace needs on Day 1 (for example: login/refresh session, publish item, update price, delist item, fetch orders)?"*
- *"Do different marketplaces have very different category trees and required attributes (like brand, size, condition)?"*
- *"Should connectors support both cloud worker execution and Chrome Extension execution using the same data models?"*

---

## 2. High-Level Architecture (Adapter Pattern)
- **Canonical Ruit Domain Models (Pydantic):**
  - One internal format for `CanonicalListing`, `CanonicalSession`, and `PublishResult`.
  - Core Django services only talk to these canonical models—never directly to Vinted or Wallapop JSON.
- **Base Marketplace Connector Interface (`BaseMarketplaceConnector`):**
  - Defines standard async methods: `authenticate()`, `publish_listing()`, `update_listing()`, `delist_listing()`, and `check_health()`.
- **Per-Marketplace Plugin Folder (`connectors/vinted/`, `connectors/wallapop/`):**
  - **Mapper (`mapper.py`):** Translates `CanonicalListing` into the marketplace's exact payload and maps category/brand IDs.
  - **HTTP Transport (`client.py`):** Handles marketplace-specific headers, TLS impersonation (`curl_cffi`), token refresh, and rate limits.
  - **Response Schemas (`schemas.py`):** Pydantic models that validate the marketplace's raw JSON responses.

---

## 3. How AI Speeds Up Building a New Connector
- **Step 1 — Capture HAR:** Perform login, publish, and delete once in the browser or mobile app and export the `.har` capture.
- **Step 2 — Generate Schemas & Mapper:** Feed sanitized request/response JSON to the AI coding assistant to generate `schemas.py` and `mapper.py` drafts.
- **Step 3 — Replay Recorded Fixtures:** Run `pytest` against saved JSON fixtures (`200`, `401`, `429`, changed schema) before touching live accounts.

---

## 4. Key Trade-Offs to Mention
- **Strict Shared Interface vs. Marketplace-Specific Features:**
  - Keep 90% of actions in the standard interface (`publish`, `update`, `delist`), and use an optional `capabilities` dictionary for special features (like "bump/promote listing" on Wallapop).
