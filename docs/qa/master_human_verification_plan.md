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

## 4. Pipeline Orchestration (Pending Execution)

*Placeholder for DAG execution, central runner validation, and human-in-the-loop phase gates.*

