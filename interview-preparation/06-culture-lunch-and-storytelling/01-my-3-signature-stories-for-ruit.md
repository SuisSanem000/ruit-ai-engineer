# Your 3 Signature Engineering Stories for Ruit

> **Why Luis Invited You to Valencia:**  
> *"you built a VS Code extension that hundreds of thousands of developers use, which says a lot about shipping things people rely on."*  
> *"The Dadroit JSON Generator extension you built in three days, and the crawler behind your news app for over 150 sites, are close to the integration work we do."*

Keep these three stories crisp (90 seconds each for the summary, with deep technical layers ready when Luis or Alonso asks follow-up questions).

---

## Story 1: The 150+ Site Crawler & Semantic News Feed (Parsaiane — 60K+ DAU)

- **Why It Maps 1:1 to Ruit:** Crawling and extracting structured data from 150+ independent websites that constantly change their HTML/JSON layouts, rate limits, and anti-bot headers is the **exact same engineering problem** as maintaining 15+ marketplace integrations at Ruit.
- **The 90-Second Narrative:**
  > *"At Parsaiane, we built a semantic news platform serving 60,000+ daily active users that aggregated, scored, and summarized articles from over 150 heterogeneous sources in real time. The hardest problem wasn't writing the initial scraper for site #1—it was **keeping 150 integrations alive simultaneously** when upstream sites silently changed their DOM structure, RSS/JSON payloads, pagination, or rate limits without warning.*
  >
  > *To prevent one broken or slow site from starving the rest of the pipeline, I isolated ingestion by source priority, enforced strict schema validation on extracted payloads before they ever touched our database or OpenAI summarization pipeline, and built per-source health telemetry (tracking empty-field rates, HTTP 403/429 spikes, and latency). Whenever a site's extraction yield dropped or validation failed, we caught the drift automatically before users saw broken feeds."*
- **Deep Technical Follow-Ups to Be Ready For:**
  - **Queue & Concurrency Isolation:** How did you prevent 5 slow sites from blocking 145 fast sites? (*Bounded concurrency per domain, separate priority queues, aggressive connect/read timeouts, and exponential backoff with jitter*).
  - **Deduplication & Idempotency:** How did you avoid re-processing and paying LLM tokens for the same article twice? (*Canonical URL normalization + content hash fingerprinting in Redis/Postgres before queuing LLM scoring*).
  - **Connecting to Python/Ruit:** *"If I were building that pipeline today in Ruit's stack, I'd use `curl_cffi`/`httpx` async workers orchestrated by Celery + Redis with Pydantic v2 validation and per-marketplace circuit breakers."*

---

## Story 2: Dadroit JSON Generator VS Code Extension (630K+ Installs, Shipped in 3 Days) & Multi-GB JSON Viewer

- **Why It Maps 1:1 to Ruit:** Proves two things Luis cares deeply about: (1) **extreme shipping velocity with high quality** (v1 shipped in 3 days, scaled to 630K+ installs), and (2) **deep mastery of JSON schemas, tree structures, streaming memory efficiency, and browser/editor extension architectures**.
- **The 90-Second Narrative:**
  > *"While working on the Dadroit ecosystem—where we built a high-performance desktop JSON Viewer capable of opening multi-gigabyte JSON files for 60K+ users without running out of memory—we noticed developers constantly needed realistic, schema-valid mock JSON datasets for testing APIs. Instead of over-engineering a 3-month project, I scoped, built, and shipped the **Dadroit JSON Generator** VS Code extension in **three days**.*
  >
  > *I focused obsessively on developer ergonomics, zero-latency generation, and clean recursive schema traversal. Then I paired the engineering with technical articles and SEO, driving 540% organic growth to over 630,000 installs and making it a top-10 extension. It taught me how to ship a pragmatic v1 in days, listen directly to users, and iterate on edge cases that only appear when hundreds of thousands of people rely on your tool."*
- **Deep Technical Follow-Ups to Be Ready For:**
  - **Handling Multi-GB JSON Without OOM:** How does a viewer or parser handle a 4GB JSON file without allocating 20GB of DOM/object nodes? (*Lazy streaming/lexing, indexing byte offsets rather than materializing every nested object in RAM, and virtualized tree rendering—the exact same principle behind Python generators (`yield`) and Django's `.iterator()`!*).

---

## Story 3: QueryLaw / TreeScribe — Antifragile AI Decision Engine (95%+ Accuracy & Brittle-Logic Telemetry)

- **Why It Maps 1:1 to Ruit:** Both LLM outputs and third-party marketplace APIs are **non-deterministic, brittle external systems**. Your work at QueryLaw proves you know how to wrap unreliable external calls in deterministic validation gates and observability.
- **The 90-Second Narrative:**
  > *"At QueryLaw, I owned the full stack for an AI legal-tech platform transforming complex European statutes into automated decision graphs. In legal tech, 80% prompt accuracy is unusable—one hallucinated branch breaks the whole decision tree. To reach **95%+ reasoning accuracy**, I engineered an **antifragile AI integration layer**:*
  > 1. *Dynamic context windows that fed only the exact relevant statutory sub-graph.*
  > 2. *Multi-layer JSON Schema (AJV) validation gates—if an output violated structural or cross-field invariants, our pipeline caught the exact validation error and triggered a targeted self-correction or fallback.*
  > 3. *Backend telemetry and side-by-side reviewer tooling that detected brittle logic and edge-case failures in real time so we could reproduce and fix them immediately.*
  >
  > *That architecture is identical to how I think about Ruit's marketplace integrations and AI catalog mapping: never trust an external boundary—validate every payload with Pydantic v2, log schema drift proactively, and build replayable telemetry so we catch breakages before sellers do."*
