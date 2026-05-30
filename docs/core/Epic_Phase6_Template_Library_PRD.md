# Epic PRD: Phase 6 - Template Library & API Selector

## 1. Overview
Following the successful implementation of the Nexus Refactor (Phase 4) and Feedback Loops (Phase 5), the Agency OS platform is now highly scalable and capable of robust human-in-the-loop intervention. **Phase 6** shifts the focus to "Operate & Evolve" by introducing the **Template Library and API Selector**. This Epic will empower users to save proven, customized agent workflows as reusable templates and dynamically select the optimal LLM provider (API) for each task based on cost, complexity, and compliance requirements.

## 2. Goals
- Provide users with a centralized library to save, discover, and reuse successful multi-agent DAG configurations (Pods/Teams).
- Implement a flexible API Selector allowing granular control over which underlying LLM provider powers specific agents or workflows.
- Enhance operational efficiency by reducing the setup time for repetitive tasks and optimizing inference costs.
- Implement workflow state rollback mechanisms to revert to previous execution nodes.

## 3. Scope

### 3.1. In Scope
- **Template Library UI/UX:** A new frontend marketplace/library interface (`TemplateLibrary.jsx`) to browse, preview, and instantiate saved workflows.
- **Template Data Model:** Backend database schema updates to serialize and store complete DAG configurations, prompts, and team structures as reusable templates.
- **Dynamic API Selector:** Frontend UI in the `CustomAgentCreator` and `WorkspaceSettingsModals` to select preferred LLM providers (e.g., OpenAI, Anthropic, Gemini, Local Models) on a per-agent or per-workspace level.
- **Provider Routing Layer:** Backend updates to `llm_runner.py` and `api_server.py` to route API requests dynamically based on the selected provider configuration.
- **State Rollbacks:** Add capabilities to the `central_runner.py` and `state_manager.py` to allow users to revert pipeline execution to a previously completed node.

### 3.2. Out of Scope
- Direct monetization or billing for premium templates (planned for future marketplace iteration).
- Full bring-your-own-model (BYOM) fine-tuning pipelines.
- Multi-cloud infrastructure provisioning for deployed templates.

## 4. Key Features & Requirements

### Feature 1: The Template Library
- **Req 1.1:** Users must be able to click a "Save as Template" button on any completed or configured pipeline execution.
- **Req 1.2:** The system must serialize the entire DAG, including agent definitions, system prompts, and task routing logic, into a standard JSON/YAML format.
- **Req 1.3:** The UI must provide a gallery view of available templates (both personal and system-provided defaults) with descriptions, complexity ratings, and required API capabilities.

### Feature 2: Dynamic API Selector
- **Req 2.1:** Users must be able to configure API credentials for multiple supported providers within the `CredentialsManager`.
- **Req 2.2:** When defining an agent or launching a template, users must be presented with a dropdown to select the `LLM_PROVIDER` (e.g., GPT-4, Claude 3.5 Sonnet, Gemini 1.5 Pro).
- **Req 2.3:** The backend `llm_runner.py` must gracefully handle the formatting and routing differences between the respective LLM APIs.
- **Req 2.4:** Fallback routing: If a selected API fails or times out, the system should ideally fallback to an alternative provider if configured.

### Feature 3: Workflow State Rollbacks
- **Req 3.1:** While a pipeline is paused (via Phase 5 intervention) or after a failure, the UI must display a "Rollback to Node X" option.
- **Req 3.2:** The `central_runner` must cleanly revert the state matrix, dropping downstream context, and restart execution from the targeted node.

## 5. Success Metrics
- **Template Utilization:** > 40% of new workflows initiated are derived from saved templates within the first month.
- **API Diversity:** Successful routing of API requests across at least 3 different provider backends.
- **Rollback Success Rate:** > 90% of initiated rollbacks successfully resume without context corruption.

## 6. Development Kickoff Plan
1. **Epic Branching & Architecture:** Architect the database schema changes for Templates and the Provider Routing Layer (`docs/technical/Phase6_Template_Architecture.md`).
2. **Backend Foundation:** Update schemas, routing logic in `llm_runner.py`, and rollback mechanisms in `state_manager.py`.
3. **Frontend Implementation:** Build the `TemplateLibrary.jsx`, update the `CustomAgentCreator` with the API Selector, and integrate rollback UI.
4. **QA & UAT:** Extensive testing of dynamic API routing, template instantiation integrity, and rollback stability.

---
**Prepared By:** Product Manager
**Status:** Ready for Technical Architecture Review