# Product Requirements Document (PRD): Custom Agents & Document-Driven Pipelines

## 1. Overview
AgencyOS is evolving to empower users to define their own specialized agents and seamlessly ingest unstructured documentation to generate structured execution pipelines. This PRD outlines two core features:
1. **Custom Specialized Agents (Agency-Agents Format Compatibility)**
2. **Document-Driven Task Ingestion & Pipeline Generation**

## 2. Goals & Objectives
* **Extensibility:** Allow users to create custom agents (e.g., Salesforce/WordPress experts) without waiting for official releases.
* **Standardization:** Adopt the format used by `msitarzewski/agency-agents` to ensure community interoperability.
* **Efficiency:** Reduce the friction of starting projects by automatically converting uploaded documents (PRDs, briefs) into actionable tasks in the execution pipeline.

## 3. Features & Requirements

### 3.1 Custom Specialized Agent Creator
* **Description:** A UI and API mechanism to define new agent personas and capabilities.
* **Requirements:**
  * Users can specify agent Name, Role, Goal, Backstory, Capabilities, and Tools.
  * System must export/save the agent configuration matching the markdown/YAML format of `agency-agents`.
  * Custom agents must be immediately available to the central runner (`central_runner.py`) for task assignment.
  * *Update (Completed):* Exact YAML generation ensures strict schema adherence required by the engine, including robust error handling for user inputs to prevent malformed configurations.
  * *Example Use Case:* A user needs a niche CMS expert (e.g., Ghost or Webflow). They use the creator to define the rules, and the agent is added to their workspace.

### 3.2 Document-Driven Task Pipeline
* **Description:** The ability to create a new project/epic by uploading existing files.
* **Requirements:**
  * Support file uploads (PDF, Markdown, TXT, DOCX) to a Project Workspace.
  * Introduce an "Analysis Agent" (or utilize the Orchestrator) to review ingested documents.
  * System must parse the documents and automatically generate a structured task list (Execution Pipeline).
  * Users can review, edit, and approve the generated tasks before execution begins.
  * *Example Use Case:* A user uploads a 10-page PRD. The system extracts the features, breaks them into epics, and assigns them to the appropriate specialized agents (Frontend, Backend, QA).

## 4. Success Metrics
* Number of custom agents created per user.
* Percentage of projects initiated via document ingestion vs. manual task creation.
* Time saved from project creation to first task execution.

## 5. Next Steps
1. **Architecture Review:** Hand off to the Architect to design the `agency-agents` parser and the document ingestion pipeline.
2. **UI/UX Design:** Draft the user interface for the Agent Creator and Document Upload modules.
3. **Implementation:** Update `/agents` structure, `central_runner.py`, and client interface.
