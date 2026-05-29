# Epic Plan: Technical Debt & Security Remediation (Custom Agent Creation)

## 1. Objective
Address critical security vulnerabilities, data integrity issues, and architectural flaws outlined in `docs/qa/architectural-review.md`.

## 2. Phase & Priority Breakdown

### Phase 1: Security Hotfixes (P0 - Immediate)
*   **Issue 1: Hardcoded Tenant ID Fallback**
    *   *Frontend:* Update `client/src/CustomAgentCreator.jsx` to completely remove `|| '1'`. Abort the API call and show an error if `activeWorkspace` is missing.
    *   *Backend:* Modify `server/dependencies.py` to enforce `X-Tenant-ID` presence. Remove the `SUPER_ADMIN` fallback to tenant `1` and validate cross-tenant access explicitly.
*   **Issue 3: Global Exception Handler PII Leak**
    *   *Backend:* Rewrite `validation_exception_handler` in `server/main.py` to remove request body echoing from logs and client responses. Introduce a `DEBUG_VALIDATION` flag.
    *   *Compliance:* Implement a log redaction utility to mask API keys and PII even when debugging is enabled.

### Phase 2: Data Integrity & Schema Mapping (P1 - This Sprint)
*   **Issue 2 & 5: Schema Duality & Fallbacks**
    *   *Backend:* Refactor `CustomAgentCreate` schema in `server/schemas.py` to strictly enforce a nested structure. Delete all flattened fields. Reject any payload containing legacy `goal`/`guardrails` attributes.
    *   *Frontend:* Implement a payload adapter in `client/src/CustomAgentCreator.jsx` to intercept and map legacy `goal`/`guardrails` state data into `system_rules.mission` and `system_rules.rules` *before* transmission.
*   **Edge Cases: Transaction Safety**
    *   *Backend:* Refactor the endpoint in `server/routers/custom_agents.py` (or equivalent endpoint) to perform DB flush -> write markdown file -> DB commit, wrapping in a try/except to rollback/delete on failure.

### Phase 3: Maintainability & Policy (P2 - Next Sprint)
*   **Issue 4: Hardcoded Port Configuration**
    *   *DevOps:* Update `client/vite.config.js` and `docker-compose.yml` to use `VITE_API_URL` environment variables instead of hardcoded `localhost:8001`.
*   **Compliance Policy Implementation**
    *   *Compliance:* Draft an Environment Data Segregation Policy and a Log Retention/Purge Policy (30-day TTL) to satisfy GDPR storage limitation principles.

## 3. Role Assignments
1. **Frontend Developer (`frontend-developer`):** Execute Phase 1 & 2 UI tasks (Fail-fast tenant validation, legacy schema mapping).
2. **Backend Architect (`backend-architect`):** Execute Phase 1 & 2 backend tasks (Tenant enforcement, atomic DB transactions, schema strictness).
3. **Legal Compliance Checker (`support-legal-compliance-checker`):** Audit the `server/main.py` fix, implement log masking, and draft GDPR retention policies.
4. **DevOps Engineer (`engineering-devops-engineer`):** Execute Phase 3 Vite/Docker variable decoupling.
5. **Evidence Collector (`testing-evidence-collector`):** Write automated tests for tenant boundaries and execute the Strict QA Gate before merging.
6. **Agents Orchestrator (`agents-orchestrator`):** Create the `epic/architectural-remediation` git branch, route tasks, and oversee validation.
