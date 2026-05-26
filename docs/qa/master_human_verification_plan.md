# Agency OS Master Human Verification Plan

This document serves as the definitive master end-to-end human test script for Agency OS. It covers all core features, workflows, and portals to ensure the application meets all acceptance criteria prior to any major release. The testing flow is structured chronologically, matching a real-world user journey.

## Prerequisites & Setup
- Ensure the application stack is running (`docker-compose up` or local `npm run dev` & `python -m uvicorn`).
- **Test Accounts Required:**
  - **Agency Admin:** Full access to settings, billing, workspaces, agents, and system configurations.
  - **Agency Staff/Member:** Can work within assigned workspaces, create projects, but cannot alter global billing or API keys.
  - **Client Approver:** Restricted access, primarily interacting with chat, pipeline approvals, and specific assigned workspaces.
  - **Client Viewer:** Read-only access to assigned workspaces to view progress but cannot approve tasks or modify projects.
- Seed data generated (if applicable).

---

## 1. Phase 1: Admin Setup & Provisioning
*Testing the initial setup required before any client work can begin.*

### 1.1 API Key & Credentials Management
**Setup:** Log in as Agency Admin. Navigate to Credentials Manager.
**Steps:**
1. Add a new API key (e.g., for OpenAI or Anthropic).
2. Save the key (ensure it is masked in the UI).
3. Delete an old/unused key.
**Expected Outcomes:**
- [ ] Keys are saved securely and UI masks sensitive key data.

### 1.2 Workspace Creation & RBAC Setup
**Setup:** Log in as Agency Admin. Navigate to the Agency Panel.
**Steps:**
1. Create a new workspace, provision initial credits, and configure basic settings.
2. Navigate to Workspace Settings -> RBAC Manager.
3. Invite users and assign them specific roles (Agency Staff, Client Approver, Client Viewer).
**Expected Outcomes:**
- [ ] Admin successfully creates a new workspace.
- [ ] Invites are sent/recorded, and users are properly mapped to their assigned roles within the new workspace.

---

## 2. Phase 2: Project Creation & Discovery
*Testing how agency members initiate work within a provisioned workspace.*

### 2.1 Chat Interaction & Micro-Tasking
**Setup:** Log in as Agency Admin or Agency Staff. Navigate to the Workspace Chat Interface.
**Steps:**
1. Use the Context Switcher dropdown to select the newly created workspace.
2. Type a general query (e.g., "Hello, what can you help me with?") and send.
3. Request a micro-task (e.g., "Write a Python script to parse CSVs").
4. Approve the generated output for execution and review the response.
**Expected Outcomes:**
- [ ] Changing workspaces immediately updates the UI context.
- [ ] System accurately responds to queries and handles micro-task execution.

### 2.2 "Napkin Pitch" to Executable Plan
**Setup:** Log in as Agency Staff. Navigate to "Create New Project" flow.
**Steps:**
1. Pitch an idea via chat (e.g., "I want to build a simple web app for recipes").
2. Answer clarifying questions from the Orchestrator AI.
3. Observe the Automated Scoping phase and review generated documents in the split-view (Project Details, Draft PRD, Tech Spec, Task List).
4. Refine the plan by requesting a change in the chat.
5. Click "Approve Plan".
**Expected Outcomes:**
- [ ] Orchestrator accurately captures requirements and handles refinement requests dynamically.
- [ ] UI properly transitions to a split-view for document review.
- [ ] Approving the plan successfully queues the project into the Nexus Pipeline.

### 2.3 Document Ingestion Pipeline
**Setup:** Log in as Agency Staff. Have a sample PDF project brief ready.
**Steps:**
1. Click "Create Project via Document Upload" and select the PDF file.
2. Observe the Orchestrator analysis and review the structured Task Pipeline.
3. Click "Execute".
**Expected Outcomes:**
- [ ] The Orchestrator correctly extracts core features and generates a structured execution pipeline mapping to specialized agents.

---

## 3. Phase 3: Pipeline Execution & Orchestration
*Testing the core Nexus Pipeline and agent interactions.*

### 3.1 Execution Visibility & Intervention
**Setup:** Log in as Agency Admin or Staff.
**Steps:**
1. Navigate to the Pipeline Execution Viewer for the active project.
2. Observe the agents visualized as active nodes and view real-time logs.
3. Intervene via chat while a task is running (e.g., "Make the primary theme green instead").
4. Wait for a task requiring approval to pause the pipeline.
**Expected Outcomes:**
- [ ] The dashboard provides real-time visualization of agent nodes and execution logs.
- [ ] Orchestrator successfully intercepts manual intervention and updates the active agent's context.

---

## 4. Phase 4: Client Interaction & Approvals
*Testing access controls and approval flows from the client perspective.*

