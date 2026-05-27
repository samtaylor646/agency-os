# Epic: Project Scope UI Remediation

## 1. Overview
This Epic consolidates the remaining frontend remediation work identified in the `application_audit_report.md`. While the backend infrastructure (DAG orchestration, Redis, Secure Sandbox) has been successfully implemented, the frontend 'Project Scope' interface (`ChatScopeInterface.jsx`) remains incomplete. It currently lacks the ability to ingest files (PDF, TXT, MD) and continues to rely on static mock data in some areas. 

This Epic is the single source of truth for bridging the remaining gap between the robust backend infrastructure and the user interface.

## 2. Goals
*   **Enable Document Ingestion:** Allow users to upload requirement documents directly into the chat interface.
*   **Context Verification:** Ensure the UI correctly displays the real, dynamic data parsed by the backend LLM runner, replacing all hardcoded fallbacks.
*   **State Persistence:** Ensure the UI accurately reflects the real-time state of the project derived from the database and WebSocket events.

## 3. Scope of Work

### Ticket A: Document Ingestion UI
*   **Component:** `client/src/ChatScopeInterface.jsx`
*   **Task:** Implement a file upload button/input within the chat interface.
*   **Requirements:**
    *   Accept `.txt`, `.md`, and `.pdf` files.
    *   Show loading state/spinner during upload.
    *   Post the file using `FormData` to the existing backend endpoint: `/api/v1/chat/{chat_id}/documents/upload`.
    *   Inject a system success message into the chat UI upon successful upload (e.g., "Successfully ingested requirements.pdf").

### Ticket B: Context Integration & LLM Wiring
*   **Component:** `client/src/ChatScopeInterface.jsx`
*   **Task:** Ensure the parsed context from uploaded documents updates the Right-Hand "Project Details" panel.
*   **Requirements:**
    *   The backend extraction payload from the upload endpoint must be appended/merged into the frontend `projectDetails` state.
    *   Verify that the `.env` configuration (e.g., `LLM_PROVIDER_TYPE`) is correctly set so document parsing utilizes real intelligence (OpenAI/Anthropic) rather than mock fallback responses.

### Ticket C: End-to-End QA
*   **Component:** E2E Test Suite
*   **Task:** Formally test the ingestion pipeline.
*   **Requirements:**
    *   Upload a sample text document.
    *   Verify the extracted metadata (Project Name, Description, Tech Stack) populates the Right-Hand panel correctly.
    *   Sign off the Epic in `docs/qa/`.

## 4. Execution Plan
*   **Role:** Frontend Developer
*   **Branch:** `epic/project-scope-remediation`
*   **Prerequisites:** Backend endpoint `/api/v1/chat/{chat_id}/documents/upload` is confirmed active.
