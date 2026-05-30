# Product Exploration: AgencyOS Lite

## Executive Summary

AgencyOS Lite is a proposed standalone, lightweight version of AgencyOS designed specifically for developers, solo founders, and power users who prefer working entirely within their terminal and text editor. It strips away the complex GUI, database overhead, and multi-tenant infrastructure of the Enterprise version in favor of a purely CLI and Markdown-driven approach.

## Core Value Proposition

### 1. Zero Abstraction Tax
Users interact directly with the underlying agent configuration files (Markdown, YAML). There are no web interfaces to click through or forms to fill out. You get raw access to the agent logic, meaning what you write is exactly what executes.

### 2. Ultimate Flexibility
Because the system runs on flat files and CLI commands, it natively integrates with any existing developer toolchain. You can version control your entire agency in Git, use standard diff tools, run it in CI/CD pipelines, and script it using bash or python. 

### 3. Low Maintenance Burden
Without a PostgreSQL database, React frontend, Docker orchestration, or complex API layer, the deployment and maintenance burden approaches zero. It can run locally on a laptop, on a Raspberry Pi, or in a lightweight GitHub Action.

## Target Audience

*   **Solo Developers/Indie Hackers:** Need powerful AI orchestration without the overhead of managing infrastructure.
*   **Power Users & Tinkerers:** Prefer terminals, text editors, and raw file manipulation over web GUIs.
*   **Security-Conscious Teams:** Want 100% local execution or air-gapped environments where code and data never leave their file system.

## Core CLI / Markdown Workflow

1.  **Define:** Users create agents by writing Markdown files in an `agents/` directory (e.g., `agents/copywriter.md`). This file contains the persona, instructions, and constraints.
2.  **Configure:** A simple `agency.yaml` maps the agents to specific tasks or pipelines.
3.  **Execute:** The user runs a command like `agency run pipeline.yaml --input data.txt`.
4.  **Review:** Output is piped directly to the terminal or saved as new Markdown files, ready to be committed or further processed.

## AgencyOS Lite vs. Enterprise AgencyOS

| Feature | AgencyOS Lite | Enterprise AgencyOS |
| :--- | :--- | :--- |
| **Interface** | CLI, Markdown, Text Editor | Web UI, Dashboards, Visual Builders |
| **Data Storage** | Local File System (Markdown/YAML) | Relational Database (PostgreSQL) |
| **User Base** | Single User / Local Environment | Multi-tenant, Enterprise Teams |
| **Infrastructure** | Standalone Executable / Script | Docker, Kubernetes, Cloud Services |
| **Access Control** | OS-level File Permissions | Advanced RBAC, Audit Logging |
| **Best For** | Prototyping, Local Scripts, CI/CD | Enterprise Workflows, Collaborative Teams |

## Strategic Conclusion

AgencyOS Lite serves as both an entry-level product to capture mindshare among developers and a highly efficient tool for internal use. It validates the core orchestration logic without the UI/UX overhead.

## The Architectural Reality: Combining `agency-agents` and `AGENT-ZERO`

The true vision for AgencyOS Lite is realized by directly combining two specific, highly focused paradigms: the static configuration of `agency-agents` and the dynamic execution engine of `AGENT-ZERO`. When merged, these two concepts create the perfect, lightweight CLI workflow.

### 1. Feeding Static Personas into the Dynamic Engine

The `agency-agents` repository excels at defining specialized, domain-specific personas through simple, static Markdown and YAML files (e.g., `design-brand-guardian.md`, `qa-engineer.yaml`). These files contain pure instructions, constraints, and system prompts. 

In the Lite architecture, these static files act as the "cartridges." The `AGENT-ZERO` execution engine acts as the "console." When a task is initiated, the Lite orchestrator simply reads the static file from `agency-agents`, parses the system prompt and constraints, and injects them directly into the context window of `AGENT-ZERO`'s LLM call. The engine doesn't need a database to know *who* it is acting as; it just assumes the identity dictated by the flat file currently loaded into memory.

### 2. The Core Loop: Orchestrator, Memory Bank, and Persona Swapping

The power of this combination lies in the execution loop managed by the orchestrator (the core logic from `AGENT-ZERO`):

1.  **State Machine:** The orchestrator maintains a simple state machine tracking the current task, sub-tasks, and required approvals.
2.  **Memory Bank Injection:** As the loop runs, the orchestrator continuously updates and reads from a flat-file "Memory Bank" (e.g., `active_context.md`, `changelog.md`). This provides continuity across the session.
3.  **Dynamic Swapping:** When the state machine determines that a different domain expertise is required (e.g., moving from code generation to code review), the orchestrator drops the current persona context. It then loads the next required static file from the `agency-agents` directory, prepends the accumulated context from the Memory Bank, and executes the next step. 

The `AGENT-ZERO` engine is essentially rebooted with a new personality (from `agency-agents`) but retains the shared project memory, allowing for complex, multi-agent workflows without heavy infrastructure.

### 3. The Definition of AgencyOS Lite

This pure combination *is* the exact definition of AgencyOS Lite. By relying on flat files (`agency-agents`) for configuration and a raw script (`AGENT-ZERO`) for the execution loop, we eliminate the need for a web server, a database, or a complex UI. 

It represents the raw CLI workflow: a developer types a command, the orchestrator pulls the necessary persona files, runs the execution loop against the local filesystem, writes the results back to text files, and exits. It is the minimal viable architecture for sophisticated, multi-agent orchestration.