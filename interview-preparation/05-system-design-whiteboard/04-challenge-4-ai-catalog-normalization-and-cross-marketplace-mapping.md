# 04 — Whiteboard Challenge 4: AI Catalog Normalization & Cross-Marketplace Mapping

> **Why This Problem:** Ruit states: *"With a single photo, our AI identifies the product, generates optimised descriptions, estimates prices, and publishes simultaneously on Vinted, Wallapop, eBay, Vestiaire Collective, and more."* Each marketplace has its own category tree, brand IDs, size systems, and condition labels.

---

## 1. Clarifying Questions to Ask First
- *"Does the seller wait on the screen while AI generates the listing, or do they upload a batch of photos in the background?"*
- *"How many categories and brands does each marketplace have, and how often do they change?"*
- *"Can the seller review and edit the AI-generated fields before publishing?"*

---

## 2. High-Level Architecture (Two-Stage Pipeline)
- **Stage 1 — Vision & Extraction into Ruit Canonical Listing:**
  - Seller uploads 1–5 photos (and optional short notes).
  - Multimodal LLM extracts a structured `CanonicalProductDraft` validated by **Pydantic**: title, description, brand name, category path, color, material, condition, and suggested price range.
- **Stage 2 — Deterministic + Embedding Mapping to Each Marketplace:**
  - **Never ask the LLM to guess raw Vinted or eBay category IDs directly** (LLMs hallucinate numeric IDs).
  - Instead, match the canonical category/brand against a pre-indexed lookup table in PostgreSQL (`pgvector` / fuzzy text search) to find the top 3 matching IDs for Vinted, Wallapop, and eBay.
  - A small deterministic mapper (or constrained LLM pick from the top 3 valid candidates) selects the exact `category_id`, `brand_id`, and `size_id` for each marketplace.

---

## 3. Making It Fast, Cheap, and Reliable
- **Cache Brand & Category Mappings in Redis:**
  - Once `"Nike -> Air Force 1 -> EU 42"` is mapped to Vinted and Wallapop IDs, cache that mapping in Redis so future shoes skip AI mapping completely.
- **Confidence Score & Seller UI Fallback:**
  - If an attribute (like exact shoe size) cannot be read from the photo, return `confidence: low` and highlight just that one dropdown in the UI for the seller to pick in 2 seconds.
- **Async Streaming UI:**
  - Return the title and description first in 2–3 seconds while marketplace-specific category and price lookups finish in parallel.
