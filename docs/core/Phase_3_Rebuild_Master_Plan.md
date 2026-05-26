# Phase 3 Rebuild: Master Plan

## 1. Executive Summary

This document serves as the unified source of truth for the Phase 3 Rebuild of AgencyOS, consolidating requirements, engineering specifications, devops strategies, QA gates, and sprint planning. Based on the findings in the Phase 3 Reassessment Report, critical technical debt, missing test coverage, and architectural vulnerabilities must be addressed before proceeding with new feature development. This rebuild focuses on system scalability, reliability, and data security by establishing a production-ready DAG orchestrator and completing the foundational Custom Agent Creator backend.

---

## 2. Goals & Objectives

1.  **System Stability & Reliability:** Transform the current proof-of-concept orchestration into a resilient, production-ready system capable of handling failures gracefully and persisting state. Implement resilient, state-persisting DAG orchestration.
2.  **Scalability & Distributed Readiness:** Decouple state from the local filesystem to support distributed deployments (e.g., Docker, Kubernetes) and ensure multi-tenant data isolation. Migrate custom agent storage to a multi-tenant, cloud-ready S3 architecture with local fallback.
3.  **Feature Completeness:** Deliver complete lifecycle management (CRUD) for custom agents, including Update and Delete API endpoints.
4.  **Data Integrity & Security:** Enforce strict schema validation, Pydantic context validation, and transactional database rollbacks across system operations.

---

## 3. Product Requirements (Epics)

### Epic A: Orchestration Hardening & Resilience
**Goal:** Transform the DAG orchestrator from an in-memory mock to a production-ready, resilient runtime.

*   **Story A1: Workflow State Persistence** - Workflow executions must save their state to a database so progress is not lost during interruptions, and workflows can be paused/resumed.
*   **Story A2: Real LLM Runtime Integration** - The orchestrator must execute real LLM tasks rather than mock functions so that workflows produce actual value.
*   **Story A3: Resilience & Partial Failure Handling** - Handle node failures gracefully with retries and exponential backoff so that transient errors do not fail the entire workflow.
*   **Story A4: Strict Context Schema Validation** - Data passed between workflow nodes must be strictly validated to prevent errors caused by unstructured data or missing fields.

### Epic B: Custom Agent Storage & Lifecycle Management
**Goal:** Secure agent configurations and complete the foundational agent management API.

*   **Story B1: Scalable Agent Storage & Isolation** - Custom agent configurations must be stored in a scalable and isolated manner (S3 or DB) so the system can be deployed in distributed environments.
*   **Story B2: Complete Agent Lifecycle API (Update & Delete)** - Users must be able to update existing custom agents and delete those they no longer need.
*   **Story B3: Transactional Integrity on Failure** - Database changes must roll back if the associated storage write fails so that the database and file storage remain in sync.
*   **Story B4: Decoupled Markdown Generation** - Markdown generation logic must be decoupled from the router layer for modularity, testability, and maintainability.

---

## 4. Engineering & Architecture Specification

### 4.1. Database Schema Changes: State Checkpointing
To transition the DAG orchestrator to a resilient runtime, workflow execution state must be persisted.
*   **New Table: `workflow_executions`**: Tracks the state of a DAG execution at a granular level. Fields include: `id` (UUID), `tenant_id` (UUID), `pipeline_id` (UUID), `status` (Enum), `completed_nodes` (JSONB), `failed_nodes` (JSONB), `execution_context` (JSONB), `retry_counts` (JSONB), `created_at`, `updated_at`.

### 4.2. Storage Migration Architecture: Custom Agents
A Storage Abstraction Layer will be implemented to decouple the application from the underlying storage mechanism.
*   **Primary Storage (S3):** Metadata stored in `custom_agents` PostgreSQL table. Markdown files stored in S3 (`s3://<bucket-name>/tenants/{tenant_id}/custom_agents/{agent_id}.md`).
*   **Fallback Storage (Local):** Local development uses strict tenant isolation (`agents/custom/{tenant_id}/{agent_id}.md`).

### 4.3. Custom Agent CRUD Operations & Endpoints
*   **Decoupled Service:** Create `server/services/agent_config_service.py` to handle markdown generation and storage interaction.
*   **Update Endpoint (`PUT /api/custom-agents/{agent_id}`):** Validates payload, updates DB metadata, generates new markdown, overwrites storage file. Requires transactional rollback on storage failure.
*   **Delete Endpoint (`DELETE /api/custom-agents/{agent_id}`):** Deletes file from storage and database record. Requires transactional rollback on storage failure.

### 4.4. DAG Resiliency and Validation
*   Replace mock functions with actual LLM/agent dispatchers. Implement automatic retries for transient node failures using exponential backoff (e.g., `tenacity`).
*   Validate all data passed between nodes using standard Pydantic models.

---

## 5. DevOps Deployment Specification

