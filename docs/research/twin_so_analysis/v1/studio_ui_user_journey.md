# Studio UI User Journey: Natural Language to Agent Configuration

## Overview
This document maps the user journey for the "Studio UI," an interface inspired by Twin.so's strategy of bridging natural language intent with complex backend systems. The Studio UI empowers non-technical users (e.g., Agency Owners, Project Managers) to create, configure, and deploy specialized AI agents simply by describing what they want the agent to do. 

Behind the scenes, the system translates these natural language prompts into structural database configurations (PostgreSQL) and agent routing parameters (YAML).

## User Persona
**The Non-Technical Operator**
*   **Goal**: Wants to automate a specific workflow (e.g., "I need an agent that reviews incoming support tickets, categorizes them by urgency, and drafts a polite response.")
*   **Pain Point**: Does not know how to write YAML, configure PostgreSQL schemas, or set up API routing.
*   **Need**: A conversational, intuitive interface that acts as an "Agent Architect."

---

## The User Journey

### Stage 1: Intent Capture (The Prompt Input)
**User Action:**
1. The user navigates to the "Studio" tab in AgencyOS.
2. They are greeted by a clean, centralized text area: *"What kind of agent would you like to build today?"*
3. The user types a natural language prompt. 
   * *Example:* "Create an agent called 'Lead Qualifier'. It should look at new form submissions, score the lead based on company size, and assign it to the sales pod if the score is over 80."
4. The user clicks **"Generate Agent"**.

**System Background (Invisible to User):**
*   The Orchestrator captures the raw string and routes it to an internal `Agent-Architect-LLM`.
*   The LLM parses the intent, extracting key entities: Agent Name, Role, Triggers, Workflow Logic, and Output definitions.

### Stage 2: Clarification & Scoping (Interactive Feedback)
**User Action:**
1. The Studio UI transitions to a "Building..." state, then presents a visual summary (a card or simple node-map) of what it understood.
2. The system asks 1-2 clarifying questions if necessary: *"What should the Lead Qualifier do if the score is below 80?"*
3. The user replies: *"Just tag it as 'Nurture' and archive it."*
4. The system updates the visual summary in real-time.

**System Background (Invisible to User):**
*   The system refines the initial parsed entities based on the clarification prompt.
*   It begins constructing the JSON/YAML structure in memory.

### Stage 3: Background Translation (The "Twin.so" Engine)
**User Action:**
1. The user clicks **"Finalize & Build"**. They see a polished loading animation indicating that the agent is being configured.

**System Background (Invisible to User):**
*   **YAML Generation**: The system dynamically generates the `agent_base.yaml` equivalent for this specific agent, defining its `system_prompt`, `allowed_tools`, and `routing_rules`.
*   **Database Configuration (PostgreSQL)**: 
    *   Inserts a new record into the `agents` table (name, description, status).
    *   Sets up the necessary relational links in the `agent_capabilities` and `workflow_triggers` tables.
*   **Routing Allocation**: The Orchestrator updates its internal registry to recognize the new "Lead Qualifier" agent, assigning it a dedicated namespace/endpoint for future message routing.

### Stage 4: Validation & Testing (The Sandbox)
**User Action:**
1. The Studio UI presents a "Test Drive" environment.
2. A chat interface allows the user to simulate an input. 
   * *User inputs test data:* "Company size: 500, Industry: Tech."
3. The newly generated agent processes the input and returns the expected output: *"Score: 85. Assigned to Sales Pod."*
4. The user verifies the output matches their expectations.

**System Background (Invisible to User):**
*   The system spins up a temporary instance of the agent using the newly minted YAML and PostgreSQL records.
*   It monitors execution paths to ensure no fallback/error loops occur.

### Stage 5: Deployment & Activation
**User Action:**
1. The user clicks **"Deploy Agent"**.
2. A success modal confirms the agent is live and available in the AgencyOS Marketplace or their specific Workspace pod.
3. The user can now seamlessly invoke this agent in their daily operations.

**System Background (Invisible to User):**
*   The sandbox configuration is committed to the main production schema.
*   The agent is officially registered in the active `.roomodes` or routing tables.
*   An audit log is generated: `"System: Agent 'Lead Qualifier' generated via Studio UI by [User]." `

---

## Technical Outcomes & Success Metrics
*   **Zero-Code Creation**: The user successfully created an agent without touching a single line of code or database query.
*   **Standardized Output**: Despite natural language input, the system output strictly adheres to the established AgencyOS schema (structured YAML + Postgres).
*   **Scalability**: This workflow allows rapid expansion of the AgencyOS agent marketplace through organic, user-driven creation.