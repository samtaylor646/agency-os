# Sprint Plan: Phase 3 Rebuild

## 1. Executive Summary
This sprint plan executes the Phase 3 Rebuild of AgencyOS, addressing critical technical debt, missing test coverage, and architectural vulnerabilities. The focus is on system scalability, reliability, and data security by establishing a production-ready DAG orchestrator and completing the foundational Custom Agent Creator backend.

## 2. Sprint Goals
1. **System Stability & Reliability:** Implement resilient, state-persisting DAG orchestration.
2. **Scalability:** Migrate custom agent storage to a multi-tenant, cloud-ready S3 architecture with local fallback.
3. **Feature Completeness:** Deliver Update and Delete API endpoints for complete Custom Agent lifecycle management.
4. **Data Integrity:** Enforce transactional DB rollbacks and strict Pydantic context schema validation.

## 3. Epic A: Orchestration Hardening & Resilience

| Task ID | Description | Assigned Agent | Status |
|---|---|---|---|
| A1-1 | Create database migration for `workflow_executions` table to persist DAG state. | Backend Architect | Done |
| A1-2 | Implement workflow state saving (PENDING, RUNNING, PAUSED, COMPLETED, FAILED, PARTIAL_FAILURE) in `central_runner.py`. | Backend Architect | Done |
| A2-1 | Replace mock `execute_node` in `central_runner.py` with actual LLM/agent dispatch logic. | Backend Architect | Done |
| A3-1 | Implement retry mechanism with exponential backoff (e.g., using `tenacity`) for transient node failures. | Backend Architect | Done |
| A3-2 | Handle disconnected graph scenarios and prevent ungraceful orchestrator crashes on single node failures. | Backend Architect | Done |
| A4-1 | Implement standard Pydantic models for DAG node inputs and outputs. | Backend Architect | Done |
| A4-2 | Enforce strict schema validation between nodes in the DAG context. | Backend Architect | Done |
| QA-A | Execute DAG Partial Failures & Retries, Workflow Pause & Resume, and Strict Context Validation test scenarios. | Evidence Collector | Done |

## 4. Epic B: Custom Agent Storage & Lifecycle Management

| Task ID | Description | Assigned Agent | Status |
|---|---|---|---|
| B4-1 | Refactor markdown generation into a dedicated `server/services/agent_config_service.py` module. | Backend Architect | To Do |
| B1-1 | Implement Storage Abstraction Layer supporting both S3 and Local Filesystem fallback. | Backend Architect | To Do |
| B1-2 | Ensure strict tenant isolation in storage paths (`tenants/{tenant_id}/custom_agents/{agent_id}.md`). | Backend Architect | To Do |
| B2-1 | Implement `PUT /api/custom-agents/{agent_id}` endpoint with DB update and markdown regeneration. | Backend Architect | To Do |
| B2-2 | Implement `DELETE /api/custom-agents/{agent_id}` endpoint. | Backend Architect | To Do |
| B3-1 | Implement transactional integrity: rollback DB changes if storage write/delete operations fail. | Backend Architect | To Do |
| QA-B | Execute S3 Mocking, Storage Rollback & Transactional Integrity, and Tenant Data Isolation test scenarios. | Evidence Collector | To Do |

## 5. DevOps & Infrastructure

| Task ID | Description | Assigned Agent | Status |
|---|---|---|---|
| D1-1 | Provision S3 bucket (`agency-os-agent-storage-prod`) and configure IAM Roles/Policies. | DevOps Engineer | To Do |
| D1-2 | Update Kubernetes configs (ConfigMaps/Secrets) with new environment variables (`STORAGE_BACKEND`, `S3_BUCKET_NAME`, etc.). | DevOps Engineer | To Do |
| D1-3 | Update `docker-compose.yml` for local testing with fallback mount and environment variables. | DevOps Engineer | To Do |
| D1-4 | Configure CI/CD pipeline to run integration tests against both `local` and `s3` storage implementations. | DevOps Engineer | To Do |

## 6. Dev ↔ QA Loop Execution

Following the strict Dev-QA Loop for Phase 3:
1. **Implementation:** Backend Architect and DevOps Engineer complete their assigned tasks in a dedicated Epic branch.
2. **Automated Testing:** Developers write Pytest fixtures (`mock_db_session`, `mock_s3_bucket`, etc.) and unit/integration tests meeting 85% coverage minimums.
3. **QA Handoff:** Once CI checks pass (linting, type checking, 100% test pass rate), the Evidence Collector assumes control.
4. **Validation:** Evidence Collector verifies all scenarios defined in `docs/qa/qa_gates_phase_3_rebuild.md`.
5. **Sign-off:** The Evidence Collector documents sign-off in the QA gates document before the branch is merged into `main`.