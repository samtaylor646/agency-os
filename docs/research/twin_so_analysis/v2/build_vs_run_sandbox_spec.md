# Engineering Specification: Build vs. Run Sandbox Architecture

## 1. Executive Summary
This specification outlines the backend architecture required to support the "Build vs. Run" paradigm in AgencyOS V2, heavily inspired by the twin.so analysis. The goal is to provide a low-latency, cost-effective, and highly isolated "Sandbox" environment for iterative agent development (Build), completely decoupled from the persistent, high-fidelity production execution environment (Run).

## 2. Architectural Overview
The system introduces a strict bifurcation of execution pathways:
*   **Build Mode (The Sandbox):** An ephemeral, highly mocked, and cost-optimized execution layer. It relies on model degradation, semantic caching, and strict network isolation.
*   **Run Mode (Production):** A persistent, asynchronous execution layer utilizing premium LLM models, full API/DB access, and scalable worker queues.

### 2.1 Core Components
1.  **LLM Routing Proxy:** Intercepts LLM calls to downgrade models in the Sandbox and enforce token limits.
2.  **Semantic Cache Layer:** Redis-based caching mechanism to eliminate redundant LLM calls during iterative prompt tweaking.
3.  **Ephemeral Execution Engine:** Synchronous, low-latency executor for immediate UI feedback.
4.  **Production Worker Queues:** Asynchronous execution engine (Celery/RQ) for long-running, real-world tasks.
5.  **State Manager:** Handles the immutable promotion of agent configurations from Build to Run.

## 3. The "Build" Environment (Sandbox) Specifications

### 3.1 Cost Optimization Controls
*   **Automatic Model Degradation:** All requests routed through the Sandbox are automatically downgraded to cost-effective models (e.g., `gpt-4o` degrades to `gpt-4o-mini`). The LLM Routing Proxy handles this translation transparently.
*   **Semantic Caching:** A Redis semantic cache stores the vector embeddings of recent user prompts. If an iterative test falls within a 95% cosine similarity threshold of a previous prompt, the cached response is served instantly.
*   **Hard Token Caps:** Strict token limits (e.g., max 2000 output tokens) are enforced per Sandbox execution to prevent runaway loops during development.

### 3.2 Security and Isolation
*   **Network-Isolated Execution:** Tool executions that require external access or compute are run within isolated, short-lived Docker containers (or Firecracker microVMs if scaling requires).
*   **Secret Manager Masking:** The Sandbox environment is completely decoupled from production secrets. Tool payloads that require API keys will be injected with dummy values, and the outgoing network requests are intercepted and mocked.
*   **Mock Execution Engine:** The backend provides a mocking framework for standard tool types (e.g., Database Write, External API Call). Instead of executing the tool, the Sandbox returns a simulated success response and logs the intended payload to the "Trace View" overlay.

## 4. The "Run" Environment (Production) Specifications

### 4.1 Execution Fidelity
*   **Premium Model Routing:** The LLM proxy restores the specified premium models (e.g., `gpt-4o`, `claude-3-opus`) for maximum reasoning capability.
*   **Full API/Data Access:** Agents operate with actual production secrets and write privileges, executing tools against live endpoints and databases.

### 4.2 Scalability and Persistence
*   **Asynchronous Worker Queues:** Run executions are offloaded to distributed message queues (e.g., RabbitMQ/Redis + Celery). This supports long-running, multi-step agent pipelines without timing out the client connection.
*   **Persistent State Management:** Execution state, memory, and intermediate tool outputs are persistently logged to the PostgreSQL database, ensuring traceability and resume-ability in case of failure.

## 5. Promotion Flow (State Management)
Moving an agent from Build to Run requires a strict versioning protocol.

1.  **Snapshotting:** When a user initiates a "Promote to Production", the backend generates an immutable JSON snapshot of the agent configuration (System Prompt, Tool Registry, Context linkages).
2.  **Versioning:** The snapshot is assigned a semantic version tag (e.g., `v1.0.0`) and stored in the database.
3.  **Deployment:** The worker queues are updated to reference this immutable configuration ID for all subsequent production executions. Future edits in the Sandbox will not affect this deployed version until explicitly promoted again.

## 6. Implementation Strategy
*   **Phase 1:** Implement the LLM Routing Proxy and Semantic Caching for immediate cost reduction.
*   **Phase 2:** Build the Mock Execution Engine and integrate the Trace View data structures.
*   **Phase 3:** Finalize the Snapshotting and Promotion state management logic.
*   **Phase 4:** Migrate all Run executions to asynchronous queues.