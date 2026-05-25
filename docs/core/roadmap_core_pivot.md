# Agency OS Roadmap: Core Engine Pivot

This roadmap outlines the strategic pivot to prioritize the Conversational Project Creation and AI Orchestration workflow, building upon the existing enterprise foundation.

## Phase 1: The Pivot & UI Overhaul (Immediate Next Steps)
**Goal:** Transition the user interface to be chat-first and integrate the LLM runner for basic conversational scoping.

- **UI Refactoring:** Replace traditional project creation forms with a conversational interface.
- **LLM Runner Integration:** Connect the frontend chat UI to the backend LLM engine (e.g., OpenAI/Anthropic APIs) via `server.main`.
- **Basic Intent Parsing:** Implement logic to extract core project details (name, description, tech stack) from the chat.
- **Split-View Prototyping:** Build the UI component to show chat alongside auto-generating markdown documents.

## Phase 2: Automated Scoping & Document Generation
**Goal:** The AI reliably generates comprehensive project plans from the conversational context.

- **Prompt Engineering for Scoping:** Develop specialized prompts for the Orchestrator AI to ask the right clarifying questions.
- **Document Generators:** Implement backend services to dynamically generate PRDs, Architecture Specs, and Task Checklists based on user input.
- **Document Ingestion Engine:** Allow users to bypass chat generation by uploading existing specs/PRDs to automatically seed the execution pipeline.
- **Iterative Refinement Loop:** Allow users to request changes to generated docs via natural language, updating the docs in real-time.

## Phase 3: Agent Connection & Orchestration (The Nexus Pipeline)
**Goal:** Bridge the generated plans directly into agent execution, guided by the [Nexus Strategy](../../agents/strategy/nexus-strategy.md).

- **Dynamic Agent Selection:** Implement logic to map task requirements to the specific roles defined in the `/agents` directory.
- **Custom Agent Support (`agency-agents` format):** Build parsing and creation tools to allow users to plug in custom, specialized agents seamlessly.
- **Task Queue Generation:** Automatically translate the generated Markdown task list into actionable items for `central_runner.py`.
- **Execution Visibility:** Update the frontend Dashboard to display real-time logs and statuses of agents working on the newly created project.

## Phase 4: Feedback Loops & Intervention
**Goal:** Allow users to guide and correct agents during the execution phase.

- **Mid-Execution Chat:** Enable users to chat with the Orchestrator *while* agents are working to change priorities or clarify requirements.
- **Approval Gates:** Implement pause points where agents require explicit user approval before proceeding to the next major phase (e.g., approving UX before starting Frontend development).
- **Error Handling & Escalation:** If an agent fails a task, the Orchestrator automatically alerts the user via chat with context and proposed solutions.

## Phase 5: Iterative Refinements & Advanced Features
**Goal:** Polish the experience and add power-user capabilities.

- **Template Library:** Allow users to start conversations based on pre-defined project templates (e.g., "E-commerce MVP", "Internal Dashboard").
- **External Tooling Integrations:** Enable agents to automatically provision resources (e.g., GitHub repos, Vercel deployments) as part of the execution pipeline.
- **Voice Interface:** Introduce voice-to-text for the initial "Napkin Pitch" phase.