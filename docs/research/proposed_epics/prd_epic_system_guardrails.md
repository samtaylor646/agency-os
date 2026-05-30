# PRD: System-Enforced Guardrails Epic

## 1. Executive Summary
This Epic focuses on implementing strict, system-level guardrails across AgencyOS to ensure that all automated and agentic actions adhere strictly to organizational rules and user intents. It transitions our operational guidelines (e.g., as defined in `.clinerules` and `settings.md`) from "suggested best practices" to **hard-coded, system-enforced constraints**.

## 2. Objectives
- **Mandatory Routing Validation:** Enforce the ROUTING FIRST MANDATE. Prevent agents from executing tasks outside of their specialized domain.
- **Validation Layer Integration:** Ensure all task executions invoke `scripts/validation_layer.py` to check against global constraints (`config/settings.md`).
- **Human-in-the-Loop (HITL) Enforcement:** Programmatically pause workflows to require explicit human consent before major phase transitions, code merges, or sensitive operations.
- **Orchestrator Isolation:** Strictly forbid the `agents-orchestrator` mode from executing file modifications directly. Limit its tools to `new_task` and `switch_mode`.
- **Ecosystem Review Board Trigger:** Automate the halting of major phase gates to synthesize a compliance, security, and financial audit before proceeding.

## 3. Scope
**In Scope:**
- Enhancement of `scripts/validation_layer.py` to include strict routing and domain checking.
- Updates to `server/services/orchestrator_service.py` and `server/services/task_router.py` to enforce the Orchestrator Isolation Mandate.
- Middleware implementations (`server/core/validation_middleware.py`) to block unauthorized file writes or tool executions by the Orchestrator.
- Git hook or pipeline enforcement for the STRICT QA GATE (preventing merges without Evidence Collector QA sign-off).
- Implementation of the `toggle_ecosystem_board.sh` logic to intercept Phase Gate transitions.

**Out of Scope:**
- Creation of new specialized agents (handled in separate Epics).
- Complete rewrite of the existing database layer.

## 4. Technical Requirements
- **Validation Middleware:** Introduce a robust interceptor that evaluates the current `agent_mode` against the requested `tool_call`. If the Orchestrator attempts a `write_to_file` or `execute_command` (other than structural scripts), it must immediately raise a `DomainViolationError`.
- **HITL Checkpoints:** API routes managing Phase Gates (`server/routers/projects.py` or similar) must require an `approved_by_human` boolean flag and an associated `user_id` for progression.
- **Agent Roles Verification:** Before routing, the system must parse `.roomodes` and the `/agents` directory to ensure the target specialized mode exists and is correctly configured.

## 5. Success Metrics
- **0% Violation Rate:** Number of times the Orchestrator directly modifies application code drops to zero.
- **100% Routing Accuracy:** All tasks are handled by explicitly designated specialized agents.
- **HITL Compliance:** 100% of Epic completions and Phase Gate transitions have a logged human approval timestamp.

## 6. Milestones
- **Milestone 1:** Middleware implementation for Orchestrator Isolation and Tool Restriction.
- **Milestone 2:** Hardening of `validation_layer.py` and integration into all task execution paths.
- **Milestone 3:** Implementation of Automated QA Gates and Phase Gate HITL checkpoints.
- **Milestone 4:** Full system end-to-end testing of the guardrails by intentionally violating them and ensuring proper error handling.

## 7. Next Steps
1. The Backend Architect will review this PRD and begin implementing Milestone 1 (Orchestrator Isolation Middleware).
2. Human user to approve the PRD.