### 4.1 Client Approver Portal
**Setup:** Log in as Client Approver.
**Steps:**
1. Attempt to access the overarching Agency Panel, Credentials Manager, or global billing.
2. Navigate to the designated Client Workspace and open the pending project pipeline.
3. Click "Approve" on a pending task/step.
**Expected Outcomes:**
- [ ] Client Approver is strictly blocked (403 or hidden UI) from Admin-specific areas.
- [ ] Client can only view their assigned workspace.
- [ ] Approving a task successfully unpauses and triggers the next step in the pipeline.

### 4.2 Client Viewer Portal
**Setup:** Log in as Client Viewer.
**Steps:**
1. Navigate to the assigned Workspace and view the active pipeline.
2. Attempt to approve a task or edit a project requirement.
**Expected Outcomes:**
- [ ] Client Viewer can see real-time progress but all modification/approval controls are disabled or hidden.

---

## 5. Phase 5: Custom Agents & Marketplace
*Testing advanced platform extensions.*

### 5.1 Custom Agent Creation (Multi-Step Wizard)
**Setup:** Log in as Agency Admin. Navigate to the Custom Agent Creator.
**Steps:**
1. **Validation Check:** Try clicking "Next" without filling out required fields on Step 1. Verify error.
2. Complete Steps 1-4 (Identity, Rules, Capabilities, System Prompt).
3. Click "Submit" or "Save Agent".
4. Go to the Chat Interface and request a task tailored for the new agent.
**Expected Outcomes:**
- [ ] Wizard accurately maintains state and validates input.
- [ ] Agent is successfully created, saved to the backend, and appears in the agent roster.
- [ ] Orchestrator can immediately assign tasks to the new agent dynamically.

### 5.2 Marketplace Usage
**Setup:** Log in as Agency Admin. Navigate to the Marketplace.
**Steps:**
1. Browse available pre-built agents and click "Install" on one.
2. Verify the installed agent appears in the active agents list.
**Expected Outcomes:**
- [ ] Installation completes successfully and the agent is immediately usable.

---

## 6. Phase 6: System Monitoring & Audit
*Testing global tracking and observability.*

### 6.1 Analytics & Global View
**Setup:** Log in as Agency Admin.
**Steps:**
1. Access the Analytics Dashboard.
**Expected Outcomes:**
- [ ] Analytics display aggregated metrics correctly across all active workspaces.

### 6.2 Audit Log Exports
**Setup:** Log in as Agency Admin. Navigate to the Audit Log Viewer.
**Steps:**
1. Verify that recent actions (Workspace Creation, Approvals, Agent Creation) are recorded.
2. Click "Export CSV".
**Expected Outcomes:**
- [ ] Audit log accurately reflects cross-role activities with precise timestamps.
- [ ] Export triggers a properly formatted file download.

---

## 7. Supplemental Role-Based & Security Test Scripts
*(Consolidated from Fix & Wire Verification)*

### 7.1 Inviting a New User to a Workspace
**Scenario A: Agency Admin Invites a Client**
- **Role:** Agency Admin
- **Steps:**
  1. Navigate to **Workspace Settings** > **Members**.
  2. Click **Invite User**, enter email, select **Client Approver**.
  3. Click **Send Invitation**.
- **Expected Outcome:** Success notification; user appears as "Pending".

**Scenario B: Client Attempts to Invite a User (Negative Test)**
- **Role:** Client
- **Expected Outcome:** The **Invite User** button should be disabled or hidden.

### 7.2 Editing a User's Role
**Scenario:** Agency Admin Changes User Role
- **Steps:**
  1. Navigate to **Workspace Settings** > **Members**.
  2. Click **Edit Role** for an existing user.
  3. Change role to **Client Approver** and Save.
- **Expected Outcome:** Member list updates immediately. Log in as that user to verify UI restricts admin-only features.

### 7.3 Managing API Keys (Generating and Revoking)
**Scenario A: Agency Admin Generates Key**
- **Steps:**
  1. Navigate to **Settings** > **API Keys**.
  2. Click **Generate New Key**, name it, click **Create**.
- **Expected Outcome:** Key generated and displayed once. Appears partially obscured in active list.

**Scenario B: Agency Admin Revokes Key**
- **Steps:**
  1. In **API Keys**, click **Revoke** on an existing key.
- **Expected Outcome:** Key removed from list; subsequent API calls with it return 401.

### 7.4 Exporting Data (CSV/Downloads)
**Scenario A: Audit Logs**
- **Steps:** Go to **Audit Logs**, apply filters, click **Export to CSV**.
- **Expected Outcome:** CSV downloads with accurate, filtered data (timestamps, users, actions, IPs).

**Scenario B: Analytics Data**
- **Steps:** Go to **Analytics Dashboard**, click **Export** on a chart/table.
- **Expected Outcome:** Downloaded file accurately reflects current dashboard data.
