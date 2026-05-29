# AgencyOS Full Application Audit Plan

## 1. Overview
This audit plan outlines the expected features to be built at this stage of AgencyOS, based on the core documentation (`PRD.md`, `AgencyOS_Comprehensive_Overview.md`, `Phase_2_Automated_Scoping_Spec.md`, `Phase_3_Rebuild_Master_Plan.md`, and `chat_scope_interface_redesign.md`). A primary focus is evaluating the 'Project Scope' feature, which is currently reported to contain dummy data instead of production-ready functionality.

## 2. Expected Feature List (Global Audit Criteria)
The application must currently possess the following core features:

1. **Conversational UI & Chat Engine:**
   - Persistent, context-aware chat acting as the primary project/task entry point.
   - Real LLM integration for processing user intents and managing conversation state.
   - Responsive UI (Atlassian-inspired) with a main chat area and robust accessibility features (focus trapping, ARIA roles).

2. **Nexus Pipeline Orchestration:**
   - Real LLM task execution via a resilient DAG orchestrator (`central_runner.py`).
   - Workflow state persistence in the database with graceful failure handling, retries, and strict Pydantic schema validation.

3. **Custom Agents & Storage:**
   - Multi-tenant S3 (or local fallback) storage for agent markdown configurations.
   - Full CRUD API (Create, Read, Update, Delete) for custom agents via a multi-step Wizard UI.
   - Instant availability of newly created agents for dynamic task assignment.

4. **Enterprise Foundation:**
   - Multi-tenancy and Workspace management.
   - Role-Based Access Control (RBAC) (e.g., Client Approver vs. Client Viewer restrictions).
   - Audit Logging and secure API Key Management.

## 3. Project Scope Feature Audit (Deep Dive)
**Current Issue:** The 'Project Scope' UI (`ChatScopeInterface`) currently displays hardcoded dummy data instead of dynamically generated context.

**Expected State & Audit Criteria:**
To successfully pass the audit, the 'Project Scope' feature must satisfy the following criteria:

### A. Document Generation & Integration
- **Actual LLM Data:** The contextual details panel (Right-hand drawer/sidebar) MUST display real, dynamically generated project details (Project Name, Description, Tech Stack, Draft PRD) derived from the active chat or ingested documents, completely replacing the dummy text.
- **Document Generators Active:** The backend `PRDGenerator`, `EngineeringSpecGenerator`, and `TaskListGenerator` must actively process the conversation history and output structured Markdown.
- **State Persistence & Real-time Updates:** The generated documents must accurately reflect the ongoing conversation state, updating iteratively as the user modifies requirements in chat.

### B. Document Ingestion (Uploads)
- **File Parsing:** Users must be able to upload unstructured/structured documents (PDF, Markdown, TXT) directly into the chat interface.
- **Context Injection:** Uploaded text must be correctly parsed and appended to the context window to seed the scoping pipeline and document generation.

### C. UI & Architecture Validation
- **Three-Pane Layout:** Verification of the implemented layout (Left Nav, Main Chat, Right Contextual Details Drawer).
- **Responsive Behavior:** The right contextual drawer must correctly collapse, slide-over, or tuck behind a hamburger menu on smaller device breakpoints.
- **Document Viewing:** Ability to view generated Markdown alongside the chat cleanly, with options to copy to clipboard or save to the project directory.

## 4. Next Steps & Execution
1. **Frontend Code Review:** Review `client/src/ChatScopeInterface.jsx` and related components to identify where dummy data is injected and wire it to the correct API endpoints.
2. **Backend API Validation:** Verify the availability and functionality of document ingestion and generation endpoints (e.g., `/api/chat/{id}/documents/upload`, `/api/chat/{id}/generate/{doc_type}`).
3. **Manual QA Pass:** The Evidence Collector agent must perform a manual validation on the staging environment against the criteria outlined in this document before signing off.