# Epic 8: Async Database Refactor - Technical Design Specification

**Status:** Phase 1 (Dual-Engine foundation, `workspaces.py`, `agents.py`) COMPLETED. Phase 2 (remaining routes) pending.

## 1. Overview and Purpose

This document outlines the technical architecture and migration strategy for transitioning the AgencyOS database layer from synchronous operations to asynchronous operations using `asyncpg` and SQLAlchemy's async extensions. The primary goal is to unblock horizontal scalability by eliminating event loop blocking without introducing regressions, specifically addressing the technical pitfalls encountered in previous refactoring attempts.

## 2. Ecosystem Review Board Alignment

In accordance with the `.clinerules` mandate for major platform shifts, this Epic qualifies as a Phase Gate transition touching core infrastructure. The design adheres to the following constraints:

*   **Infrastructure Maintainer (Server Load):** The Dual-Engine strategy ensures database connection limits are respected across both sync and async pools during the transition.
*   **Incident Response Commander (Kill Switches):** A strict feature-toggling mechanism is required at the route level to immediately revert to synchronous execution if latency or error thresholds are breached.
*   **Agentic Identity Trust:** No changes to existing authorization, data integrity, or tenant isolation models will occur. The underlying data schema remains untouched.
*   **Finance Analyst (Cost Containment):** The transition to async allows significantly higher throughput, risking sudden auto-scaling events on managed Postgres and Redis clusters. Hard caps on connection pools, explicit limits on concurrent pgvector searches per tenant, and strict guardrails on auto-scaling triggers MUST be enforced to prevent unexpected infrastructure cost spikes.

## 3. Dual-Engine Side-by-Side Strategy

To guarantee zero downtime and zero regression, we will implement a **Dual-Engine Side-by-Side Strategy**. This avoids the "big bang" release pattern that caused the previous failure.

### 3.1. Database Configuration and Session Management

*   **Legacy Sync Engine (`get_db`):** The existing SQLAlchemy synchronous engine (using `psycopg2`) and its associated session maker (`get_db` dependency) will remain **completely untouched**.
*   **New Async Engine (`get_async_db`):** A new asynchronous SQLAlchemy engine will be instantiated using the `asyncpg` driver. We will create a new async session maker dependency (`get_async_db`).
*   **Coexistence:** Both engines will be initialized on application startup. They will run concurrently, connecting to the same underlying Postgres database. Connection limits must be carefully partitioned (e.g., if max connections = 100, allocate 50 to sync and 50 to async during the migration phase) to prevent database exhaustion.

### 3.2. Route-by-Route Migration Path

We will port operations route-by-route, module-by-module.
1.  Identify a target route (e.g., `GET /api/workspaces/{id}`).
2.  Duplicate the underlying CRUD functions in the data access layer (DAL). For example, `get_workspace()` becomes `get_workspace_async()`.
3.  Update the target route handler to use `async def` and inject the `get_async_db` dependency.
4.  Modify the handler to call `get_workspace_async(db)`.

### 3.3. Feature Toggling and Rollback (Kill Switch)

Every migrated route must be wrapped in a feature toggle (managed via environment variables or a dynamic config service like LaunchDarkly/Redis).

```text
IF FEATURE_TOGGLE_ASYNC_WORKSPACES == TRUE:
    Route handler uses get_async_db and async DAL
ELSE:
    Route handler uses get_db and legacy sync DAL
```

If anomalies are detected in production monitoring (e.g., elevated error rates, memory leaks), the toggle can be flipped instantly to restore synchronous execution without a redeployment.

## 4. Addressing Previous Failures (Technical Safeguards)

The previous async migration failed due to specific SQLAlchemy architectural nuances. This design enforces strict rules to prevent recurrence.

### 4.1. The `.scalars()` Chaining Pitfall

**The Problem:** In SQLAlchemy 2.0 async mode, querying requires the `session.execute()` pattern followed by `.scalars().all()`. The previous attempt failed because developers chained synchronous methods on async results, or attempted lazy-loading of relationships outside the async session context, leading to `MissingGreenlet` errors.

**The Solution:**
*   **Strict Eager Loading:** All required relationships MUST be explicitly eager-loaded using `selectinload` or `joinedload` within the initial async query.
*   **No Lazy Loading:** Lazy loading is strictly prohibited in the async DAL. Any attempt to access a relationship that was not eager-loaded will fail.
*   **Execution Pattern Standard:** All list queries must strictly follow: `result = await session.execute(stmt); return result.scalars().all()`. Single items must use `.scalar_one_or_none()`.

### 4.2. Connection Pooling and Starvation (Blast Radius & Cascading Failures)

**The Problem:** `asyncpg` can aggressively open connections under high concurrent load. In the previous failure, the connection pool was exhausted because the application spawned thousands of coroutines waiting for a database connection, leading to deadlocks and timeouts. This has the potential to cause cascading failures across the entire system.

