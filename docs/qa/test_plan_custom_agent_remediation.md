# QA Test Plan: Custom Agent Remediation Epic

## 1. Overview
This test plan defines the automated, manual, and Human-in-the-Loop (HITL) testing required before the Custom Agent Remediation Epic can be merged into `main`. The `Strict QA Gate` rule applies.

## 2. Automated Test Requirements (pytest)

### 2.1 Multi-Tenant Boundaries
*   **Test Case 1:** `test_custom_agent_create_missing_tenant` - Send request without `X-Tenant-ID`. Assert HTTP 400.
*   **Test Case 2:** `test_custom_agent_create_cross_tenant_reject` - Authenticate as user in Tenant A, but attempt to create agent for Tenant B. Assert HTTP 403 or 404.

### 2.2 Schema Strictness
*   **Test Case 3:** `test_custom_agent_create_legacy_payload_rejected` - Send payload with legacy `goal` and `guardrails` top-level fields. Assert HTTP 422 Unprocessable Entity.
*   **Test Case 4:** `test_custom_agent_create_nested_payload_accepted` - Send payload matching the new `system_rules` schema. Assert HTTP 201 Created.

### 2.3 Transaction Integrity
*   **Test Case 5:** `test_custom_agent_create_file_failure_rollback` - Mock `agent_config_service.write_agent_file` to throw an IOError. Assert HTTP 500 and verify NO record was added to the database.

### 2.4 PII Leakage
*   **Test Case 6:** `test_validation_error_no_pii_leak` - Send an invalid payload. Assert that the resulting HTTP 422 JSON response body does **not** contain the original invalid data.
*   **Test Case 7:** `test_validation_error_debug_mode` - Enable `DEBUG_VALIDATION`. Send invalid payload. Assert HTTP 422 response *does* contain debug info.

## 3. Frontend & HITL (Human-in-the-Loop) Testing

### 3.1 UI State Adapter Verification
1.  **Manual Tester Action:** Navigate to the Custom Agent Creator UI (`/client/src/CustomAgentCreator.jsx`).
2.  **Action:** Fill out the legacy form fields (Mission, Rules, Name).
3.  **Assertion:** Inspect the outgoing Network request in the browser DevTools. The payload must **not** contain `goal` or `guardrails`. It must strictly be nested under `system_rules`.

### 3.2 Full E2E Flow
1.  **Manual Tester Action:** Create a Custom Agent via the UI.
2.  **Assertion 1:** Verify success toast on the UI.
3.  **Assertion 2:** Check the backend database to ensure the `tenant_id` matches the active workspace.
4.  **Assertion 3:** Check the file system to ensure the markdown file was correctly written to `/agents/specialized/`.

## 4. QA Sign-Off Criteria
- [ ] All 7 automated tests must pass on CI.
- [ ] HITL Network payload inspection confirms frontend adapter is functioning.
- [ ] No regression on existing pipelines relying on custom agents.
