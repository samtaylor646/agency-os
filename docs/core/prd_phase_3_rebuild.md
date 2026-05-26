# Product Requirements Document: Phase 3 Rebuild

## 1. Executive Summary

This PRD outlines the requirements for the Phase 3 Rebuild of AgencyOS. Based on the findings in the Phase 3 Reassessment Report, critical technical debt, missing test coverage, and architectural vulnerabilities must be addressed before proceeding with new feature development. This rebuild focuses on system scalability, reliability, and data security by establishing a production-ready DAG orchestrator and completing the foundational Custom Agent Creator backend.

## 2. Business Goals

1.  **System Stability & Reliability:** Transform the current proof-of-concept orchestration into a resilient, production-ready system capable of handling failures gracefully and persisting state.
2.  **Scalability & Distributed Readiness:** Decouple state from the local filesystem to support distributed deployments (e.g., Docker, Kubernetes) and ensure multi-tenant data isolation.
3.  **Feature Completeness:** Deliver complete lifecycle management (CRUD) for custom agents.
4.  **Data Integrity & Security:** Enforce strict schema validation and transactional integrity across system operations.

## 3. Epic A: Orchestration Hardening & Resilience

**Goal:** Transform the DAG orchestrator from an in-memory mock to a production-ready, resilient runtime.

### User Stories & Acceptance Criteria

**Story A1: Workflow State Persistence**
*As an Operator or System Administrator, I want workflow executions to save their state to a database so that progress is not lost during system interruptions or crashes, and workflows can be paused/resumed.*
*   **Acceptance Criteria:**
    *   DAG execution state is stored in the database.
    *   System crashes during execution do not result in total data loss; the workflow can resume from the last successful node.
    *   Database schema modifications are documented and reviewed.

**Story A2: Real LLM Runtime Integration**
*As an Operator, I want the orchestrator to execute real LLM tasks rather than mock functions so that the workflows produce actual value.*
*   **Acceptance Criteria:**
    *   Mock `execute_node` functions are replaced with production runtime dispatch logic.
    *   Successful invocation of LLMs or agent runtimes is verified via integration tests.

**Story A3: Resilience & Partial Failure Handling**
*As an Operator, I want the system to handle node failures gracefully with retries and exponential backoff so that transient errors do not fail the entire workflow.*
*   **Acceptance Criteria:**
    *   Configurable retry logic with exponential backoff is implemented for node execution.
    *   Failure of a single node within an async block does not ungracefully crash the orchestrator.
    *   DAG partial failure test coverage is implemented and passing.
    *   Disconnected graph scenarios are handled gracefully and tested.

**Story A4: Strict Context Schema Validation**
*As a System Architect, I want the data passed between workflow nodes to be strictly validated so that errors caused by unstructured data or missing fields are prevented.*
*   **Acceptance Criteria:**
    *   Pydantic (or equivalent) schema validation is enforced for inputs and outputs between agents/nodes.
    *   DAG context passing integration tests verify data integrity across nodes end-to-end.

## 4. Epic B: Custom Agent Storage & Lifecycle Management

**Goal:** Secure agent configurations and complete the foundational agent management API.

### User Stories & Acceptance Criteria

**Story B1: Scalable Agent Storage & Isolation**
*As a System Administrator, I want custom agent configurations stored in a scalable and isolated manner so that the system can be deployed in distributed environments without stateful filesystem dependencies.*
*   **Acceptance Criteria:**
    *   Custom agent storage is migrated to PostgreSQL (JSONB/text) or Cloud Storage (e.g., AWS S3).
    *   *Fallback (If filesystem retained temporarily):* Strict physical tenant isolation is implemented (`agents/custom/{tenant_id}/`).
    *   The solution supports containerized (Docker/Kubernetes) deployments without breaking.

**Story B2: Complete Agent Lifecycle API (Update & Delete)**
*As an Agency Owner, I want to be able to update existing custom agents and delete those I no longer need so that I can maintain my workspace effectively.*
*   **Acceptance Criteria:**
    *   Update (`PUT`/`PATCH`) API endpoint is implemented and functional.
    *   Delete (`DELETE`) API endpoint is implemented and functional.
    *   Tests exist for Update/Delete endpoints, specifically ensuring appropriate storage cleanup upon deletion.

**Story B3: Transactional Integrity on Failure**
*As a System Architect, I want database changes to roll back if the associated storage write fails so that the database and file storage remain in sync.*
*   **Acceptance Criteria:**
    *   Database transactions are rolled back if the file/storage write operation fails.
    *   Automated tests verify database rollback during a simulated storage write failure.

**Story B4: Decoupled Markdown Generation**
*As a Developer, I want the markdown generation logic decoupled from the router layer so that the codebase is more modular, testable, and maintainable.*
*   **Acceptance Criteria:**
    *   Markdown generation logic is refactored into a dedicated service module.
    *   Unit tests are added/updated for the new service module independently of the API routers.