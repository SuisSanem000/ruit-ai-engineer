# 01 — My 3 Signature Stories for Ruit (STAR Format)

> **Email Cheat Sheet Priority:** *"Wait for us to ask: 'Talk to us about a project you built from scratch or a technical challenge you're proud of.' Be specific — architecture decisions, what went wrong, what you'd do differently."*

---

## Story 1: Building a Multi-Tenant SaaS Platform from Scratch (`b2b-api` at Visual Meta / Shopping.de)
- **Situation:**
  - At Visual Meta (Axel Springer), our e-commerce marketplaces in Germany (`ladenzeile.de` and `shopping.de`) needed a new B2B partner portal so thousands of merchants could manage product catalogs, campaigns, and performance metrics.
- **Task:**
  - I took full ownership of designing and building the backend (`b2b-api`) from scratch for a multi-tenant SaaS system with 4 user roles (`admin`, `manager`, `partner`, `user`).
- **Action (Architecture Decisions):**
  - Built the backend with Node.js, TypeScript, Express, MySQL, and Redis.
  - Designed strict multi-tenant data isolation so a partner could never query another partner's SKU data.
  - Added Redis caching with a 15-minute TTL for heavy dashboard aggregation queries and used database transactions for account and role changes.
  - Containerized the service with Docker and set up Jenkins CI/CD pipelines.
- **What Went Wrong & How I Fixed It:**
  - Early on, large merchants with tens of thousands of products caused slow dashboard queries and high memory usage when exporting reports.
  - I fixed this by replacing full in-memory data loads with paginated SQL queries, composite indexes on `(partner_id, created_at)`, and Redis caching.
- **What I Would Do Differently Today:**
  - I would add cursor-based pagination and background export workers from Day 1 instead of waiting for large merchants to hit timeouts.

---

## Story 2: Migrating Legacy C++ Systems & Fixing High-Concurrency SQL Deadlocks (Dotin Banking)
- **Situation:**
  - At Dotin (a core banking company with 1,000+ employees), our legacy C++ middleware handled high-volume EFTPOS card transactions for millions of bank customers, but it was hard to maintain and suffered from concurrency bottlenecks during peak hours.
- **Task:**
  - Lead a 6-person team to migrate critical banking modules from C++ to Delphi and optimize our Oracle PL/SQL transaction procedures.
- **Action (Architecture Decisions):**
  - Re-architected the transaction pipeline using worker thread pools and non-blocking I/O.
  - Profiled slow Oracle SQL queries, removed unnecessary table locks, and enforced a consistent row-locking order (`SELECT ... FOR UPDATE`) across transactions.
- **What Went Wrong & How I Fixed It:**
  - During peak load, two concurrent settlement jobs locked accounts in opposite orders, causing database deadlocks.
  - I fixed this by sorting account IDs before locking rows and shortening the transaction scope so external network calls never happened inside an open database transaction.
- **Result:**
  - Reduced system crash rate by **75%** and improved transaction response times by **65%**.
- **What I Would Do Differently Today:**
  - I would introduce an event-driven outbox pattern earlier so slow downstream notifications are completely separated from core ledger updates.

---

## Story 3: Leading the Rewrite of a Legacy PHP Platform into Modern Services (`shop-Engine` at Visual Meta)
- **Situation:**
  - Our main e-commerce platform served millions of product listings, but the legacy PHP monolith was slow, fragile, and difficult for engineers to deploy safely.
- **Task:**
  - Lead a team of 4 developers to extract and rewrite core catalog and user services into a modern Node.js + TypeScript + PostgreSQL + Redis architecture.
- **Action (Architecture Decisions):**
  - Used the **Strangler Fig pattern**: we migrated endpoints one by one behind our routing layer instead of doing a risky "big bang" rewrite.
  - Added strict TypeScript validation at API boundaries and automated integration tests in GitLab CI before switching traffic.
- **What Went Wrong & How I Fixed It:**
  - Legacy PHP data had inconsistent field formats (missing attributes and weird encodings) that broke our strict new schemas during the first shadow traffic test.
  - We built a normalization and fallback layer that cleaned dirty legacy records and logged warnings without crashing user requests.
- **Result:**
  - Improved response times by **40%**, cut infrastructure costs by **25%**, and reduced customer-facing errors by **60%**.
