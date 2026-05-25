# Agency OS Master Human Verification Plan

This document serves as the definitive master end-to-end human test script for Agency OS. It covers all core features, workflows, and portals to ensure the application meets all acceptance criteria prior to any major release.

## Prerequisites & Setup
- Ensure the application stack is running (`docker-compose up` or local `npm run dev` & `python -m uvicorn`).
- Test accounts required:
  - **Agency Admin:** Full access to settings, billing, workspaces, agents.
  - **Client Approver:** Restricted access, primarily interacting with chat, pipeline approvals, and specific workspaces.
- Seed data generated (if applicable).

---

## 1. Core Conversational Engine (Chat UI & Project Creation)

### 1.1 Chat Interaction & Micro-Tasking
**Setup:** Log in as either Agency Admin or Client Approver. Navigate to the Chat Interface or use the Universal Command Chat (Cmd+K).
**Steps:**
1. Type a general query (e.g., "Hello, what can you help me with?") and send.
2. Request a micro-task (e.g., "Write a Python script to parse CSVs and output a JSON summary").
3. Approve the generated output for execution and review the final response.
4. Use the Context Switcher dropdown to change the active workspace context and send a new message.
**Expected Outcomes:**
- [ ] System responds accurately to general queries.
- [ ] Universal command chat is easily accessible and responds to micro-tasks quickly.
- [ ] System parses task-based intents, generates code/output, asks for approval, executes, and returns results.
- [ ] Changing workspaces immediately updates the UI context, and subsequent messages are tied to the newly selected workspace.

### 1.2 "Napkin Pitch" to Executable Plan
**Setup:** Log in as Agency Admin. Navigate to the "Create New Project" flow.
**Steps:**
1. Start a new project by pitching an idea via chat (e.g., "I want to build a simple web app for recipes").
2. Answer clarifying questions from the Orchestrator AI to complete discovery.
3. Observe the Automated Scoping phase.
4. Review the generated documents in the split-view (Chat on left, Docs on right), verifying the tabbed interface functions correctly (Project Details, Draft PRD, Tech Spec, Task List).
5. Attempt to share the documents via link or email, and trigger an internal review alert.
6. Refine the plan by requesting a change in the chat (e.g., "Add social sharing to recipes").
7. Click "Approve Plan".
**Expected Outcomes:**
- [ ] The Orchestrator correctly asks clarifying questions.
- [ ] The UI successfully transitions to a split-view with functional tabs presenting Project Details, Draft PRD, Technical Spec, and Initial Task List.
- [ ] Documents can be successfully exported, shared, and trigger notifications.
- [ ] The AI instantly updates documents based on refinement requests.
- [ ] Approving the plan transitions the project into the Nexus Pipeline orchestration.

---

## 2. Document Ingestion Pipeline

### 2.1 File Upload & Pipeline Generation
**Setup:** Log in as an Agency Admin. Have a sample PDF and Markdown project brief ready.
**Steps:**
1. Click "Create Project via Document Upload" and select the PDF file.
2. Observe the upload progress and Orchestrator analysis phase.
3. Review the generated structured Task Pipeline.
4. Make minor adjustments to the pipeline and click "Execute".
**Expected Outcomes:**
- [ ] Files upload successfully with clear UI feedback.
- [ ] The Orchestrator extracts core features and translates them into a structured execution pipeline of tasks.
- [ ] The generated pipeline correctly maps to epics and assigns specialized agents.
- [ ] Clicking "Execute" correctly triggers the Nexus Pipeline.

---

## 3. Nexus Pipeline Orchestration

### 3.1 Execution Visibility & Intervention
**Setup:** Log in as Agency Admin. Ensure a pipeline has been approved and is running.
**Steps:**
1. Navigate to the Project Dashboard / Pipeline Execution Viewer.
2. Observe the agents visualized as active nodes and view real-time logs.
3. While a task is running (e.g., UI Design), intervene via chat (e.g., "Make the primary theme green instead").
4. Observe the final delivery and presentation for review.
**Expected Outcomes:**
- [ ] UI successfully transitions to "Execution Mode" from "Planning Mode".
- [ ] The dashboard provides real-time visualization of agent nodes and execution logs.
- [ ] Orchestrator successfully intercepts manual intervention, updates context, and redirects the active agent.
- [ ] The pipeline successfully runs to completion, tests are triggered via QA agents, and final review alerts are dispatched.

---

## 4. Portals: Agency Admin vs. Client Approver Flows

