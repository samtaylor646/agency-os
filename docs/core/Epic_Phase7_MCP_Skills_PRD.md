# Product Requirements Document (PRD)
## Epic 7: MCP Skills Architecture & Agent Upscaling Pipeline

### 1. Executive Summary
**Objective:** Transform AgencyOS from a passive host of text-based conversational agents into a secure, autonomous ecosystem of action-oriented AI workers by adopting the open Model Context Protocol (MCP) and standardizing the `agents.md` format.

**Value Proposition:** By replacing bespoke tool schemas with the universal MCP standard, AgencyOS can instantly access an ecosystem of capabilities. Furthermore, by introducing an automated "Agent Upscaler," we solve the "Blank Canvas Problem," allowing users to automatically upgrade basic community agents into premium, enterprise-grade autonomous workers with explicitly assigned skills and UI styling.

### 2. Core Features & Requirements

#### 2.1 The Hybrid Agent Format
- **Requirement:** AgencyOS must natively support the standard `agents.md` format downloaded from PRPM without breaking.
- **Progressive Enhancement:** Support YAML frontmatter for UI properties (colors, icons) and MCP capability mapping (`required_mcp_skills`), falling back to default styling if missing.
- **IP Attribution:** Include a `derived_from:` field in the frontmatter to respect open-source licensing.

#### 2.2 Model Context Protocol (MCP) Integration
- **Requirement:** Decouple agent "personas" from "skills".
- **Implementation:** Integrate the official Python MCP Client SDK into `server/services/llm_runner.py`.
- **Infrastructure:** Host MCP servers via a Dockerized "Sidecar Pattern" ensuring skills (e.g., GitHub access, Database querying) are completely isolated per workspace tenant.

#### 2.3 The Agent Upscaler Pipeline (The Moat)
- **Requirement:** An asynchronous meta-agent workflow that upgrades raw `agents.md` files.
- **Functionality:** 
  1. Ingests basic `agents.md` from the marketplace/PRPM.
  2. Synthesizes YAML frontmatter (UI elements).
  3. Injects domain-specific Few-Shot Prompting (code examples/best practices).
  4. Automatically parses the agent's intent and maps it to a list of `required_mcp_skills`.

#### 2.4 UX & Security Gates ("Friction by Design")
- **Requirement:** The UI must safely guide the user through the upscaling process.
- **User Journey:**
  1. Click "Install" -> UI displays an "Installing & Upgrading Agent..." async loader.
  2. Agent lands in a "Draft" status.
  3. **Security Gate:** User is presented with a human-readable permissions modal detailing the assigned MCP skills (e.g., "Read Google Drive"). The user must explicitly tick checkboxes to approve capabilities.

#### 2.5 Security & Compliance Guardrails
- **Kill Switch:** Integration with the existing LLM Kill Switch to immediately sever all MCP sidecar connections in an emergency.
- **Rate Limiting:** Hardcoded limits on MCP tool executions per hour per agent to prevent runaway blast radiuses and massive LLM token billing.
- **Data Privacy:** PII must never be sent to the Upscaler LLM.

### 3. Out of Scope
- Writing custom, bespoke AgencyOS tools (we will rely entirely on the MCP open ecosystem).
- Synchronous UI processing of the Upscaler LLM (must be queued via Redis/background task).

### 4. Metrics & Success Criteria
- **M1:** 100% compatibility with standard `agents.md` files from PRPM.
- **M2:** Successful connection to standard off-the-shelf MCP servers (e.g., filesystem, web_search).
- **M3:** 0 security breaches or runaway loop costs during UAT testing of the Upscaler pipeline.

### 5. Next Steps
- **Review Board:** This PRD must be evaluated by the Backend Architect, UX Architect, and Evidence Collector before technical specifications are drafted.

### 6. Review Board Recommendations

#### UX Architect Review
**Feasibility Sign-Off:** Approved. The technical architecture (Redis async queue and FastAPI polling/WebSockets) fully supports the required user journeys.

**Recommendations for Async Loading States:**
1. **Granular Progress Indication:** To mask the LLM processing time during the Upscaler pipeline, the UI should not use a static spinner. Instead, it should display granular, step-by-step progress updates based on the queue status (e.g., "1. Ingesting base agent...", "2. Synthesizing UI elements...", "3. Mapping MCP capabilities...").
2. **Skeleton States:** While the agent is in the "Draft" state, display a skeleton card in the UI grid to indicate future placement and set visual expectations.
3. **Playful Micro-interactions:** Introduce subtle, brand-aligned animations during the loading phase to keep the user engaged and reduce perceived waiting time.

**Recommendations for the Security Gate ("Friction by Design"):**
1. **Human-Readable Explanations:** The permissions modal must translate technical `required_mcp_skills` into plain, user-friendly language (e.g., converting `postgres_query` to "Access and modify your connected Database").
2. **Progressive Disclosure:** Group skills by risk level. If an agent requires many skills, use collapsible sections to avoid overwhelming the user, ensuring the most critical permissions remain prominent.
3. **Explicit Opt-In:** Ensure checkboxes for permissions are un-ticked by default, forcing the user to actively acknowledge and grant each capability before activation.

#### DevOps Engineer Review
**Feasibility Sign-Off:** Approved. The Docker Sidecar deployment model and Redis async queue are standard, robust patterns for this type of workload.

