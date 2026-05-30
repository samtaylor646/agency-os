# AgencyOS Developer Onboarding & API Guide

Welcome to the AgencyOS Developer Onboarding Guide. This document provides technical teams, integrators, and enterprise architects with the knowledge required to extend the AgencyOS platform, integrate custom agents, and interact with the core orchestration engine via our APIs.

Unlike developer frameworks like AutoGen or CrewAI—which require you to build and host orchestration logic from scratch—AgencyOS provides an enterprise-ready, multi-tenant foundation (complete with RBAC and Audit Logging). As a developer using AgencyOS, your focus is on extending platform capabilities through highly specialized custom agents and integrating our "Conversation to Creation" pipelines directly into your existing enterprise workflows.

---

## 1. Technical Architecture Overview

AgencyOS bridges the gap between high-level human intent and autonomous multi-agent execution.

### The Nexus Pipeline
The core orchestration layer of AgencyOS is the **Nexus Pipeline**. When a project is initiated (via chat or document ingestion), the system's Auto-Scoping engine generates a Product Requirements Document (PRD) and breaks it down into an Execution Pipeline. 

The Nexus Pipeline is responsible for:
*   Routing specific tasks to the most qualified agent.
*   Managing state and context handoffs between multi-disciplinary agents (e.g., passing UX research to a UI design agent, then to a frontend developer agent).
*   Streaming execution updates to the real-time Execution Dashboard.

### Enterprise Foundation
All developer extensions operate within a secure environment:
*   **Multi-Tenancy:** Agents and APIs operate strictly within isolated Workspaces.
*   **RBAC (Role-Based Access Control):** API keys and custom agents adhere to granular permission models.
*   **Audit Logging:** Every API call, agent execution, and state change is logged for enterprise compliance.

---

## 2. Custom Agent Integration

One of AgencyOS's primary differentiators is its dynamic scalability. While the platform includes a No-Code Custom Agent Wizard for standard users, developers can programmatically deploy and integrate complex, stateful custom agents.

### The `agency-agents` Standard
Custom agents must adhere to the `agency-agents` integration standard, allowing seamless interoperability with the Nexus Pipeline.

To register a custom agent programmatically, you define the agent's capabilities, expected inputs, and outputs.

#### Example Agent Payload
```json
{
  "agent_name": "salesforce-data-architect",
  "role": "Salesforce Integration Specialist",
  "description": "Analyzes legacy CRM data and writes Apex triggers for migration.",
  "capabilities": ["data_modeling", "apex_generation", "crm_audit"],
  "input_schema": {
    "type": "object",
    "properties": {
      "legacy_schema_url": { "type": "string" },
      "target_objects": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["legacy_schema_url"]
  },
  "webhook_url": "https://your-infrastructure.com/api/agents/sfdc-architect/execute",
  "auth_token": "bearer_token_for_your_webhook"
}
```

### Execution Flow for Custom External Agents
1.  **Task Assignment:** The Nexus Pipeline identifies that a task requires the `salesforce-data-architect`.
2.  **Webhook Trigger:** AgencyOS sends a secure `POST` request to your agent's `webhook_url` containing the task context and project PRD.
3.  **Execution & Polling:** Your infrastructure processes the task. You can stream progress back to AgencyOS via the Webhook Response API to update the user's Execution Dashboard.
4.  **Completion:** Your agent returns the final artifact (code, report, etc.) to the Nexus Pipeline, which then triggers the next phase of the project.

---

## 3. Core API Extensibility

The AgencyOS REST API allows you to trigger pipelines and manage workspaces externally. All requests require an API key passed in the `Authorization: Bearer <token>` header.

### 3.1. Project & Pipeline APIs

**Initiate a Project via Text**
`POST /api/v1/projects/initiate`
Create a new project by passing conversational intent. The Auto-Scoping engine will automatically begin PRD generation.
*Body:* `{ "workspace_id": "ws_123", "prompt": "Build a React-based CRM dashboard with authentication." }`