### 4.1 Agency Admin Portal
**Setup:** Log in as Agency Admin.
**Steps:**
1. Navigate to the Agency Panel.
2. Create a new workspace, assign a client, and provision initial credits.
3. Access the Analytics Dashboard and verify aggregated metric visibility across workspaces.
**Expected Outcomes:**
- [ ] Admin has unrestricted access to create workspaces and manage client assignments.
- [ ] Analytics display correctly for the global agency view.

### 4.2 Client Approver Portal
**Setup:** Log in as Client Approver.
**Steps:**
1. Attempt to access the overarching Agency Panel or global billing (should be restricted).
2. Navigate to the designated Client Workspace.
3. View pending tasks or pipeline steps requiring approval.
4. Click "Approve" on a pending item.
**Expected Outcomes:**
- [ ] Client Approver cannot access Agency Admin specific pages (receives 403 or UI elements are hidden).
- [ ] Client can only view workspaces they are explicitly assigned to.
- [ ] Approving a task successfully triggers the next step in the pipeline.

---

## 5. Custom Agent & Marketplace Interaction

### 5.1 Custom Agent Creation (Multi-Step Wizard)
**Setup:** Log in as Agency Admin. Navigate to the Custom Agent Creator.
**Steps:**
1. **Validation Check:** On Step 1, try clicking "Next" without filling out required fields (Name, Role). Verify validation error appears.
2. **Step 1: Identity:** Enter the agent Name, Role, and Version. Click Next.
3. **Step 2: Rules & Constraints:** Enter the System rules path, select the Enforcement level, and provide a markdown list of constraints. Click Next.
4. **Step 3: Capabilities:** Enter a markdown list of capabilities. Click Next.
5. **Step 4: System Prompt & Review:** Enter the System Prompt in the textarea. Review the final summary of the agent configuration.
6. **Error Handling Check:** Intentionally disconnect the network or simulate an API failure to verify error toast/message is displayed on submit.
7. Click "Submit" or "Save Agent".
8. **File Verification:** Check the backend file system to ensure the agent markdown file was created in the correct `agents/` directory and contains the proper YAML frontmatter and format matching `config/agent_base.yaml`.
9. Go to the Chat Interface and request a task specifically tailored for the newly created agent to ensure dynamic mapping by the Orchestrator works without a restart.
**Expected Outcomes:**
- [ ] Wizard accurately maintains state across steps and validates required fields.
- [ ] Backend successfully processes the complex payload and generates the YAML-frontmatter markdown file in the correct directory.
- [ ] Agent appears in the agent roster for the assigned workspace.
- [ ] The Orchestrator successfully assigns tasks to the newly created agent dynamically.

### 5.2 Marketplace Usage
**Setup:** Log in as Agency Admin. Navigate to the Marketplace.
**Steps:**
1. Browse available pre-built agents/integrations.
2. Select an agent (e.g., "SEO Specialist") and click "Install" or "Add to Workspace".
3. Verify the installed agent appears in the workspace's active agents list.
**Expected Outcomes:**
- [ ] Marketplace catalog loads properly.
- [ ] Installation flow completes successfully.
- [ ] Installed agents are immediately usable within the designated workspace context.

---

## 6. Workspace Settings, RBAC, API Keys, and Audit Logs

### 6.1 RBAC & Workspace Settings
**Setup:** Log in as Agency Admin. Navigate to Workspace Settings -> RBAC Manager.
**Steps:**
1. Invite a new user to the workspace with a specific role (e.g., "Viewer").
2. Log in as the newly invited user and verify restrictions (e.g., cannot delete workspace).
**Expected Outcomes:**
- [ ] Role assignments enforce correct UI and API access levels.

### 6.2 API Key Management (Credentials)
**Setup:** Log in as Agency Admin. Navigate to Credentials Manager.
**Steps:**
1. Add a new API key (e.g., for OpenAI or Anthropic).
2. Save the key (ensure it is masked in the UI).
3. Delete an old/unused key.
**Expected Outcomes:**
- [ ] Keys are saved securely and UI masks sensitive key data.

### 6.3 Audit Log Exports
**Setup:** Log in as Agency Admin. Navigate to the Audit Log Viewer.
**Steps:**
1. Generate some activity (e.g., log in, create an agent, delete a key).
2. View the Audit Log table to confirm events are recorded.
3. Click the "Export CSV" (or equivalent export) button.
**Expected Outcomes:**
- [ ] Recent actions are accurately reflected in the audit log table with timestamps and actor details.
- [ ] Export triggers a file download containing the correct log data in a structured format.
