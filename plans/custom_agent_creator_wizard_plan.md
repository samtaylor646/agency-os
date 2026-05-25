# Custom Agent Creator Wizard Implementation Plan

## 1. Overview
The current Custom Agent Creator is a single-page form that generates a basic markdown file with simple frontmatter. To align with the standard agent template format (as defined in `config/agent_base.yaml` and our system conventions), we need to update the application to output a more structured format including `identity`, `system_rules`, `capabilities`, `constraints`, and `system_prompt`.

To improve user experience and handle the increased complexity of the agent configuration, the frontend UI will be upgraded from a single form to a **Multi-Step Wizard**. The backend API will also be updated to accept these structured fields and generate the correct template file format.

### Key Changes
*   **Frontend UI (React):** Convert `CustomAgentCreator.jsx` into a stepped wizard interface (e.g., Step 1: Identity, Step 2: Rules & Constraints, Step 3: Capabilities, Step 4: System Prompt).
*   **Backend API (Python/FastAPI):** Update the `POST /api/v1/custom_agents` route in `server/routers/custom_agents.py` to process the new data structure and generate a file that adheres to the `agent_base.yaml` / `.md` template format.

## 2. Agent Assignments

To ensure this epic is completed with maximum quality according to the NEXUS pipeline, the work will be distributed among specialized agents:

*   **UX Architect:** Responsible for designing the state management and layout flow of the multi-step wizard.
*   **Frontend Developer:** Responsible for implementing the React components, form validation, and state progression for the `CustomAgentCreator.jsx` wizard.
*   **Backend Architect:** Responsible for updating `schemas.py` (Pydantic models) and the API router in `server/routers/custom_agents.py` to write the updated file format.
*   **Evidence Collector:** Responsible for verifying the final integration, ensuring the UI steps work correctly, and confirming the generated file exactly matches the expected format.

## 3. Subtasks and Execution Checklist

The following checklist maps out the execution order. 

### Phase 1: Planning and Architecture
- [ ] **Task 1 (UX Architect):** Define the multi-step wizard UI flow and form fields mapping to the template structure.
- [ ] **Task 2 (Backend Architect):** Define the exact output format (YAML frontmatter vs pure YAML) required to match `config/agent_base.yaml` and update the Pydantic schema design (`schemas.CustomAgentCreate`).

### Phase 2: Backend Implementation
- [x] **Task 3 (Backend Architect):** Update `server/schemas.py` to include new fields: `identity` (name, role, version), `system_rules` (path, enforcement_level), `capabilities` (list), `constraints` (list), and `system_prompt` (string).
- [x] **Task 4 (Backend Architect):** Refactor `generate_agent_markdown` in `server/routers/custom_agents.py` to format the file properly according to the new schema.
- [x] **Task 5 (API Tester / Backend Architect):** Test the updated API endpoint via curl or Swagger UI to ensure the generated file matches the template.

### Phase 3: Frontend Implementation
- [x] **Task 6 (Frontend Developer):** Refactor `CustomAgentCreator.jsx` to use a multi-step wizard state (e.g., `currentStep` state variable).
- [x] **Task 7 (Frontend Developer):** Build Step 1: Identity (Name, Role, Version).
- [x] **Task 8 (Frontend Developer):** Build Step 2: Rules & Constraints (System rules path, enforcement level, markdown list for constraints).
- [x] **Task 9 (Frontend Developer):** Build Step 3: Capabilities (Markdown list input).
- [x] **Task 10 (Frontend Developer):** Build Step 4: System Prompt & Review (Textarea for prompt, final review, and Submit button).
- [x] **Task 11 (Frontend Developer):** Wire the wizard submission to the updated backend API payload structure.

### Phase 4: QA and Handoff
- [x] **Task 12 (Evidence Collector):** Perform end-to-end testing of the wizard, providing screenshot evidence of each step and the final generated agent file.
- [ ] **Task 13 (Agents Orchestrator):** Review QA findings, finalize the epic, and prepare handoff documentation.
