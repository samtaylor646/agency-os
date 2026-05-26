# Operational Instructions

## Project Structure
* `/agents`: Domain-specific agent configurations.
* `/config`: settings.md (Rules) and agent_base.yaml (Templates).
* `/scripts`: central_runner.py (Orchestrator) and validation_layer.py (Guardrails).

## Operational Rules

1. **Validation**: All task executions must first invoke `validation_layer.py` to check against `settings.md`.
2. **No Unsolicited Advice**: Maintain the strict "No Unsolicited Advice" protocol.
3. **Docker Environment**: When modifying code, always consider the impact on the Docker container environment. NEVER install dependencies directly on the host Mac. Always rely on Docker containers and update the respective requirements/package files instead.
4. **Routing First Mandate**: Before engaging with the user, answering questions, or processing a task, you MUST evaluate the intent and use the `switch_mode` tool to switch to the appropriate specialized agent. Do not attempt to resolve tasks outside your current domain.
5. **Explicit Rule for Agent Roles**: Each task must be assigned to the appropriate specialized agent from the `/agents` directory. Before assigning tasks, you must check the `/agents` folder, and add any needed specialized agents to the `.roomodes` file to ensure the task is handled by the correct specialist.
6. **Documentation Routing Rule**: All new documentation must be routed to the appropriate subfolder within `docs/`. NO new documents should be created in the root `docs/` folder.
   - `docs/core/`: The absolute source of truth containing core product requirements, project roadmaps, and pivotal strategy documents.
   - `docs/technical/`: Architecture documents, API specifications, and technical implementation details.
   - `docs/operations/`: Operational procedures, deployment guides, git workflows, and system maintenance playbooks.
   - `docs/qa/`: Test plans, QA findings, test scripts, and quality assurance evidence.
   - `docs/archive/`: Deprecated or superseded documents.
7. **Memory Maintenance Mandate**: Upon the completion of any Epic, Sprint, or Phase Gate, you MUST update `.roo/memory/changelog.md` and `.roo/memory/active_context.md`. Context loss is strictly prohibited.
8. **Epic Workflow and Handoff Mandate**: When starting work on an Epic, you MUST create a new git branch to ensure we are not building directly in the main branch. Upon the completion of any Epic, a formal handoff process is required. This process must include:
   1. Full documentation updates reflecting the completed epic.
   2. A formal `git commit` encapsulating all changes for the epic on the epic's branch.
   3. Pushing the commit to the remote repository (GitHub commit) via `git push` to ensure the handoff is officially recorded and synchronized.
9. **Strict QA Gate**: No feature branch or phase handoff can be merged into `main` without documented automated tests and a formal sign-off from the Evidence Collector (QA) agent. Code must be proven to work via tests before merging.
