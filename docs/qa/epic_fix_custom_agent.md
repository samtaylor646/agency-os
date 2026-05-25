# Epic: Fix Custom Agent Wizard Error

## Plan & Roles
1. **Agents Orchestrator**: Manage the Epic, ensure branches are created, roles are assigned, and handoff is performed.
2. **Frontend Developer**: Fix the `CustomAgentCreator.jsx` to pass the correct `Authorization` and `X-Tenant-ID` headers. (Already completed).
3. **Evidence Collector**: Verify the UI properly constructs the API request with authentication context. Verify curl fails without auth and succeeds with auth.

## Root Cause
The `POST /api/v1/custom_agents` route requires `dependencies.get_api_or_user_tenant_context` which enforces user authentication (`Authorization: Bearer <token>`) and workspace isolation (`X-Tenant-ID: <id>`). The `CustomAgentCreator.jsx` was making an unauthenticated `fetch` request, leading to an `HTTP 401/400` error and displaying "Failed to create custom agent".

## Resolution
Added header injection logic in `CustomAgentCreator.jsx` utilizing `localStorage.getItem('agency_os_token')` and the React context `useWorkspace`.

