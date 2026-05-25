# Product Requirements Document: Core Engine & Orchestration

## 1. Overview
This consolidated PRD defines the requirements for the "Conversational Core Engine", the "Nexus Pipeline" orchestration, and features for "Custom Agents & Document-Driven Ingestion" within Agency OS. Having established a secure, multi-tenant enterprise foundation, the focus shifts to creating and executing projects through an intelligent, chat-based interface that orchestrates autonomous agents using the `agency-agents` format and automated document ingestion.

## 2. Goals
- Reduce the friction of starting a new project to zero via natural language input and document uploads.
- Automate the creation of project documentation (PRDs, Specs, Tasks) from conversational context or ingested briefs.
- Seamlessly bridge the conversational interface into multi-agent orchestration (The Nexus Pipeline).
- Extend capability dynamically by allowing users to create Custom Specialized Agents via a wizard UI.

## 3. Scope

### 3.1. In Scope
- **Conversational UI:** A persistent, context-aware chat interface for project creation and management.
- **LLM Runner Integration:** Processing user intent, extracting requirements, and managing conversation state.
- **Auto-Scoping & Ingestion Engine:** Generating structured Markdown documents from chat history or parsing uploaded documents (PDF, Markdown, DOCX) into an Execution Pipeline.
- **Nexus Pipeline Orchestration:** Translating Markdown task lists into actionable queues for `central_runner.py`.
- **Dynamic Agent Selection:** Automated mapping of tasks to available agents in the `/agents` registry.
- **Execution Dashboard:** Real-time visibility of agent activity.
- **Custom Agent Creator Wizard:** A multi-step UI wizard and API to define, save, and dynamically inject custom agents into the pipeline.

### 3.2. Out of Scope
- Voice-to-text integration (planned for later).
- Complex 3D visualizations of agent networks.
- Third-party chat integrations (e.g., Slack/Discord bots).

## 4. Features & Requirements

### Feature 1: The "Create Project" Chat Flow
- **Req 1.1:** The primary CTA for a new project must immediately open a full-screen or prominent modal chat interface.
- **Req 1.2:** The system must utilize an "Orchestrator" prompt to guide the user through requirement gathering.
- **Req 1.3:** Chat state must be persistent, saved as a "Draft Project" if the user navigates away.

### Feature 2: Automated Document Generation
- **Req 2.1:** A split-screen view allowing users to navigate via tabs (e.g., Project Details, Draft PRD, Tech Spec, Task List) to see the generated documents update in real-time as the conversation progresses.
- **Req 2.2:** Generated documents must adhere to standard Agency OS markdown templates.
- **Req 2.3:** Users must be able to edit generated documents manually or via chat requests.

### Feature 3: Document Ingestion Pipeline
- **Req 3.1:** Users can upload unstructured/structured docs (PDF, Markdown, TXT) into a project context.
- **Req 3.2:** An Analysis pass (via Orchestrator) translates uploaded documents into a structured execution pipeline of tasks.
- **Req 3.3:** Users must be able to review and approve the generated task list before the Nexus Pipeline begins.

### Feature 4: Agent Orchestration (Nexus Pipeline)
- **Req 4.1:** Upon clicking "Execute Project", the system parses the task list, converting it to a DAG for `central_runner.py`.
- **Req 4.2:** The system dynamically maps tasks to appropriate specialized agents from the registry.
- **Req 4.3:** The UI transitions from "Planning Mode" to "Execution Mode", displaying live logs and statuses.

### Feature 5: Custom Agent Integration (Wizard UI)
- **Req 5.1:** Provide a Multi-Step Wizard UI to define custom agents (Identity, Rules, Capabilities, System Prompt).
- **Req 5.2:** The backend API (`POST /api/v1/custom_agents`) must rigorously validate and export configurations matching the `config/agent_base.yaml` and `agency-agents` standards.
- **Req 5.3:** Newly created custom agents must be instantly available to the Orchestrator for dynamic task assignment without requiring a restart.

## 5. Success Metrics
- **Time to First Spec:** Decrease average time from project initiation to completed PRD by 80%.
- **Engagement vs UI:** High percentage of projects initiated via chat/upload versus manual form-filling.
- **Agent Orchestration Success:** Successful execution of generated task lists by `central_runner.py`.
- **Custom Agent Usage:** High creation and active assignment rates of user-defined custom agents.