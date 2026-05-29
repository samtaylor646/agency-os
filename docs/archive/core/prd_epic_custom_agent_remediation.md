# Product Requirements Document (PRD): Custom Agent Remediation Epic

## 1. Executive Summary
This epic addresses critical technical debt, security vulnerabilities, and data integrity issues identified during the Custom Agent architectural review. The primary focus is to harden the existing Custom Agent creation flow to ensure strict multi-tenant isolation, prevent PII leaks in logging, enforce structural schema integrity, and eliminate hardcoded configurations.

## 2. Goals & Objectives
- **Security First:** Eliminate hardcoded tenant fallbacks to prevent accidental cross-tenant data exposure.
- **Privacy Compliance:** Ensure PII is not leaked through validation exceptions or global error handlers.
- **Data Integrity:** Enforce strict, nested schema structures for Custom Agent payloads (eliminating legacy flat fields) and guarantee transaction safety (DB and File synchronization).
- **Maintainability:** Decouple environment variables from hardcoded port values for flexible cloud deployments.

## 3. Scope of Work

### Phase 1: Security Hotfixes (P0 - Immediate)
- **Strict Tenant Enforcement:** Remove `|| '1'` fallback logic on the frontend (`client/src/CustomAgentCreator.jsx`) and `SUPER_ADMIN` tenant `1` fallbacks in the backend (`server/dependencies.py`). API must fail-fast without a valid `X-Tenant-ID`.
- **PII Leak Remediation:** Redesign the `validation_exception_handler` in `server/main.py` to mask request body content from logs and client responses. Implement a log redaction utility for compliance.

### Phase 2: Data Integrity & Schema Mapping (P1 - This Sprint)
- **Strict Schema Enforcement:** Backend (`server/schemas.py`) must reject legacy flattened payloads and require strict nested structures (e.g., `system_rules.mission`).
- **Frontend Payload Adapter:** Intercept legacy `goal`/`guardrails` state from the UI and map to the new nested schema before API transmission.
- **Atomic Transactions:** Backend endpoints for custom agent creation must guarantee file system (markdown write) and database commit sync, rolling back on failure.

### Phase 3: Maintainability & Policy (P2 - Next Sprint)
- **Dynamic Configuration:** Replace hardcoded `localhost:8001` with `VITE_API_URL` environment variables in Vite and Docker configs.
- **Data Governance:** Implement an Environment Data Segregation Policy and a 30-day Log Retention/Purge Policy to comply with GDPR.

## 4. Non-Goals
- Adding new capabilities or form fields to the Custom Agent Creator UI.
- Redesigning the agent reasoning engines.
- Refactoring endpoints unrelated to Custom Agent creation and multi-tenant security.

## 5. Success Metrics
- Zero cross-tenant data leaks (verified by E2E tenant boundary tests).
- 100% of custom agent creation requests enforce strict nested schema parsing without server errors.
- PII is provably absent from global error validation logs.
- Successful rollback tests on atomic file/DB write failures.