**Ingest a Document (PDF/Markdown)**
`POST /api/v1/projects/ingest`
Bypass chat and directly upload unstructured documents (like competitor research or briefs) to generate an actionable Execution Pipeline.
*Body (Multipart/form-data):* `file: <document>`, `workspace_id: "ws_123"`

**Get Pipeline Status**
`GET /api/v1/pipelines/{pipeline_id}/status`
Retrieve the real-time status of all active agents working on a project.

### 3.2. Workspace & Security APIs

**Provision Workspace**
`POST /api/v1/workspaces`
Programmatically create isolated workspaces for new clients or departments.

**Retrieve Audit Logs**
`GET /api/v1/audit-logs?workspace_id=ws_123`
Fetch execution logs, agent assignments, and user actions for security compliance.

---

## 4. Webhooks & Real-Time Events

Developers can subscribe to workspace events to trigger external workflows (e.g., sending a Slack notification when a design agent finishes a mockup).

**Supported Events:**
*   `project.created`
*   `pipeline.phase_started`
*   `agent.task_completed`
*   `project.completed`

Configure your webhook endpoints via the API or the Workspace Settings UI.

---

## 5. Getting Started

1.  **Generate an API Key:** Navigate to **Workspace Settings > API & Integrations** in the AgencyOS UI.
2.  **Review the Postman Collection:** Download our comprehensive API schema [Link to Postman].
3.  **Build Your First Agent:** Use the No-Code Wizard in the UI to understand the agent capabilities, then transition to programmatic deployment using the `agency-agents` standard.

For support, reach out to our Developer Success team or consult the architecture blueprints in `docs/technical/`.
## Architectural Governance & Velocity Toggles

AgencyOS uses dynamic rules to balance fast-paced feature development with rigorous architectural security. By default, development velocity is prioritized. However, before crossing major Phase Gates or introducing massive architectural pivots (like new third-party integrations or billing changes), developers **must** enable the Ecosystem Review Board.

**To toggle the strict governance rules ON or OFF:**
Run the following script in your terminal:
```bash
./scripts/toggle_ecosystem_board.sh
```
*   **When toggled ON:** The orchestrator will automatically summon Legal, Security, and Finance agents to audit any proposed changes before code is written.
*   **When toggled OFF:** Maximum development velocity is restored for daily sprint tasks and bug fixing.

---

## Automated Validation Layer (SOC2 & Quality Control)

To move the system from "hoping the AI behaves" to "mathematically proving it complies", AgencyOS enforces automated guardrails via Git Hooks (for platform development) and Pre-Save Hooks (for autonomous agents operating in user workspaces).

### 1. Marketplace Quality Control (Epic 9)
When deploying a custom agent to the PRPM marketplace (or committing a new agent to the `agents/` directory), an automated Git Hook enforces strict quality control. The `pre-commit` hook scans all modified `.md` or `.yaml` files in the `agents/` directory to ensure they contain:
*   Required YAML frontmatter (Role, Dependencies, Capabilities).
*   Correct IP attributions and safety tags.
*   Valid schema definitions.

### 2. Blast Radius Containment
If an autonomous agent inside AgencyOS writes code or generates artifacts for a user, a built-in pre-save hook acts as a final firewall. It automatically runs security checks, prevents unauthorized root-level modifications, and injects required safety tags before the file is persisted to the user's workspace.

### 3. Auditability for SOC2 Compliance
Every action taken by a multi-agent Pod within AgencyOS is forcefully tagged by the system layer (rather than trusting the AI to tag itself). This guarantees an irrefutable audit log of which AI executed which action, fulfilling enterprise SOC2 requirements.

**Testing the Validation Hooks:**
The validation layer runs automatically on `git commit`. To manually verify the agent metadata, run:
```bash
python scripts/validate_agent_metadata.py
```
