# Epic Phase 7: MCP Skills & Agent Upscaling Pipeline - Technical Specification

## 1. Overview
This technical specification details the architecture for Epic 7: MCP Skills Architecture & Agent Upscaling Pipeline, transforming AgencyOS into a secure, autonomous ecosystem of action-oriented AI workers using the Model Context Protocol (MCP).

## 2. Architecture Details

### 2.1 Python MCP Client Integration
**Objective:** Enable agents to interact with external tools and services via MCP.
- **Library/SDK:** Official Python MCP Client SDK.
- **Integration Point:** Incorporate into `server/services/llm_runner.py`.
- **Mechanism:** The MCP client will handle discovering tools provided by MCP servers, converting LLM tool calls into MCP RPC calls, and returning results to the LLM context.
- **Authentication/Transport:** Standard Stdio or SSE transport as defined by the MCP specification, interfacing securely with the sidecar containers.
- **State Management:** MCP client sessions will be instantiated per agent invocation, ensuring strict separation of context and capabilities between different agents and workflows.

### 2.2 Docker Sidecar Deployment Model for MCP Servers
**Objective:** Isolate MCP server processes securely per workspace tenant.
- **Architecture:** "Sidecar Pattern" using Docker containers.
- **Implementation:** 
  - Each configured MCP server (e.g., FileSystem, Postgres, GitHub) will run in a dedicated, isolated Docker container alongside the main AgencyOS server containers.
  - The AgencyOS server will communicate with these sidecars over a dedicated internal Docker network using standard protocols (e.g., SSE over HTTP for MCP).
  - **Security:** Sidecars run with minimal privileges. Network access is restricted. The main application uses the LLM Kill Switch to sever connections (e.g., killing the Docker network or specific sidecar containers) during emergencies.
  - **Dynamic Provisioning:** Future iterations will support dynamic provisioning of sidecars when a tenant adds a new integration.

### 2.3 Redis Async Queue for the Upscaler Meta-Agent
**Objective:** Handle the ingestion and upgrading of basic `agents.md` files asynchronously.
- **Architecture:** Message queue using Redis and a background task worker (e.g., Celery or RQ).
- **Workflow:**
  1. **Ingestion Request:** User initiates the installation of an `agents.md` file via the UI.
  2. **Enqueue:** The API enqueues an "upscale_agent" job to Redis and immediately returns a Job ID and a "Draft" status to the client.
  3. **Background Processing:** A dedicated worker consumes the job:
     - Parses the base `agents.md`.
     - Invokes the Upscaler Meta-Agent LLM to generate YAML frontmatter (UI colors, icons), domain-specific few-shot prompting, and `required_mcp_skills`.
     - Persists the upgraded agent definition to the database in a "Pending Approval" state.
  4. **Status Polling/Push:** The frontend polls the job status or receives updates via WebSockets until the upscaling is complete.

### 2.4 FastAPI Routes for UX Security Gates
**Objective:** Expose APIs for the UI to manage the agent lifecycle, specifically the security gating of MCP skills.
- **Endpoints:**
  - `POST /api/agents/import`: Initiates the asynchronous upscaling process. Returns a Job ID.
  - `GET /api/agents/jobs/{job_id}`: Polls the status of the upscaling job.
  - `GET /api/agents/{agent_id}/capabilities`: Retrieves the list of `required_mcp_skills` identified by the Upscaler for a "Draft" agent.
  - `POST /api/agents/{agent_id}/approve`: Accepts a payload of user-approved MCP skills (boolean flags). Transitions the agent from "Draft" to "Active" state.
- **Security Check:** `POST /api/agents/{agent_id}/approve` must strictly validate that the user has authorized the exact permissions required before marking the agent as fully operational. Unapproved skills are stripped from the agent's MCP client configuration.

## 3. Data Flow & Security Guardrails
- **Kill Switch Integration:** When the kill switch is activated, `llm_runner.py` immediately destroys active MCP client instances, and a system call forces termination of running MCP sidecar containers for the affected tenant.
- **Rate Limiting:** Implemented in `llm_runner.py` or an intermediary proxy to track and hard-limit tool executions per hour per agent.
- **Data Privacy:** The payload sent to the Upscaler LLM will strip any user PII.

## 4. Conclusion
This architecture supports the requirements of Epic 7, providing a scalable, secure, and open-standards-based foundation for autonomous agents in AgencyOS.