# AgencyOS Product Requirements Document (PRD)

## 1. Introduction
AgencyOS is an orchestration platform designed explicitly for **Service Agencies** to manage, coordinate, and monetize specialized AI agents. This document outlines the requirements for the V1 (MVP) release, reflecting our strategic "Agency First" focus.

## 2. Scope & Objectives
The MVP will focus strictly on delivering value to AI-as-a-Service agencies. Objectives include:
1. Reliable, centralized multi-agent orchestration.
2. Robust multi-tenant client management.
3. End-to-end white-labeling capabilities.
4. Seamless integration with standard agency CRM tools.

## 3. User Personas
### 3.1 The Agency Operator (Admin)
- **Goal:** Manage scalable "AI services" across multiple B2B clients, oversee agent pipelines, and track performance.
- **Pain Points:** Fragmented prompt management, inability to demonstrate clear ROI, lack of centralized workflow monitoring.
- **Needs:** Multi-workspace dashboard, pipeline intervention controls, and white-labeling configuration.

### 3.2 The Agency Client (End-User)
- **Goal:** View progress on deliverables, approve reports, and access generated assets.
- **Pain Points:** Disjointed communication with the agency, lack of transparency on AI-driven tasks.
- **Needs:** A branded, simple portal to review outputs, KPIs, and status updates.

## 4. Epics & Detailed User Stories (MVP Scope)

### Epic 1: Multi-Tenant Client Workspace & Portal
**Description:** Establish isolated environments for each agency client, ensuring secure data handling and contextual agent execution.
- **Story 1.1 - Workspace Creation:** As an Agency Operator, I want to create isolated workspaces for each client, so that client data, API keys, and agent histories do not bleed into one another.
  - *Acceptance Criteria:* Operator can create, edit, and archive workspaces. Each workspace has a unique ID and isolated database schema/partition.
- **Story 1.2 - Context Switching:** As an Agency Operator, I want to seamlessly switch between client workspaces via a dropdown, so that I can manage multiple accounts from a single session.
  - *Acceptance Criteria:* Global context switcher in the top navigation. Selecting a workspace filters all dashboards and pipelines to that specific client context.
- **Story 1.3 - Client Portal Access:** As an Agency Client, I want to log in to a secure portal, so that I can view my project status and access deliverables.
  - *Acceptance Criteria:* Role-based access control (RBAC). Clients have "Read-Only" or "Approver" access restricted exclusively to their assigned workspace.

### Epic 2: Core Multi-Agent Orchestration (NEXUS Pipeline)
**Description:** The engine that executes markdown-defined agent personas, routes tasks, and manages inter-agent handoffs.
- **Story 2.1 - Agent Template Loading:** As the System, I need to parse markdown-based agent personas (e.g., `.md` files in `/agents`), so that I can initialize agents with specific system prompts, tools, and guardrails.
  - *Acceptance Criteria:* Backend parser successfully extracts instructions, role, and constraints from standard agent markdown templates.
- **Story 2.2 - Task Routing & Handoff:** As an Agency Operator, I want to define multi-step workflows where the output of Agent A (e.g., Researcher) automatically feeds into Agent B (e.g., Writer), so that complex tasks are fully automated.
  - *Acceptance Criteria:* Orchestrator supports sequential and parallel execution DAGs (Directed Acyclic Graphs). State is passed reliably between nodes.
- **Story 2.3 - Pipeline Monitoring & Intervention:** As an Agency Operator, I want to see a visual representation of active pipelines and pause/resume them, so that I can intervene if an agent encounters an error or hallucination.
  - *Acceptance Criteria:* Dashboard shows active runs with status indicators (Pending, Running, Paused, Completed, Failed). Operators can manually inject context into a paused run.

### Epic 3: White-Labeling & Branded Reporting
**Description:** Features allowing agencies to present the software and its outputs as their own proprietary technology.
- **Story 3.1 - Brand Configuration:** As an Agency Operator, I want to upload my logo, set a primary hex color, and configure a custom domain, so that the client portal matches my agency's brand identity.
  - *Acceptance Criteria:* Settings page with logo upload (SVG/PNG) and color picker. Application of settings instantly updates the CSS theme for the client-facing portal.
- **Story 3.2 - Automated Report Generation:** As an Agency Operator, I want agents to output their final deliverables into branded PDF or HTML reports, so that I can deliver professional results to clients without manual formatting.
  - *Acceptance Criteria:* Report generation module that takes agent markdown/JSON output, applies the agency's branding template, and exports to PDF.

### Epic 4: Standardized API & Integrations
**Description:** Connecting AgencyOS to the external tools agencies already use.
- **Story 4.1 - LLM Provider Configuration:** As an Agency Operator, I want to securely input API keys for OpenAI and Anthropic, so that the orchestrator can utilize the best model for specific tasks.
  - *Acceptance Criteria:* Secure credential vault in settings. Agents can be configured to use specific models (e.g., `gpt-4o` for logic, `claude-3-opus` for writing).
- **Story 4.2 - CRM Webhook Triggers:** As an Agency Operator, I want to trigger an agent pipeline via an incoming webhook, so that a state change in my CRM (e.g., HubSpot "Deal Won") automatically starts onboarding tasks.
  - *Acceptance Criteria:* System generates unique webhook URLs per pipeline. Payload mapping UI to pass CRM data into the agent's initial prompt.

## 5. Non-Functional Requirements
- **Performance:** UI must reflect real-time updates of agent pipeline execution (sub-2 second latency on status updates via WebSockets).
- **Deployment:** Deployable via Docker (docker-compose) for standardized, cloud-agnostic hosting.
- **Security:** Strict multi-tenant data isolation. Encrypted at rest storage of client-specific LLM/CRM API keys.

## 6. Out of Scope for MVP
- Product-Led Growth (PLG) self-serve onboarding tailored for single indie developers.
- Complex SOC2/Enterprise compliance features (e.g., Active Directory integration, on-premise VPC deployments).
- B2C payment gateways or complex multi-tiered usage billing (Stripe integration is deferred to V2).