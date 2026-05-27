# QA Test/Validation Plan: End-to-Task HITL Workflow Process

## 1. Overview
This document serves as the formal QA validation and evidence collection plan for enforcing the new Five-Phase End-to-Task Workflow, specifically focusing on Phase 4 (QA Gate) and Phase 5 (End of Task Mandate) as defined in `docs/core/prd_workflow_process_update.md`.

## 2. Objective
To establish a strict, repeatable protocol for humans and the Evidence Collector (QA) to validate that agents are strictly adhering to the mandatory sequence:
**Testing Starts -> Docs/Memory Finalization -> Testing Ends/HITL Approval -> Git Workflow Master Handoff**.

## 3. Validation Scope
The QA process will monitor and enforce compliance during the transition from active development (Phase 3) through final handoff (Phase 5).

## 4. Test/Validation Protocol

### 4.1 Phase 4: The QA Gate Validation
Before a task can proceed to finalization, the Evidence Collector must verify:
* **[ ] Automated Test Coverage:** Verify that unit/integration/E2E tests have been written, executed, and passed for the current epic/feature. Evidence: Test suite output logs must be captured.
* **[ ] Human Testing Instructions Generation:** Verify that the agent has explicitly formulated concise, step-by-step instructions for the human operator to perform UAT.
* **[ ] No Premature Completion:** Ensure the agent does NOT invoke the `attempt_completion` tool at this stage.

### 4.2 Phase 5: The End of Task Mandate (Strict Sequence Validation)

The following sequence must be verified in order. If an agent attempts to deviate from this sequence, the Evidence Collector will flag the task for immediate remediation.

#### Step 1: Handoff Documentation & Memory Updates Verification
* **[ ] Changelog Update:** Verify `.roo/memory/changelog.md` contains the latest changes and context.
* **[ ] Active Context Update:** Verify `.roo/memory/active_context.md` reflects the current state of the project.
* **[ ] Documentation Routing:** Verify any new documents were routed to the correct `docs/` subfolder (e.g., `docs/core/`, `docs/technical/`, `docs/operations/`, `docs/qa/`). NO new documents should be in the root `docs/` folder.

#### Step 2: HITL Verification (Formal UAT)
* **[ ] Execution Halt:** Verify the agent explicitly halts operations and prompts the human user.
* **[ ] Prompt Content:** Verify the prompt includes the previously generated Human Testing Instructions.
* **[ ] Explicit Approval:** Collect evidence (chat logs/screenshots) of the human operator explicitly stating approval or providing feedback for iteration.

#### Step 3: Git Workflow Master Handoff Verification
* **[ ] Branch Isolation:** Verify the work was completed on a dedicated feature/epic branch, not `main`.
* **[ ] Git Commit:** Verify a commit was created encapsulating all changes, including the updated documentation and memory files.
* **[ ] Remote Push:** Verify the commit was pushed to the remote repository (`git push`).

## 5. Enforcement & Remediation
* **Tool Call Monitoring:** The Evidence Collector will actively monitor the use of the `update_todo_list` tool to ensure agents are populating the Phase 5 checklist before attempting finalization.
* **Task Rejection:** If the sequence is broken (e.g., a git commit is pushed before HITL approval, or memory is updated after testing ends), the QA gate is considered failed. The agent must revert the out-of-sequence actions and re-execute the protocol in the correct order.

## 6. Sign-off
This document represents the formal QA process for workflow enforcement. All future tasks will be audited against this plan.
