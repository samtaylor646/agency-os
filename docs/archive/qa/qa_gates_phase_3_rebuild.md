# Phase 3 Rebuild: Strict QA Gates

## 1. Overview

This document defines the strict QA gates, specific Pytest fixtures, integration test scenarios, and compliance checks required before Epics A and B of the Phase 3 Rebuild can be merged into `main`. These gates ensure that the DAG orchestrator is resilient and that custom agent storage is scalable, transactional, and tenant-isolated.

## 2. General Compliance Checks

Before any merge to `main`, the following automated and process checks must pass:
*   **Database Migrations:** All schema changes (e.g., `workflow_executions`) must include `up` and `down` migration scripts, verified for rollback capability.
*   **Test Pass Rate:** 100% pass rate for the complete Pytest integration and unit test suites.
*   **Code Coverage:** Minimum of 85% line coverage for all modified services (e.g., `central_runner.py`, `routers/custom_agents.py`, `services/agent_config_service.py`).
*   **Static Analysis:** Linting (flake8/black) and type checking (mypy) must report zero errors.

## 3. Epic A: Orchestration Hardening & Resilience

### 3.1. Required Pytest Fixtures

The following fixtures must be defined in `conftest.py` or the specific test module to support DAG testing:
*   `mock_db_session`: Provides a database session rolled back after each test to ensure transactional isolation.
*   `mock_workflow_execution`: Factory fixture to seed the `workflow_executions` table with specific states (`PENDING`, `RUNNING`, `PAUSED`, `PARTIAL_FAILURE`).
*   `mock_llm_runtime`: Mocks the external LLM or agent dispatcher to deterministically simulate successes, timeouts, and specific API exceptions.
*   `mock_dag_context`: Generates valid and invalid DAG context payloads for Pydantic schema validation tests.

### 3.2. Integration Test Scenarios

The following automated integration tests must be written and pass:

1.  **DAG Partial Failures & Retries**
    *   **Scenario:** A node within the DAG fails due to a transient error (simulated via `mock_llm_runtime`).
    *   **Assertion:** Verify the orchestrator uses exponential backoff (e.g., via `tenacity`) to retry the node up to the maximum configured attempts.
    *   **Scenario:** A node fails permanently after exceeding max retries.
    *   **Assertion:** Verify the specific node is marked as failed, the workflow status transitions to `PARTIAL_FAILURE` (or fails gracefully), and the orchestrator process does not crash.
2.  **Workflow Pause & Resume (State Persistence)**
    *   **Scenario:** A workflow is interrupted mid-execution (simulating a crash or pause command).
    *   **Assertion:** Verify the `completed_nodes` array and `execution_context` JSONB are accurately persisted to the database.
    *   **Scenario:** The orchestrator restarts processing the interrupted workflow.
    *   **Assertion:** Verify execution resumes exactly from the last successful node without re-running completed nodes.
3.  **Strict Context Validation**
    *   **Scenario:** An invalid payload (missing required fields) is passed to a node's input.
    *   **Assertion:** Verify Pydantic raises a validation error immediately and the node halts cleanly rather than failing downstream.
    *   **Scenario:** End-to-end data flow between Node A and Node B.
    *   **Assertion:** Verify Node A's output correctly maps and validates against Node B's input schema.

## 4. Epic B: Custom Agent Storage & Lifecycle Management

### 4.1. Required Pytest Fixtures

*   `mock_s3_bucket`: Utilizes the `moto` library to provide a mocked AWS S3 environment.
*   `mock_local_filesystem`: Intercepts file I/O to isolate local disk operations during fallback testing.
*   `mock_tenant_id`: Generates isolated, unique UUIDs for multi-tenant data isolation testing.
*   `mock_agent_update_payload`: Factory fixture providing valid and invalid `CustomAgentUpdate` Pydantic models.

### 4.2. Integration Test Scenarios

1.  **S3 Mocking & Storage Abstraction Layer**
    *   **Scenario:** Create a new custom agent with S3 configured.
    *   **Assertion:** Verify metadata is stored in the DB and the markdown file is created at `s3://<mock-bucket>/tenants/{tenant_id}/custom_agents/{agent_id}.md`.
    *   **Scenario:** Create an agent with S3 disabled (fallback mode).
    *   **Assertion:** Verify the markdown file is created on the local disk at `agents/custom/{tenant_id}/{agent_id}.md`.
2.  **Storage Rollback & Transactional Integrity**
    *   **Scenario (Write Failure):** Attempt to update an agent, but simulate a failure during the S3/File write operation (e.g., raise `botocore.exceptions.ClientError`).
    *   **Assertion:** Verify the database transaction is rolled back, and the agent's DB record remains in its previous state.
    *   **Scenario (DB Failure):** Attempt to update an agent, but simulate a DB constraint violation.
    *   **Assertion:** Verify the S3/File is not written/overwritten.
    *   **Scenario (Delete Failure):** Attempt to delete an agent, but simulate an S3 deletion failure.
    *   **Assertion:** Verify the database delete transaction is rolled back.
3.  **Tenant Data Isolation**
    *   **Scenario:** A user attempts to update/delete an agent belonging to a different `tenant_id`.
    *   **Assertion:** Verify a `403 Forbidden` or `404 Not Found` response is returned. The DB query must include `tenant_id` in the `WHERE` clause.
    *   **Scenario:** Directory structure audit.
    *   **Assertion:** Verify that storage paths strictly encapsulate files within their respective `{tenant_id}` namespace.

## 5. Sign-off Authorization

Before merging the Phase 3 Rebuild branch, this document must be reviewed and signed off.

- [ ] **Evidence Collector (QA) Sign-off:** (Name/Date)
- [ ] **Automated Test Report URL:** (Insert link to passing CI/CD run)
