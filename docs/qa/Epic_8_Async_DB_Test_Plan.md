# Epic 8: Async Database Refactor - QA Test Plan

## 1. Overview
This document defines the formal Quality Assurance Test Plan for the Epic 8 Async Database Refactor. Given the previous failure due to SQLAlchemy architectural nuances and connection starvation, this plan enforces strict testing strategies and human-in-the-loop (HITL) validations.

## 2. Automated E2E Testing Strategy for `.scalars()` Errors

The core of the previous failure was improper use of SQLAlchemy 2.0 async mode, specifically chaining synchronous methods on async results and lazy-loading relationships, resulting in `MissingGreenlet` errors.

To catch these issues automatically, the following E2E strategy is required:

### 2.1. Strict Eager-Loading Validation Tests
Every migrated endpoint MUST have E2E tests that explicitly attempt to access all nested relationships returned by the endpoint.
*   **Test Design:** Create nested resource payloads, fetch them via the API, and assert that the entire nested graph is correctly serialized.
*   **Failure Condition:** Any lazy-loading triggered outside the async session will throw a `MissingGreenlet` error, causing the test to fail.
*   **Coverage Rule:** 100% of relationship attributes accessed by the API response models MUST be verified in integration tests under the `FEATURE_TOGGLE_ASYNC_* = TRUE` flag.

### 2.2. Concurrent Load Tests (Catching Pool Starvation)
The previous migration resulted in connection pool exhaustion.
*   **Test Design:** Implement concurrent load tests using `pytest-asyncio` or `locust` that bombard the migrated endpoints with rapid, parallel requests.
*   **Execution Pattern Standard:** Test cases must assert that `asyncpg` properly handles concurrent `await session.execute(stmt); return result.scalars().all()` calls without deadlocking.
*   **Failure Condition:** High latency, `TimeoutError`, or 503 Service Unavailable responses indicating connection pool starvation.

### 2.3. Compliance Parity Shadow Mode Tests
Based on the Legal & Compliance Checker's report ([`docs/qa/Epic_8_Compliance_Signoff.md`](docs/qa/Epic_8_Compliance_Signoff.md)):
*   **Context Isolation:** Tests must fire concurrent requests from multiple distinct tenant IDs to verify that `contextvars` correctly isolates state and no cross-tenant data leakage occurs.
*   **Shadow Mode Logs:** Test the dual-read shadow mode and assert that log outputs do not contain plaintext PII or generate duplicate audit log entries.

## 3. Human-in-the-Loop (HITL) Verification Protocol

Before any route toggle (`FEATURE_TOGGLE_ASYNC_<RESOURCE>`) is permanently enabled in production, the following manual HITL steps must be completed and signed off.

### 3.1. Route Migration Sign-off Checklist
For each migrated route, a QA Engineer must manually verify:
- [ ] **Dual-Engine Stability:** Trigger the route and observe the application logs to confirm both the sync and async engines remain stable.
- [ ] **Data Parity Check:** Manually verify that the response payloads from the async route perfectly match the legacy sync route payloads.
- [ ] **Kill Switch Verification:** Manually toggle the environment variable from `TRUE` to `FALSE` during active execution to confirm the application gracefully falls back to the synchronous engine without requiring a restart.
- [ ] **Error Handling:** Manually inject a database error (e.g., bad payload) and verify that the transaction is rolled back correctly and `session.close()` is confirmed via logs.

### 3.2. Phase Gate Authorization
The "Migrated" status is only granted when:
1. The Automated E2E test suite passes 100% against the target route.
2. The HITL checklist is fully signed off for the target route.
3. The Evidence Collector agent has documented the proof of passage.

