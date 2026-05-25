# Agency OS Master Human Verification Plan

This document serves as the definitive master end-to-end human test script for Agency OS. It covers all core features, workflows, and portals to ensure the application meets all acceptance criteria prior to any major release.

## Prerequisites & Setup
- Ensure the application stack is running (`docker-compose up` or local `npm run dev` & `python -m uvicorn`).
- Test accounts required:
  - **Agency Admin:** Full access to settings, billing, workspaces, agents.
  - **Client Approver:** Restricted access, primarily interacting with chat, pipeline approvals, and specific workspaces.
- Seed data generated (if applicable).

---

## 1. Core Conversational Engine (Chat UI & Task Generation)

### 1.1 Chat Interaction
**Setup:** Log in as either Agency Admin or Client Approver. Navigate to the Chat Interface.
**Steps:**
1. Type a general query (e.g., "Hello, what can you help me with?") and send.
2. Type a specific task generation prompt (e.g., "Draft a marketing email for a new product launch").
3. Use the Context Switcher dropdown to change the active workspace context and send a new message.
**Expected Outcomes:**
- [ ] System responds accurately to general queries.
- [ ] System parses task-based intents and visually indicates a "Task Generated" state (or provides a structured task response).
- [ ] Changing workspaces immediately updates the UI context, and subsequent messages are tied to the newly selected workspace.

---

## 2. Document Ingestion (PDF/Markdown Upload)

### 2.1 File Upload & Processing
**Setup:** Log in as an Agency Admin. Have a sample PDF and Markdown file ready. Navigate to the Workspace settings or dedicated Document Upload area.
**Steps:**
1. Click the upload area or button and select the PDF file.
2. Observe the upload progress and processing state.
3. Repeat the process for the Markdown (.md) file.
4. Go back to the Chat Interface and ask a question specifically related to the contents of the uploaded documents.
**Expected Outcomes:**
- [ ] Files upload successfully with clear UI feedback (progress bars, success toasts).
- [ ] Uploaded documents appear in the workspace's document list.
- [ ] The conversational engine successfully retrieves context from the newly uploaded documents and incorporates it into the chat response.

---

## 3. Nexus Pipeline Execution

### 3.1 Viewing Logs & Execution State
**Setup:** Log in as Agency Admin. Navigate to the Pipeline Execution Viewer.
**Steps:**
1. Identify a recently executed or currently running pipeline in the list.
2. Click to expand or view details of the pipeline run.
3. Observe the state changes (e.g., Pending -> Running -> Completed/Failed).
4. Review the execution logs provided in the UI.
**Expected Outcomes:**
- [ ] Pipelines are listed clearly with their current status.
- [ ] Expanding a pipeline shows a detailed, real-time (or near real-time) log of execution steps.
- [ ] Status indicators accurately reflect the backend state.

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
1. **Step 1: Identity:** Enter the agent Name, Role, and Version. Click Next.
2. **Step 2: Rules & Constraints:** Enter the System rules path, select the Enforcement level, and provide a markdown list of constraints. Click Next.
3. **Step 3: Capabilities:** Enter a markdown list of capabilities. Click Next.
4. **Step 4: System Prompt & Review:** Enter the System Prompt in the textarea. Review the final summary of the agent configuration.
5. Click "Submit" or "Save Agent".
6. Go to the Chat Interface and mention/select the newly created agent.
**Expected Outcomes:**
- [ ] Wizard accurately maintains state across the 4 steps, allowing back-and-forth navigation without data loss.
- [ ] Form validates required fields before allowing progression to the next step.
- [ ] Backend successfully processes the complex payload and generates the YAML-frontmatter markdown file.
- [ ] Agent is created and appears in the agent roster for the assigned workspace.
- [ ] The specific agent can be invoked in chat and responds according to its custom system prompt.

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
- [ ] Keys are saved securely.
- [ ] UI masks sensitive key data after creation.

### 6.3 Audit Log Exports
**Setup:** Log in as Agency Admin. Navigate to the Audit Log Viewer.
**Steps:**
1. Generate some activity (e.g., log in, create an agent, delete a key).
2. View the Audit Log table to confirm events are recorded.
3. Click the "Export CSV" (or equivalent export) button.
**Expected Outcomes:**
- [ ] Recent actions are accurately reflected in the audit log table with timestamps and actor details.
- [ ] Export triggers a file download containing the correct log data in a structured format.
