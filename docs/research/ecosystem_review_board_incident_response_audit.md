# Incident Response & Security Audit Findings (Phase 0)

## Overview
This audit reviews the `server/` directory, middleware, and logging configurations for incident response readiness and data leak prevention within the `agency-os` template baseline.

## Findings: Gaps Requiring Phase 1 Fixes

### 1. Kill Switch Implementation & Integration
- **Fail-Open Posture:** In `server/services/orchestrator_service.py`, the kill switch is imported inside a `try/except` block. If the import fails, `kill_switch` is set to `None`, and DAG execution bypasses the security check entirely instead of failing closed.
- **Incomplete Integration:** The kill switch logic is only present in `DAGOrchestrator`. It is completely missing from downstream workers and execution environments (`queue_manager.py`, `execution_engine.py`). If a rogue process is already dispatched or running in the queue, activating the kill switch will not halt the underlying tasks.

### 2. Logging Configuration & PII Leaks
- **Unstructured Logging:** `server/main.py` utilizes basic `logging.basicConfig(level=logging.INFO)` outputting plain text. This complicates automated log ingestion (e.g., Datadog, Splunk) and makes incident response searches unreliable. A structured JSON logger must be implemented.
- **Fragile PII Redaction:** The `redact_pii` function in `server/main.py` relies on rudimentary regex patterns to mask sensitive data (Emails, SSNs, Bearer tokens). This approach is prone to bypassing and false negatives, potentially leaking API keys, custom auth headers, or uniquely formatted sensitive data into validation error logs.
- **Audit Middleware Error Handling:** `server/middleware_audit.py` captures basic request paths and methods. However, if an audit write fails, it uses `print(f"Failed to log audit event: {e}")` instead of standard logging, and worse, fails open, allowing the action to proceed without an audit trail.

### 3. Middleware Security Implications
- **Duplicated/Out-of-Sync Auth Parsing:** `AuditMiddleware` redundantly decodes JWTs directly instead of relying on the context established by the primary authentication layer. This creates a brittle dependency; if token structures change, the audit log breaks silently or causes errors.
- **Middleware Execution Order:** `secure_tenant_and_headers_middleware` uses `@app.middleware("http")`, which can cause inconsistent execution order relative to the `AuditMiddleware` added via `app.add_middleware()`. This can lead to unauthenticated or malformed requests executing audit logic prematurely.

## Recommendations for Phase 1
1. **Enforce Fail-Closed Kill Switch:** Remove the `try/except` import in the orchestrator and implement a hard dependency on the kill switch. Extend the kill switch checks into `queue_manager.py` and `execution_engine.py` for comprehensive halts.
2. **Implement Structured JSON Logging:** Replace `basicConfig` with a robust logging formatter (e.g., `python-json-logger`) to ensure logs are machine-readable and easily searchable during an incident.
3. **Robust PII Masking:** Adopt a dedicated PII masking library or integrate redaction deeper at the logger/formatter level rather than relying on regex string replacement of validation payloads.
4. **Fix Audit Middleware:** Ensure `AuditMiddleware` fails closed (or alerts robustly) on log failure, and refactor it to use standardized authentication context rather than performing isolated JWT decoding.
