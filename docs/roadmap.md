# AgencyOS MVP Roadmap & Prioritization

As a platform designed for Service Agencies, the order of execution is critical to ensure a scalable, secure, and logical build process. 

## Prioritization Rationale

While the AI "Engine" (NEXUS Pipeline) is the core value proposition, it cannot operate securely in a B2B agency context without strict data isolation. If we build the engine first, we risk architectural debt when retrofitting multi-tenancy. Therefore, we must build the **Foundation (Workspaces)** first, followed by the **Engine (Agents)**, then the **Presentation (White-labeling)**, and finally the **Connectivity (APIs)**.

---

### Phase 1: Foundation (Epic 1 - Multi-Tenant Workspace & Client Portal)
**Status:** Up Next
**Goal:** Establish secure, isolated environments for agency clients.
**Key Milestones:**
1. Database schema with tenant ID partitioning.
2. Role-Based Access Control (RBAC) for Agency Admins vs. Clients.
3. Workspace CRUD operations and UI context switching.

### Phase 2: The Engine (Epic 2 - Core Multi-Agent Orchestration)
**Status:** Backlog
**Goal:** Build the NEXUS pipeline to run agents securely within the established tenant contexts.
**Key Milestones:**
1. Markdown-based agent template parser.
2. Directed Acyclic Graph (DAG) task routing.
3. Pipeline execution and monitoring dashboard.

### Phase 3: Presentation (Epic 3 - White-Labeling & Branded Reporting)
**Status:** Backlog
**Goal:** Allow agencies to brand the Phase 1 portal and Phase 2 outputs.
**Key Milestones:**
1. Custom branding settings (Logo, Colors, Domain).
2. Automated PDF/HTML report generation from agent outputs.

### Phase 4: Connectivity (Epic 4 - Standardized API & Integrations)
**Status:** Backlog
**Goal:** Connect the platform to existing agency workflows.
**Key Milestones:**
1. Secure LLM provider credential vault.
2. CRM webhook triggers (e.g., HubSpot, Salesforce).
