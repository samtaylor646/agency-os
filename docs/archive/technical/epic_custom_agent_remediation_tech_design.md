# Technical Design: Custom Agent Remediation Epic

## 1. Overview
This technical specification outlines the architectural changes required to resolve critical technical debt and security vulnerabilities in the Custom Agent creation lifecycle, as specified in `docs/core/prd_epic_custom_agent_remediation.md`.

## 2. Component Design & Changes

### 2.1 Multi-Tenant Enforcement (`server/dependencies.py`)
**Problem:** The system falls back to `SUPER_ADMIN` or tenant `1` when `X-Tenant-ID` is missing, posing a severe risk of accidental cross-tenant data bleed.
**Solution:**
- Modify `get_current_workspace()` and tenant dependency injection to strictly require `X-Tenant-ID`.
- Raise `HTTPException(400, "Missing X-Tenant-ID")` if the header is absent.
- Ensure all custom agent database queries apply the tenant ID filter synchronously.

### 2.2 Schema Strictness (`server/schemas.py`)
**Problem:** `CustomAgentCreate` accepts legacy flat schemas (`goal`, `guardrails`), causing DB/File mismatches.
**Solution:**
- Redefine `CustomAgentCreate` using Pydantic V2 to enforce a strict nested structure:
  ```python
  class CustomAgentCreate(BaseModel):
      name: str
      system_rules: SystemRules
      
      class SystemRules(BaseModel):
          mission: str
          rules: list[str]
  ```
- Use Pydantic's `model_config = {"extra": "forbid"}` to explicitly reject payloads with legacy fields.

### 2.3 Atomic Transactions (`server/routers/custom_agents.py`)
**Problem:** Writing the agent markdown file and inserting the DB record are decoupled. A file write failure leaves an orphaned DB record.
**Solution:**
- Implement the Unit of Work (UoW) pattern within the endpoint:
  1. `session.add(agent_record)`
  2. `session.flush()` (gets the DB ID without committing)
  3. Attempt file system write (`agent_config_service.write_agent_file(agent)`)
  4. If file write raises `IOError`, execute `session.rollback()` and raise `500`.
  5. If file write succeeds, execute `session.commit()`.

### 2.4 PII Leakage in Exception Handler (`server/main.py`)
**Problem:** `RequestValidationError` handlers echo back the raw request body, potentially leaking PII if the user entered sensitive data into an invalid payload.
**Solution:**
- Override FastAPI's default `validation_exception_handler`.
- Log the validation error details but strip `exc.body` from the JSONResponse returned to the client unless a `DEBUG_VALIDATION` environment variable is explicitly set to `True`.

## 3. Impact Assessment & Dependencies
- **Frontend Dependencies:** The UI (`client/src/CustomAgentCreator.jsx`) MUST be updated concurrently to pass `X-Tenant-ID` strictly and wrap legacy states into the nested schema format. Without this, the frontend will break immediately.
- **Circular Dependencies Check:** Verified against existing architecture. The schema and router changes are isolated to the `custom_agents` domain and do not introduce loops with `pipelines` or `semantic_memory`.

## 4. Rollback Strategy
If atomic transactions fail unexpectedly in production, the rollback involves reverting `server/routers/custom_agents.py` to the decoupled DB/File writes while retaining the strict schema and tenant enforcement.
