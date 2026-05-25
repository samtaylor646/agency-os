# AgencyOS Roo Memory System

This memory system is used by Roo to maintain context about the AgencyOS project.

## Project Architecture
- **/agents**: Domain-specific agent configurations.
- **/config**: System rules and templates.
- **/scripts**: Execution and validation scripts.
- **/server**: Python-based backend orchestration.
- **/client**: React/Vite-based frontend interface.
- **/docs/core**: The ABSOLUTE SOURCE OF TRUTH containing core pivot documents and strategy.
- **/docs**: Strictly routed document storage. NO files should be created in the root folder.
  - `docs/core/`: Core product requirements, roadmaps, and pivotal strategy.
  - `docs/technical/`: Architecture, API specs, and technical implementations.
  - `docs/operations/`: Operational procedures, git workflows, and maintenance playbooks.
  - `docs/qa/`: Test plans, QA findings, and test scripts.
  - `docs/archive/`: Deprecated or superseded documents.

## Development Principles
- **NEXUS Strategy**: Follow structured pipelines (Phase 0 to Phase 6) with quality gates between phases.
- **Evidence-Based QA**: Ensure all technical implementations are verified with hard evidence (logs, screenshots).
- **Role-Based Execution**: Utilize custom `.roomodes` to execute specific parts of the pipeline appropriately.

## Role Specifics
- Always maintain the operational rules from `.clinerules` and `/config/settings.md`.
- No unsolicited advice per `settings.md`.
- Be objective and clear in all outputs.
- **MEMORY MAINTENANCE**: You MUST reliably track project evolution. At the completion of any Epic, Sprint, or Phase Gate, you are strictly required to update `changelog.md` and `active_context.md` to reflect new deliverables, architectural changes, and forward-looking steps.