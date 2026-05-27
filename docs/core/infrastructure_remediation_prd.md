# Infrastructure Remediation PRD

## 1. Executive Summary
The AgencyOS prototype currently relies on mocked data, `asyncio.sleep` delays, and static frontend state. To evolve into a production-ready system, we must migrate to real infrastructure. This PRD outlines the sequential remediation of the core infrastructure to replace all mocks with robust, stateful, and secure real-world integrations.

## 2. Objectives
- Replace mocked LLM and Vector DB responses with actual API integrations.
- Implement database persistence for all entities (chats, projects, workspaces).
- Replace simulated frontend execution states with real-time websocket/polling updates from the backend DAG runner.
- Establish a secure execution environment for running arbitrary custom agent code safely.

## 3. Epics and Requirements

### Epic 1: Core Intelligence Integration (Backend First)
**Goal:** Replace the `asyncio.sleep` mocks with real LLM integration and vector storage.

*   **LLM Provider Integration:** 
    *   Implement real connections to OpenAI and Anthropic APIs within `server/services/llm_runner.py`.
    *   Ensure proper error handling, retry logic, and token usage tracking.
*   **Semantic Memory Pipeline:** 
    *   Integrate pgvector for real Vector DB storage and retrieval.
    *   Replace hardcoded context chunks with actual embedding generation and similarity search logic.

### Epic 2: Data Persistence & API Wiring (Full Stack)
**Goal:** Make the "Project Scope" and UI stateful.

*   **Backend Database Integration:** 
    *   Design and deploy database schemas for workspaces, active chats, draft projects, and pipeline executions.
    *   Develop fully functional CRUD endpoints for these entities.
*   **Frontend State Management:** 
    *   Refactor `client/src/ChatScopeInterface.jsx` and related UI components.
    *   Transition from static React state to fetching, updating, and persisting data via backend APIs.

### Epic 3: Real-Time Orchestration (Full Stack)
**Goal:** Connect the frontend execution UI to the backend DAG runner.

*   **Backend Real-Time Broker:** 
    *   Implement WebSocket connections or robust long-polling endpoints.
    *   Utilize a Redis message broker to broadcast real-time pipeline execution states from the backend DAG runner.
*   **Frontend Real-Time Listeners:** 
    *   Refactor `PipelineExecutionViewer` and `PodChatContainer`.
    *   Implement WebSocket listeners to consume live execution updates.
    *   Remove all `simulateExecution()` and `setTimeout` mock logic.

### Epic 4: Secure Execution Sandbox (DevOps/Backend)
**Goal:** Safely run arbitrary custom agent code.

*   **Sandbox Design & Deployment:** 
    *   Design a secure containerized environment for executing untrusted custom agent code.
    *   Implement restricted Docker containers or isolated Firecracker microVMs.
    *   Ensure the host system is protected from malicious or runaway agent processes (resource limits, network restrictions).
*   **Execution API:**
    *   Build internal APIs to dispatch code to the sandbox and securely stream logs and results back to the orchestrator.

## 4. Success Metrics
- **0%** simulated/mocked delays (`asyncio.sleep`) in the critical path.
- Persistent state across browser refreshes for all chat and project data.
- Live pipeline execution tracking latency < 500ms.
- 100% of untrusted agent code executes within the isolated sandbox environment.