# Master Human Verification Plan

This document serves as the master source of truth for all human-in-the-loop QA testing and verification across AgencyOS. It includes step-by-step instructions for testing core flows, UI/UX integrity, and tenant isolation.

---

## 1. Create Agent Wizard

### Objective
Accurately verify the functionality, UI/UX, and tenant isolation of the "Create Agent Wizard" when defining custom agents.

### Prerequisites
- [] AgencyOS local environment is running.
- [] Tester is logged in as Workspace Admin.
- [] Tester has access to a primary and secondary workspace.

### Step-by-Step Verification
- [ ] **1. Initialization:** Click "Create Custom Agent". Verify the modal/page opens without console errors and UI matches design specs.
- [ ] **2. Form Validation:** Attempt to submit empty. Verify validation errors (e.g., "Agent Name is required") appear.
- [ ] **3. Edge Case Inputs:** Enter a 200+ character name. Verify input constrains or wraps cleanly. Add special characters to prompt fields. Verify text is sanitized and accepted without 500 errors.
- [ ] **4. Capabilities:** Toggle agent capabilities/tools. Verify UI reflects active states correctly.
- [ ] **5. Submission:** Fill all required fields and submit. Verify loading spinner appears, followed by a success toast. Verify the new agent appears in the list.
- [ ] **6. Tenant Isolation:** Switch context to a different workspace. Verify the newly created agent is **NOT** visible.
- [ ] **7. Error Handling:** Disconnect network/server and submit. Verify a graceful error message appears instead of a crash.

---

## 2. Workspace Management (Pending Execution)

*Placeholder for workspace creation, RBAC testing, and deletion flows.*

---

## 3. Chat Interface & Context Switching (Pending Execution)

*Placeholder for testing chat scoping, history retention, and active context switching.*

---

## 4. Pipeline Orchestration (Phase 2 - Ready for Execution)

### Objective
Accurately verify the execution of the Phase 2 Core Engine, including NEXUS DAG orchestration, LLM integration, and semantic memory.

### Step-by-Step Verification
- [ ] **1. DAG Initialization:** Trigger a complex task list and verify the DAG structure is created and visible in the orchestrator logs.
- [ ] **2. LLM Integration:** Monitor nodes executing and verify real API calls are dispatched to the LLM backend (OpenAI/Anthropic).
- [ ] **3. Semantic Memory:** Provide context from a previous step and verify the vector database accurately retrieves and applies the memory.
- [ ] **4. State Persistence:** Pause the pipeline mid-execution and verify `workflow_executions` saves the exact state. Resume to verify accurate continuation.
- [ ] **5. Resilience:** Induce a transient network failure during a node execution. Verify exponential backoff and retry logic trigger correctly without full pipeline failure.

---

## 5. Phase 5 Verification: Feedback Loops, Interventions & Rollbacks

### Objective
Accurately verify the functionality of human-in-the-loop interventions, execution rollbacks, and active feedback loops.

### Step-by-Step Verification
- [ ] **1. Intervention Trigger:** Run a standard pipeline. While running, click "Intervene". Verify the pipeline pauses and state is saved.
- [ ] **2. Mid-Execution Edits:** Provide feedback in the chat. Verify the orchestrator acknowledges and alters the DAG state.
- [ ] **3. Rollback Execution:** Trigger a rollback command to a previous node. Verify database state matches the expected state.
- [ ] **4. Resume Verification:** Click "Resume". Verify pipeline picks up from the modified state seamlessly.

---

## 6. Phase 6 Verification: Template Library & Routing

### Objective
Accurately verify template creation, discovery, and instantiation.

### Step-by-Step Verification
- [ ] **1. Template Browsing:** Open Template Marketplace. Verify templates load with correct metadata.
- [ ] **2. Instantiation:** Select "SaaS Starter". Verify new workspace/project is populated with correct agents and base files.
- [ ] **3. API Selector:** Open Project Settings -> API Selector. Verify model routing respects custom selections (e.g., GPT-4 vs Claude 3.5 Sonnet).

