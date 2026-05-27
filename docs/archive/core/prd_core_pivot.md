# Product Requirements Document: Conversational Core Engine

## 1. Overview
This PRD defines the requirements for the "Conversational Core Engine" of Agency OS. Having established a secure, multi-tenant enterprise foundation, the focus shifts to the primary user experience: creating and executing projects through an intelligent, chat-based interface that orchestrates autonomous agents.

## 2. Goals
- Reduce the friction of starting a new project to zero via natural language input.
- Automate the creation of project documentation (PRDs, Specs, Tasks) from conversational context.
- Seamlessly integrate the conversational interface with the existing multi-agent orchestration pipeline.

## 3. Scope

### 3.1. In Scope
- **Conversational UI:** A persistent, context-aware chat interface for project creation and management.
- **LLM Runner Integration:** Integration with the core LLM backend to process user intent and manage conversational state.
- **Auto-Scoping Engine:** System to generate structured Markdown documents (PRD, Architecture, Tasks) based on chat history.
- **Agent Selection Logic:** Automated mapping of extracted project requirements to available agents in the `/agents` registry.
- **Execution Dashboard:** UI updates to show real-time agent activity initiated from the chat.
- **Custom Specialized Agents:** Ability for users to define and integrate custom agents using the standardized `agency-agents` format.
- **Document-Driven Task Ingestion:** Support for uploading existing documents (PRDs, briefs) to automatically seed the project scoping and execution pipeline.

### 3.2. Out of Scope
- Voice-to-text integration (planned for later).
- Complex 3D visualizations of agent networks.
- Third-party chat integrations (e.g., Slack/Discord bots) for project creation.

## 4. Features & Requirements

### Feature 1: The "Create Project" Chat Flow
- **Req 1.1:** The primary CTA for a new project must immediately open a full-screen or prominent modal chat interface.
- **Req 1.2:** The system must utilize an "Orchestrator" prompt to guide the user through requirement gathering without overwhelming them.
- **Req 1.3:** The chat state must be persistent and saved as a "Draft Project" if the user navigates away.

### Feature 2: Automated Document Generation
- **Req 2.1:** The system must provide a split-screen view allowing users to see the generated PRD/Specs update in real-time as the conversation progresses.
- **Req 2.2:** The generated documents must adhere to standard Agency OS markdown templates.
- **Req 2.3:** Users must be able to edit the generated documents either manually or by requesting changes in the chat.

### Feature 3: Agent Orchestration Integration
- **Req 3.1:** Upon clicking "Execute Project", the system must parse the generated task list and assign appropriate agents.
- **Req 3.2:** The system must create an initial task queue in the orchestrator script (`central_runner.py`).
- **Req 3.3:** The UI must transition from "Planning Mode" to "Execution Mode", displaying the status of the assigned agents.

### Feature 4: Custom Agent Integration
- **Req 4.1:** The system must provide an interface (or configuration path) to define new custom agents.
- **Req 4.2:** Custom agents must be saved and parsed using the `msitarzewski/agency-agents` format for standard interoperability.
- **Req 4.3:** The core pipeline must instantly recognize and assign tasks to newly created custom agents.

### Feature 5: Document Ingestion Pipeline
- **Req 5.1:** Users must be able to upload unstructured or structured documents (PDF, Markdown, text) into the project context.
- **Req 5.2:** The Orchestrator must analyze the uploaded documents and translate them into a structured execution pipeline of tasks.
- **Req 5.3:** Users must be able to review and approve the generated task list before the Nexus Pipeline begins execution.

## 5. Success Metrics
- **Time to First Spec:** Decrease the average time from project initiation to a completed PRD/Task list by 80%.
- **User Engagement:** High percentage of new projects initiated via the chat interface versus traditional form-filling.
- **Agent Execution Success Rate:** Percentage of automatically assigned tasks completed without user intervention.