**The Solution:**
*   **Strict Pool Sizing & Cost Caps:** The async engine must be configured with a strict `pool_size` and `max_overflow`. To prevent runaway managed database costs, connection pool limits must act as a hard ceiling. Auto-scaling rules for the database must be explicitly bounded or disabled during the initial rollout to avoid unexpected cost spikes.
*   **Tenant Concurrency Limits (pgvector):** High-throughput async routes could enable abuse of expensive operations like vector searches. We must enforce strict rate limits on concurrent `pgvector` searches per tenant (e.g., max 5 concurrent searches) to contain compute costs.
*   **`pool_timeout` Enforcement:** A realistic `pool_timeout` (e.g., 5-10 seconds) must be set. If a connection cannot be acquired, the application should fail fast (returning a 429 Too Many Requests or 503 Service Unavailable) rather than queuing indefinitely and consuming memory or triggering auto-scaling.
*   **PgBouncer / Connection Multiplexer:** Ensure the infrastructure utilizes a connection pooler like PgBouncer in front of the database to handle the high volume of short-lived async connections efficiently.
*   **Isolating LLM Kill Switch:** **CRITICAL:** The LLM Kill Switch architecture MUST NOT share the same `asyncpg` connection pool or event loop context if possible. It must be resilient against total `asyncpg` pool exhaustion. If the main async pool crashes or locks up, the Kill Switch API endpoints must remain operational to halt runaway LLM agent costs. The Kill Switch should maintain a dedicated, isolated minimal connection (or fallback to an isolated Redis check) to ensure uninterrupted accessibility.

### 4.3. Transaction Management (ACID)

**The Problem:** Unintended side effects occurred when async sessions were not explicitly committed or rolled back when exceptions were raised.

**The Solution:**
*   The `get_async_db` dependency must yield the session within a `try...except...finally` block, ensuring `await session.rollback()` is explicitly called on any exception, and `await session.close()` is guaranteed in the `finally` block.

### 4.4. Infrastructure Constraints (OOM Prevention)

**The Problem:** The Dual-Engine strategy necessitates running both the legacy synchronous connection pool (`psycopg2`) and the new asynchronous connection pool (`asyncpg`) side-by-side on the same FastAPI pods. This inherently increases the memory footprint per pod and effectively doubles the connection overhead. Without strict resource management, this concurrent overhead will lead to Out Of Memory (OOM) crashes on the Kubernetes cluster during the transition phase.

**The Solution:**
*   **Pod Memory Limits:** The Kubernetes deployment for FastAPI pods MUST be updated to increase the `limits.memory` by a minimum of 40% (e.g., from 512Mi to 768Mi or 1Gi) specifically for the duration of the rollout phase to accommodate the dual connection pools and the increased memory consumption of `asyncpg` coroutines.
*   **Kubernetes HPA Settings:** The Horizontal Pod Autoscaler (HPA) must be recalibrated. The `targetCPUUtilizationPercentage` should be temporarily lowered, and a new `targetMemoryUtilizationPercentage` threshold (e.g., 70%) MUST be added to ensure the HPA aggressively scales out *before* pods reach their memory limits and trigger OOMKills. 
*   **Connection Pooling Metrics Reporting:** Prometheus metrics must be explicitly added to both the sync and async session makers to emit real-time stats on `pool_size`, `checkedout`, `overflow`, and `timeout`. Dashboards must be updated to monitor these metrics side-by-side. If the combined connection count per pod approaches the maximum threshold, the Kill Switch (Section 3.3) must be triggered to prevent cascading database starvation.

## 5. Testing and QA Gate Strategy

To pass the rigorous QA Gate, we will implement the following:

1.  **Dual-Read Shadowing (Safe Mode):** For high-risk read routes, we will implement a "shadow mode." The request will execute synchronously (returning the result to the user), but spawn an async background task to execute the identical query via `asyncpg`. The results of both will be hashed and compared. Mismatches will be logged as critical alerts without impacting the user.
2.  **Automated Test Parity:** The existing test suite will be run against the legacy sync routes and the new async routes by manipulating the feature toggles during CI/CD. 100% parity is required.
3.  **Formal Sign-off:** The Evidence Collector agent (and human QA) must sign off on the regression test results before the feature toggles are flipped to active in the production environment.

## 6. Ecosystem Review Board Toggle Criteria

This Epic represents a major architectural shift requiring oversight from the Ecosystem Review Board. However, to restore development velocity, the board must be explicitly deactivated once the architectural foundation is secured and standard implementation begins.

**Trigger for Deactivation:**
The `./scripts/toggle_ecosystem_board.sh` script MUST be executed to toggle the extra rules OFF immediately after the following criteria are met:
1.  The Dual-Engine initialization strategy is successfully merged into `main` and deployed to staging.
2.  The LLM Kill Switch isolation (as defined in Section 4.2) is verified and tested against a simulated `asyncpg` pool crash.
3.  The first set of non-critical read routes has been successfully migrated, shadow-tested, and activated in staging with no performance degradation.
4.  The Evidence Collector provides formal sign-off on the foundational database migration architecture.

Once toggled off, the project will transition from Phase Gate architectural planning into standard sprint coding velocity.
