# Agency OS Roadmap

This roadmap outlines the strategic plan to build out the Conversational Project Creation and AI Orchestration workflow, progressing into hardening and quality assurance phases.

## Phase 1: The Pivot & UI Overhaul (Completed/Ongoing)
**Goal:** Transition the user interface to be chat-first and integrate the LLM runner for basic conversational scoping.

- **UI Refactoring:** Replace traditional project creation forms with a conversational interface.
- **Settings & Administration Wiring:** Fully functional integration of RBAC, API Keys, Audit Logs, and multi-tenant isolation between the frontend UI and FastAPI backend.
- **LLM Runner Integration:** Connect frontend chat UI to backend LLM engine (OpenAI/Anthropic) via `server.main`.
- **Basic Intent Parsing:** Extract core project details (name, description, tech stack).
- **Split-View Prototyping:** Build UI component to show chat alongside auto-generating documents.

## Phase 2: Automated Scoping & Document Generation
**Goal:** The AI reliably generates comprehensive project plans from conversational context or uploaded documents.

- **Prompt Engineering for Scoping:** Develop specialized prompts for the Orchestrator AI.
- **Document Generators:** Backend services to dynamically generate PRDs, Architecture Specs, and Task Checklists.
- **Document Ingestion Engine:** Allow document uploads (PDF, Markdown) to bypass manual chat and seed the execution pipeline automatically.
- **Iterative Refinement Loop:** Update generated docs in real-time via natural language chat.

## Phase 3: Agent Connection & Orchestration (The Nexus Pipeline)
**Goal:** Bridge plans directly into agent execution, guided by the Nexus Strategy, including dynamic custom agent support.

- **Dynamic Agent Selection:** Map task requirements to specific roles defined in `/agents`.
- **Custom Agent Creator Wizard:** Implement a multi-step React frontend wizard and FastAPI backend to generate robust `agency-agents` compliant files for custom, user-defined agents.
- **Task Queue Translation:** Automatically translate Markdown task lists into actionable DAGs for `central_runner.py`.
- **Execution Visibility:** Update React dashboards to display real-time logs and statuses of running agents.

## Phase 4: Quality Gauntlet & Hardening
**Goal:** The final quality gauntlet to prove production readiness with overwhelming evidence.

- **Evidence Collection:** Comprehensive visual tests, API regression suites, load testing, and compliance checks (WCAG, OWASP, GDPR).
- **Metrics & Review:** Aggregate quality dashboards, risk assessments, and Dev↔QA process efficiency reviews.
- **Infrastructure Validation:** Production environment checks, auto-scaling, monitoring, disaster recovery validation.
- **Final Reality Check:** End-to-end system validation resulting in a Reality-Based Integration Report (READY, NEEDS WORK, NOT READY) ensuring no code goes to `main` without documented proof.

## Phase 5: Feedback Loops & Intervention (Completed)
**Goal:** Allow users to guide and correct agents during the execution phase.

- **Mid-Execution Chat:** Enable users to chat with the Orchestrator *while* agents are working.
- **Approval Gates:** Implement mandatory pause points requiring explicit human approval before agents proceed (e.g., UX -> Dev).
- **Error Escalation:** Automatically alert the user via chat with context and proposed solutions upon agent task failure.

## Phase 6: Iterative Refinements & Advanced Features (Completed)
**Goal:** Polish the experience and add power-user capabilities.

- **Template Library:** Start projects based on pre-defined templates (e.g., "SaaS Starter", "Internal Dashboard").
- **Robust API Selector / Credentials Vault:** Upgrade model selection to include dynamic reasoning effort, model routing, and robust tracking similar to Roo Code.
- **External Tooling Integrations:** Agents automatically provision resources (GitHub repos, Vercel deployments, databases).
- **Voice Interface:** Voice-to-text input for the initial "Napkin Pitch" project scoping phase.