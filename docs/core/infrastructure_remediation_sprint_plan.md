# Infrastructure Remediation Sprint Plan

## Overview
This sprint plan breaks down the Infrastructure Remediation into actionable, sequential sprints based on the PRD. The focus shifts from backend intelligence to data persistence, then real-time UI updates, and concludes with secure infrastructure.

---

## Sprint 1: Core Intelligence Integration
**Focus:** Replacing backend mocks with real LLM and Vector DB connections.
**Duration:** 1 Sprint

*   **Ticket 1.1: LLM Service Integration**
    *   **Task:** Implement OpenAI and Anthropic provider classes in `server/services/llm_runner.py`.
    *   **Acceptance Criteria:** Real API calls replace `asyncio.sleep` mocks; error handling and rate limiting implemented.
*   **Ticket 1.2: Vector DB Implementation**
    *   **Task:** Set up pgvector schema and connection.
    *   **Acceptance Criteria:** Database initialized with vector extension.
*   **Ticket 1.3: Semantic Memory Pipeline**
    *   **Task:** Implement embedding generation and similarity search.
    *   **Acceptance Criteria:** Hardcoded context chunks replaced by dynamic retrieval from pgvector.

---

## Sprint 2: Data Persistence & API Wiring
**Focus:** Full-stack wiring to ensure all data is persisted and retrieved from the database.
**Duration:** 1 Sprint

*   **Ticket 2.1: Backend DB Schemas & Endpoints**
    *   **Task:** Create SQLAlchemy models and FastAPI endpoints for Chats and Projects.
    *   **Acceptance Criteria:** Full CRUD capability tested via Swagger/Postman.
*   **Ticket 2.2: Frontend ChatScopeInterface Refactor**
    *   **Task:** Update `ChatScopeInterface.jsx` to consume real APIs.
    *   **Acceptance Criteria:** Chat history and project scope persist across page reloads.
*   **Ticket 2.3: Frontend Global State Migration**
    *   **Task:** Audit remaining static state components and wire them to backend endpoints.
    *   **Acceptance Criteria:** No static mock data remains in standard UI flows.

---

## Sprint 3: Real-Time Orchestration
**Focus:** Connecting the backend DAG runner to the frontend via WebSockets.
**Duration:** 1.5 Sprints

*   **Ticket 3.1: Redis & WebSocket Backend Setup**
    *   **Task:** Configure Redis as a message broker and implement FastAPI WebSocket endpoints.
    *   **Acceptance Criteria:** Backend can broadcast test messages to connected WebSocket clients.
*   **Ticket 3.2: DAG Runner Broadcast Events**
    *   **Task:** Instrument the backend DAG runner to publish state changes to Redis channels.
    *   **Acceptance Criteria:** Node start, complete, and fail events are published to Redis.
*   **Ticket 3.3: Frontend Real-Time Listeners**
    *   **Task:** Refactor `PipelineExecutionViewer` and `PodChatContainer` to listen to WebSockets.
    *   **Acceptance Criteria:** Execution UI updates in real-time based on backend events. `simulateExecution()` is completely removed.

---

## Sprint 4: Secure Execution Sandbox
**Focus:** Implementing a safe environment for running untrusted custom agent code.
**Duration:** 2 Sprints

*   **Ticket 4.1: Sandbox Architecture & Prototyping**
    *   **Task:** Evaluate and prototype restricted Docker vs. Firecracker microVMs.
    *   **Acceptance Criteria:** Prototype successfully runs a basic Python script in isolation with network/resource limits.
*   **Ticket 4.2: Sandbox Deployment & Configuration**
    *   **Task:** Deploy the chosen sandbox infrastructure.
    *   **Acceptance Criteria:** Infrastructure is provisioning sandboxes dynamically.
*   **Ticket 4.3: Secure Dispatch API**
    *   **Task:** Build the backend service to send agent code to the sandbox and retrieve results securely.
    *   **Acceptance Criteria:** DAG runner successfully offloads untrusted code to the sandbox and processes the returned output.