**Recommendations for Dynamic Provisioning of Sidecars:**
1. **Container Orchestration:** While Docker Compose is sufficient for local development, dynamic provisioning per tenant in production requires an orchestrator like Kubernetes. Use a custom Operator or Helm charts to spin up MCP sidecars on-demand within dedicated tenant namespaces to ensure absolute network isolation.
2. **Resource Quotas & Limits:** Define strict CPU and memory limits for every MCP sidecar container to prevent "Noisy Neighbor" issues where one runaway agent's tool consumes the entire node's resources.
3. **Network Policies:** Implement strict egress/ingress network policies. The sidecars should ONLY be able to communicate with the main AgencyOS LLM Runner over a specific port and have severely restricted outbound internet access based on their specific tool requirement (e.g., a GitHub sidecar only talks to `api.github.com`).
4. **Secrets Management:** Do not pass API keys as environment variables directly in plain text. Integrate a secrets manager (like HashiCorp Vault or AWS Secrets Manager) and inject credentials into the sidecars at runtime or via mounted secure volumes.
5. **Ephemeral Lifecycles:** Implement a TTL (Time-To-Live) for sidecar containers. If an agent hasn't been invoked for a certain period, scale the sidecar down to zero to save compute costs, automatically spinning it back up upon the next invocation request (Cold Start optimization).
#### Evidence Collector (QA) Review
**Feasibility Sign-Off:** Approved. The technical separation between the async queue and the LLM execution environment provides clear boundaries for testability.

**Recommendations for Testing MCP Integrations (Unit Testing):**
1. **Mocking MCP Servers:** To unit test `server/services/llm_runner.py` reliably without requiring actual Docker sidecars, implement mock MCP server interfaces. Use mocking libraries to simulate the Python MCP Client SDK's responses, ensuring you can test tool discovery and simulated RPC call successes/failures (including timeouts and edge-case errors) deterministically.
2. **Contract Testing:** Establish contract tests for the `required_mcp_skills` payload structure. Ensure that the main AgencyOS server and the MCP sidecars agree on the schema of data being passed.
3. **Kill Switch & Rate Limit Validation:** Write specific unit tests that assert the Kill Switch function immediately tears down MCP client sessions, and that rate limiting logic properly raises exceptions when tool execution thresholds are breached.

**Recommendations for E2E Testing the Upscaler Async Queue:**
1. **Redis Queue Integration:** For End-to-End testing, utilize a dedicated test Redis instance (e.g., via testcontainers or a CI service) to fully exercise the asynchronous ingestion, enqueueing, and processing flow.
2. **Deterministic LLM Stubbing:** Do not hit real LLM APIs during E2E pipeline tests to avoid flakiness and costs. Stub the Upscaler LLM responses to consistently return a predefined set of `required_mcp_skills` and UI YAML frontmatter to rigorously verify the parsing and database persistence logic.
3. **Frontend Lifecycle Verification:** Write automated UI tests (using frameworks like Playwright or Cypress) to assert the frontend correctly transitions an agent from "Draft" to "Active" by monitoring API polling or WebSocket events, and critically verify that the Security Gate modal correctly blocks activation until permissions are explicitly ticked.

#### Legal & Compliance Checker Review
**Feasibility Sign-Off:** Approved with mandatory compliance conditions. The architecture provides necessary isolation, but strict data handling and attribution policies must be enforced.

**Recommendations for IP Attribution (PRPM & `agents.md`):**
1. **License Passthrough:** Ensure that the original license type (e.g., MIT, Apache 2.0, GPL) is explicitly parsed and retained in the YAML frontmatter. If an agent is derived from a copyleft license (e.g., GPL), the platform must prominently display these terms to the user to avoid downstream licensing contamination.
2. **Attribution Display:** The UI must display the `derived_from:` field and the original author's attribution visibly within the marketplace and on the agent's detail page, satisfying standard open-source attribution clauses.
3. **Opt-out Mechanism:** Provide a clear mechanism or contact path for original creators to request the removal of their `agents.md` templates from the AgencyOS index if they believe their copyright is infringed (DMCA compliance).

**Recommendations for Data Privacy (GDPR & SOC2 for MCP Sidecars):**
1. **Data Processing Agreements (DPAs):** If an MCP sidecar integrates with a third-party API (e.g., GitHub, Slack, external databases) on behalf of the user, the platform terms of service must clarify that AgencyOS acts as a conduit, and users are responsible for ensuring they have appropriate DPAs in place with those third parties.
2. **Explicit Consent Logs (HITL):** The "Security Gate" (explicit opt-in for MCP skills) is excellent. To meet SOC2 and GDPR compliance, the system must securely log the exact timestamp, user ID, and the specific permissions granted when the checkboxes are ticked. This audit trail is required to prove informed consent.
3. **Data Minimization & PII Scrubbing:** While the Tech Spec notes PII will be stripped from the Upscaler LLM payload, this must be rigorously enforced using a dedicated PII scrubbing library (e.g., Microsoft Presidio) before data is sent to external LLMs. Furthermore, tools executed by the MCP sidecar should only receive the minimum contextual data necessary to perform the action.
4. **Tenant Isolation:** The Docker sidecar pattern with dedicated namespaces and network policies strongly supports SOC2 logical separation requirements. Ensure that no sidecar can write data to a shared volume accessible by another tenant.
