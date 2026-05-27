# Human-in-the-Loop (HITL) Manual Validation Instructions: Custom Agent Remediation Epic - Phase 2

**Epic:** Custom Agent Remediation
**Phase:** 2 (Data Adapter & Strict Schema Enforcement)
**Target Roles:** QA Engineer, Lead Developer, or Product Manager

This document outlines the mandatory manual validation steps required before Phase 2 can be considered complete and ready for merge. These steps ensure that the frontend data adapters, backend strict schemas, and atomic transaction mechanisms are functioning as designed.

---

## Prerequisites
1. Ensure you are on the epic feature branch: `epic-custom-agent-remediation` (or the specific Phase 2 branch).
2. Start the local development environment:
   ```bash
   # Start backend
   cd server && uvicorn main:app --reload
   
   # Start frontend (in a separate terminal)
   cd client && npm run dev
   ```
3. Have your browser's Developer Tools (Network and Console tabs) open.

---

## Validation Step 1: Frontend Payload Adapter Verification (`CustomAgentCreator.jsx`)

**Objective:** Verify that the frontend correctly intercepts legacy state formats and translates them into the new strict nested schema before sending the payload to the backend.

### Instructions:
1. Navigate to the **Custom Agent Creator** UI in the application (usually `/create-agent` or via the Sidebar).
2. Fill out the form with valid data for a new custom agent (Name, Role, Tools, System Prompt, etc.).
3. Open the **Network Tab** in your Developer Tools.
4. Click the **"Create Agent"** (or "Save") button.
5. In the Network Tab, locate the `POST` request to the backend endpoint (e.g., `/api/agents` or `/api/custom-agents`).
6. Inspect the **Request Payload**.

### Expected Outcome:
The payload MUST match the strict nested schema. It should NOT contain top-level legacy fields.
*   **Correct (Nested):**
    ```json
    {
      "metadata": {
        "name": "TestAgent",
        "description": "A test agent"
      },
      "capabilities": {
        "tools": ["search", "write"],
        "llm_config": { ... }
      }
    }
    ```
*   **Incorrect (Legacy/Flat):**
    ```json
    {
      "name": "TestAgent",
      "tools": ["search"],
      "description": "A test agent"
    }
    ```
**Sign-off Criteria:** The Request Payload strictly adheres to the nested schema structure.

---

## Validation Step 2: Backend Strict Schema Rejection (`server/schemas.py`)

**Objective:** Verify that the backend actively rejects legacy or improperly formatted payloads, preventing bad data from entering the system.

### Instructions:
1. Open a terminal or an API client (like Postman or cURL).
2. Attempt to send a `POST` request to the custom agent creation endpoint using a **legacy (flat) payload format**.

   *Example cURL command:*
   ```bash
   curl -X POST http://localhost:8000/api/custom-agents \
   -H "Content-Type: application/json" \
   -d '{"name": "BadAgent", "role": "tester", "system_prompt": "do things"}'
   ```
3. Observe the HTTP response.

### Expected Outcome:
*   The backend MUST respond with a **422 Unprocessable Entity** (or similar 4xx client error).
*   The response body MUST contain validation error details indicating that required nested fields (e.g., `metadata`, `capabilities`) are missing, or that extra (forbidden) legacy fields are present.
*   The agent MUST NOT be created in the database or filesystem.

**Sign-off Criteria:** The server rejects flat payloads and returns appropriate validation errors.

---

## Validation Step 3: Atomic Transactions and Rollback (`server/routers/custom_agents.py`)

**Objective:** Verify that if the final step of agent creation (e.g., writing the markdown file to the filesystem) fails, the entire transaction rolls back, leaving no orphaned database records.

### Instructions:
*Note: This step requires simulating a failure. You can either use a dedicated test endpoint/script if provided by engineering, or manually force a failure.*

**Manual Simulation Method:**
1. Temporarily modify the backend code in `server/routers/custom_agents.py`.
2. Locate the function responsible for saving the agent (e.g., `create_custom_agent`).
3. Inject an artificial error *after* the database commit but *before* or *during* the file write operation.
   *Example:*
   ```python
   # ... database insert logic ...
   
   # INJECT ERROR HERE:
   raise Exception("Simulated file write failure for HITL testing")
   
   # ... file write logic ...
   ```
4. Restart the backend server if it doesn't auto-reload.
5. Using the UI or an API client, attempt to create a valid custom agent.
6. Observe the failure response (likely a 500 Internal Server Error).
7. Check the Database (or Agent List UI).

### Expected Outcome:
*   The request fails as expected due to the simulated exception.
*   **CRITICAL:** The newly attempted agent MUST NOT appear in the database. The rollback mechanism must have caught the exception and undone the database insertion.
*   (Remember to remove the injected error from `custom_agents.py` after testing).

**Sign-off Criteria:** A simulated failure during file writing results in a complete rollback, leaving no partial state.

---

## Final Sign-off

Reviewer Name: _______________________
Date: _______________________
Status: [ ] PASS / [ ] FAIL

*If FAIL, specify the step and details of the failure in the Epic's comment thread.*