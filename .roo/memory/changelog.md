# Changelog

## [2026-05-25] - Epic: Fix Custom Agent Wizard Error
- **Fixed**: Custom Agent Creator UI failed to send `Authorization` and `X-Tenant-ID` headers to the backend, causing 401 Unauthorized errors.
- **Changed**: `client/src/CustomAgentCreator.jsx` to dynamically fetch the token from `localStorage` and `activeWorkspace` from `WorkspaceContext`.
- **Added**: Added `validation_layer.py` per epic instructions.
- **Added**: Added Evidence documentation in `docs/qa/evidence_epic_fix_custom_agent.md`.

## [2026-05-26] - Epic: Technical Debt & Security Remediation (Custom Agent Creation)
- **Fixed**: Removed hardcoded tenant ID fallback in `client/src/CustomAgentCreator.jsx` and `server/dependencies.py` to enforce strict boundaries.
- **Fixed**: Removed request body echoing in global exception handler (`server/main.py`) to prevent PII leaks.
- **Changed**: Refactored `CustomAgentCreate` schema to enforce nested structure and implemented legacy mapping adapter in `client/src/CustomAgentCreator.jsx`.
- **Changed**: Decoupled hardcoded port configurations using `VITE_API_URL` environment variables in `client/vite.config.js` and `docker-compose.yml`.
- **Added**: Drafted GDPR-compliant Environment Data Segregation and Log Retention policies in `docs/operations/gdpr_compliance_policies.md`.
- **Added**: Added strict tenant isolation tests and provided formal QA sign-off in `docs/qa/custom_agent_tenant_isolation_qa_signoff.md`.
