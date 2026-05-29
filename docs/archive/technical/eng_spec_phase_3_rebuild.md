# Engineering Specification: Phase 3 Rebuild

## 1. Overview
This technical specification outlines the implementation details for the Phase 3 Rebuild of AgencyOS. Based on the Phase 3 Reassessment Report and the PRD, this rebuild addresses critical technical debt by focusing on DAG orchestrator resilience, state persistence, and a scalable, multi-tenant backend for Custom Agents.

## 2. Database Schema Changes: State Checkpointing

To transition the DAG orchestrator (`central_runner.py`) from an in-memory mock to a resilient runtime, we must persist workflow execution state. This allows workflows to resume from the last successful node in the event of a system crash.

### New Table: `workflow_executions`
This table will track the state of a DAG execution at a granular level.

*   `id` (UUID, Primary Key)
*   `tenant_id` (UUID, Foreign Key to `tenants`, Indexed)
*   `pipeline_id` (UUID, Foreign Key to `pipelines`)
*   `status` (Enum: `PENDING`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `PARTIAL_FAILURE`)
*   `completed_nodes` (JSONB, array of strings representing successfully completed node IDs)
*   `failed_nodes` (JSONB, array of strings representing failed node IDs)
*   `execution_context` (JSONB, stores the inputs, outputs, and intermediate state passed between nodes)
*   `retry_counts` (JSONB, tracks the number of retry attempts per node)
*   `created_at` (Timestamp, default `now()`)
*   `updated_at` (Timestamp, updated on state change)

## 3. Storage Migration Architecture: Custom Agents

Currently, custom agents are saved to a hardcoded flat directory (`agents/custom/`), which breaks multi-tenancy and distributed deployments (Docker/K8s).

### Architecture Plan: Storage Abstraction Layer

We will implement a Storage Abstraction Layer to decouple the application from the underlying storage mechanism. 

**Primary Storage Strategy: Cloud Object Storage (S3)**
*   **Database:** The `custom_agents` PostgreSQL table will store metadata (Name, Status, DB IDs, JSON configurations).
*   **Storage:** The generated markdown persona files will be stored in an S3-compatible cloud bucket.
*   **Path Structure:** `s3://<bucket-name>/tenants/{tenant_id}/custom_agents/{agent_id}.md`

**Fallback / Local Development Strategy: Tenant-Isolated Filesystem**
*   When running locally without S3 credentials, the storage layer will fall back to local disk.
*   **Path Structure:** `agents/custom/{tenant_id}/{agent_id}.md`

This architecture ensures strict physical isolation of tenant data while supporting horizontal scaling.

## 4. Custom Agent CRUD Operations & Endpoints

To fulfill the missing lifecycle management capabilities, we will implement complete CRUD for custom agents in `server/routers/custom_agents.py`.

### 4.1. Decoupling Markdown Generation
Before adding new endpoints, the markdown generation logic must be decoupled to improve testability.
*   Create a new module: `server/services/agent_config_service.py`
*   Move `generate_agent_markdown()` and storage interaction (S3/Filesystem) into this service.

### 4.2. New Endpoints

#### Update Custom Agent
*   **Endpoint:** `PUT /api/custom-agents/{agent_id}`
*   **Payload Validation:** Strict validation using a `CustomAgentUpdate` Pydantic model.
*   **Logic:**
    1.  Verify the `agent_id` belongs to the requesting `tenant_id`.
    2.  Update the metadata and JSON configuration in the database within a transaction.
    3.  Generate the updated markdown payload via `AgentConfigService`.
    4.  Overwrite the markdown file in storage (S3/Filesystem).
    5.  **Transactional Integrity:** If the storage write operation fails, the database transaction MUST be rolled back.

#### Delete Custom Agent
*   **Endpoint:** `DELETE /api/custom-agents/{agent_id}`
*   **Logic:**
    1.  Verify the `agent_id` belongs to the requesting `tenant_id`.
    2.  Attempt to delete the associated markdown file from storage.
    3.  Delete (or soft delete) the custom agent record from the database.
    4.  **Transactional Integrity:** If the storage deletion fails, the database transaction MUST be rolled back.

## 5. DAG Resiliency and Validation

### 5.1. Real Runtime Integration & Resilience
*   Replace the mock `execute_node` function in `central_runner.py` with actual LLM or agent dispatcher logic.
*   **Retry Mechanism:** Implement automatic retries for transient node failures using exponential backoff (e.g., using the `tenacity` library in Python). A single node failure must not crash the entire orchestrator ungracefully.

### 5.2. Strict Context Schema Validation
*   All data passed between nodes (DAG Context) must be validated to prevent unstructured data errors.
*   Implement standard Pydantic models for standard node inputs and outputs. The orchestrator must validate the output of Node A before passing it as input to Node B.