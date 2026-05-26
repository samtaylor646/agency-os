# Evidence Suite: Fix Custom Agent 500 Error

## Bug Verification
- **Issue**: API request to `POST /api/v1/custom_agents` returns HTTP 500 Internal Server Error.
- **Cause**: The `generate_agent_markdown` function in `server/routers/custom_agents.py` referenced `agent_data.goal` and `agent_data.guardrails`. These attributes do not exist in the `CustomAgentCreate` schema, causing an `AttributeError` inside the try/except block, raising the HTTP 500 exception.

## Fix Verification
- `server/routers/custom_agents.py` was successfully patched.
- `agent_data.goal` and `agent_data.guardrails` references were removed and replaced with safe fallbacks (`""`).
- Docker container `agency-os-server-1` was restarted to apply the changes.

## Conclusion
The backend now correctly generates the markdown string without throwing an AttributeError.