### 5.1. Infrastructure Requirements
*   **PostgreSQL:** Must accommodate the new `workflow_executions` table (JSONB). Use init-containers for migrations.
*   **S3-Compatible Storage:** Provision a dedicated bucket (e.g., `agency-os-agent-storage-prod`) with IAM roles granting `s3:PutObject`, `s3:GetObject`, and `s3:DeleteObject` scoped strictly to `tenants/*`.

### 5.2. Environment Configuration
Required variables: `STORAGE_BACKEND`, `S3_BUCKET_NAME`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `LOCAL_STORAGE_PATH`, `DATABASE_URL`.

### 5.3. Implementations
*   **Docker Compose:** Support fallback local environment using volume mounts for `LOCAL_STORAGE_PATH` and provide an `.env.example` for testing S3 logic locally.
*   **Kubernetes (Prod):** Ensure pods are stateless (no PVCs for agent files). Utilize IRSA for IAM permissions, store configuration in ConfigMaps/Secrets, and configure graceful shutdowns (`SIGTERM`) for running DAG nodes to checkpoint state before pod termination.

---

## 6. QA Gates & Compliance

### 6.1. General Compliance Checks
Before any merge to `main`, the following must pass:
*   Database Migrations tested (up and down scripts).
*   100% Pass Rate for complete Pytest integration and unit suites.
*   Minimum of 85% line coverage for all modified services.
*   Zero errors in static analysis (flake8/black, mypy).

### 6.2. Test Scenarios & Fixtures
*   **Required Fixtures:** `mock_db_session`, `mock_workflow_execution`, `mock_llm_runtime`, `mock_dag_context`, `mock_s3_bucket`, `mock_local_filesystem`, `mock_tenant_id`, `mock_agent_update_payload`.
*   **Epic A Integration Tests:** DAG Partial Failures & Retries, Workflow Pause & Resume, Strict Context Validation.
*   **Epic B Integration Tests:** S3 Mocking & Storage Abstraction, Storage Rollback & Transactional Integrity, Tenant Data Isolation (verifying 403/404 responses for cross-tenant access).

---

## 7. Sprint Plan & Execution Matrix

### Epic A: Orchestration Hardening & Resilience
| Task ID | Description | Assigned Agent | Status |
|---|---|---|---|
| A1-1 | Create database migration for `workflow_executions` table | Backend Architect | To Do |
| A1-2 | Implement workflow state saving in `central_runner.py` | Backend Architect | To Do |
| A2-1 | Replace mock `execute_node` with actual logic | Backend Architect | To Do |
| A3-1 | Implement retry mechanism with exponential backoff | Backend Architect | Done |
| A3-2 | Handle disconnected graphs & prevent ungraceful crashes | Backend Architect | Done |
| A4-1 | Implement standard Pydantic models for DAG inputs/outputs | Backend Architect | To Do |
| A4-2 | Enforce strict schema validation between DAG context nodes | Backend Architect | To Do |
| QA-A | Execute all Epic A integration and resilience test scenarios | Evidence Collector | To Do |

### Epic B: Custom Agent Storage & Lifecycle Management
| Task ID | Description | Assigned Agent | Status |
|---|---|---|---|
| B4-1 | Refactor markdown generation into `agent_config_service.py` | Backend Architect | To Do |
| B1-1 | Implement Storage Abstraction Layer (S3 & Local Fallback) | Backend Architect | To Do |
| B1-2 | Ensure strict tenant isolation in storage paths | Backend Architect | To Do |
| B2-1 | Implement `PUT /api/custom-agents/{agent_id}` endpoint | Backend Architect | To Do |
| B2-2 | Implement `DELETE /api/custom-agents/{agent_id}` endpoint | Backend Architect | To Do |
| B3-1 | Implement DB transactional rollbacks on storage failure | Backend Architect | To Do |
| QA-B | Execute all Epic B transactional and isolation test scenarios | Evidence Collector | To Do |

### DevOps & Infrastructure
| Task ID | Description | Assigned Agent | Status |
|---|---|---|---|
| D1-1 | Provision S3 bucket and configure IAM Roles/Policies | DevOps Engineer | To Do |
| D1-2 | Update Kubernetes configs (ConfigMaps/Secrets) with env vars | DevOps Engineer | To Do |
| D1-3 | Update `docker-compose.yml` for local testing with fallback | DevOps Engineer | To Do |
| D1-4 | Configure CI/CD pipeline for `local` and `s3` integration tests | DevOps Engineer | To Do |

### Dev ↔ QA Loop Execution Workflow
1.  **Implementation:** Backend Architect & DevOps Engineer complete tasks in a dedicated Epic branch.
2.  **Automated Testing:** Developers write Pytest fixtures and hit 85% coverage minimum.
3.  **QA Handoff:** Once CI passes, Evidence Collector takes control.
4.  **Validation:** Evidence Collector verifies all scenarios against the strict QA Gates.
5.  **Sign-off:** Documented sign-off in the QA gates before the branch merges into `main`.