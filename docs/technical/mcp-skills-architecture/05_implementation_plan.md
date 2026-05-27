# Session 5: Future Implementation Plan

**Status:** Research / Future Enhancement Backbone
**Topic:** Architectural drafting, peer review, and finalization of the MCP & Upscaler integration roadmap.

---

## Phase 1: The Drafting Panel
**Team:** Backend Architect, DevOps Engineer, Senior Developer

### 🏗️ Backend Architect (The Blueprint)
"To make this a reality, we need to phase the rollout to avoid breaking our current AgencyOS ecosystem. 
*   **Step 1:** Introduce the MCP Client to our `llm_runner.py`. This allows AgencyOS to talk to any MCP server.
*   **Step 2:** Update our `/agents` markdown schema. We add `required_mcp_skills: []` to the frontmatter and build a parser in `document_parser.py` to extract it.
*   **Step 3:** Build the 'Agent Architect' meta-agent. This is the LLM prompt that will power the Upscaler Pipeline."

### ⚙️ DevOps Engineer (Infrastructure)
"If we are running MCP servers and a meta-agent, infrastructure needs to shift.
*   **Skill Hosting:** MCP servers can run locally or remotely. We will need a Dockerized sidecar pattern so each workspace can spin up isolated MCP servers (e.g., a Github MCP container, a Postgres MCP container) without cross-tenant data leakage.
*   **Upscaler Pipeline:** We need an async message queue (Redis/Celery) for the Upscaling. When a user clicks 'Install Agent', it drops a message on the queue. The Upscaler processes the LLM rewrite in the background, then drops the finalized `.md` file into the user's workspace volume."

### 👨‍💻 Senior Developer (The Code Layer)
"I like the async approach. For Step 1 (MCP Client), we should use the official Python MCP SDK. For Step 3 (The Upscaler), the meta-prompt needs to be meticulously crafted. The Upscaler must be instructed *never* to remove existing few-shot examples if they are present, only to add them if the file is bare."

---

## Phase 2: The Review Panel
**Team:** Product Manager, Evidence Collector (QA), Technical Writer

### 👔 Product Manager (User Value)
"The DevOps sidecar pattern is brilliant because it means users can bring their *own* MCP servers later (like a custom internal company database). However, the Upscaler process must have a UI loader. If it's async, the UI needs to say 'Elevating Agent...' so the user doesn't think it froze."

### 🔎 Evidence Collector / QA (Risk Assessment)
"We have a security gate here. If the Upscaler is an LLM, it could hallucinate required skills. What if it assigns the `production_database_drop` skill to a Social Media Agent? 
*   **Mandatory Change:** The Upscaler Pipeline must output the enhanced `agents.md` file in a 'Draft' state. A human user *must* review the YAML frontmatter and click 'Approve Capabilities' before the agent is allowed to execute any MCP skills."

### 📝 Technical Writer (Documentation)
"I will ensure the final documentation clearly delineates 'Core Agents' (our hand-crafted templates) from 'Upscaled Agents' (PRPM downloads). The user must always know the provenance of their agents."

---

## Phase 3: The Finalized Implementation Roadmap (Future Feature)

Based on the panel reviews, here is the finalized, phased roadmap for when AgencyOS is ready to build this:

### Milestone 1: MCP Core Support
1.  Integrate the official Python MCP Client SDK into `server/services/llm_runner.py`.
2.  Deploy two default, containerized MCP Sidecars for testing (e.g., `filesystem_mcp` and `web_search_mcp`).
3.  Update `document_parser.py` to parse the `required_mcp_skills` array from YAML frontmatter.

### Milestone 2: The Upscaler Engine
1.  Write the `agent_architect.md` meta-prompt responsible for analyzing and upgrading basic `agents.md` files.
2.  Build the async background worker (`agent_upgrader_service.py`) to handle the LLM rewriting process without blocking the UI.

### Milestone 3: Security & UI Integration (QA Gate)
1.  Update the AgencyOS UI to show an "Elevating Agent..." loading state during PRPM downloads.
2.  Implement the **Human-in-the-Loop Approval Gate**: Upscaled agents are quarantined in a "Draft" status until the user manually reviews and approves the injected MCP capabilities.

### Milestone 4: DevOps & Scaling
1.  Finalize the Docker Compose / Kubernetes manifests for dynamic MCP sidecar provisioning per workspace.
2.  Open the AgencyOS UI to allow users to connect external, third-party MCP servers via URL.
