# Epic 8: Async Database Refactor - Technical Design Specification

## 1. Overview and Purpose

This document outlines the technical architecture and migration strategy for transitioning the AgencyOS database layer from synchronous operations to asynchronous operations using `asyncpg` and SQLAlchemy's async extensions. The primary goal is to unblock horizontal scalability by eliminating event loop blocking without introducing regressions, specifically addressing the technical pitfalls encountered in previous refactoring attempts.

## 2. Ecosystem Review Board Alignment

In accordance with the `.clinerules` mandate for major platform shifts, this Epic qualifies as a Phase Gate transition touching core infrastructure. The design adheres to the following constraints:

*   **Infrastructure Maintainer (Server Load):** The Dual-Engine strategy ensures database connection limits are respected across both sync and async pools during the transition.
*   **Incident Response Commander (Kill Switches):** A strict feature-toggling mechanism is required at the route level to immediately revert to synchronous execution if latency or error thresholds are breached.
*   **Agentic Identity Trust & Finance Analyst:** No changes to existing authorization, data integrity, or tenant isolation models will occur. The underlying data schema remains untouched.

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

### 4.2. Connection Pooling and Starvation

**The Problem:** `asyncpg` can aggressively open connections under high concurrent load. In the previous failure, the connection pool was exhausted because the application spawned thousands of coroutines waiting for a database connection, leading to deadlocks and timeouts.

**The Solution:**
*   **Strict Pool Sizing:** The async engine must be configured with a strict `pool_size` and `max_overflow`.
*   **`pool_timeout` Enforcement:** A realistic `pool_timeout` (e.g., 5-10 seconds) must be set. If a connection cannot be acquired, the application should fail fast (returning a 503 Service Unavailable) rather than queuing indefinitely and consuming memory.
*   **PgBouncer / Connection Multiplexer:** Ensure the infrastructure utilizes a connection pooler like PgBouncer in front of the database to handle the high volume of short-lived async connections efficiently.

### 4.3. Transaction Management (ACID)

**The Problem:** Unintended side effects occurred when async sessions were not explicitly committed or rolled back when exceptions were raised.

**The Solution:**
*   The `get_async_db` dependency must yield the session within a `try...except...finally` block, ensuring `await session.rollback()` is explicitly called on any exception, and `await session.close()` is guaranteed in the `finally` block.

## 5. Testing and QA Gate Strategy

To pass the rigorous QA Gate, we will implement the following:

1.  **Dual-Read Shadowing (Safe Mode):** For high-risk read routes, we will implement a "shadow mode." The request will execute synchronously (returning the result to the user), but spawn an async background task to execute the identical query via `asyncpg`. The results of both will be hashed and compared. Mismatches will be logged as critical alerts without impacting the user.
2.  **Automated Test Parity:** The existing test suite will be run against the legacy sync routes and the new async routes by manipulating the feature toggles during CI/CD. 100% parity is required.
3.  **Formal Sign-off:** The Evidence Collector agent (and human QA) must sign off on the regression test results before the feature toggles are flipped to active in the production environment.
