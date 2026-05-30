# Epic PRD: Phase 5 - Feedback Loops & Intervention

## 1. Overview
As outlined in `Roadmap.md`, Agency OS has successfully established its UI, automated scoping, and core Nexus Pipeline orchestration. The next immediate evolutionary step is **Phase 5: Feedback Loops & Intervention**. This epic bridges the gap between full autonomous execution and human oversight, ensuring that complex tasks can be guided, paused, and corrected in real-time by a Human-in-the-Loop (HITL).

## 2. Goals
- Enable bi-directional communication between the user and the active Nexus Pipeline during execution.
- Implement explicit human approval gates at critical phase transitions (e.g., UX -> Dev).
- Build automated error escalation workflows that translate agent failures into actionable user chat prompts.

## 3. Scope

### 3.1. In Scope
- **Mid-Execution Chat Component:** Real-time conversational interface integrated into the `PipelineExecutionViewer` allowing users to send instructions to currently running agents.
- **Approval Gate Checkpoints:** Configuration in the DAG runner (`central_runner.py`) to pause execution and await a definitive UI-based user approval before proceeding to the next node.
- **Error Escalation and Resolution UX:** System-level interception of agent crashes/failures, translated by an orchestrator LLM into a user-friendly error summary and prompt for intervention.
- **Audit Logging for Interventions:** All human interventions and approvals must be logged to the existing Audit system for compliance.

### 3.2. Out of Scope
- Fully automated, self-healing code loops (agents fixing themselves without user input) beyond basic retries.
- Rollback mechanisms to previous DAG states (to be handled in Phase 6).
- Voice-based interventions.

## 4. Key Features & Requirements

### Feature 1: Mid-Execution Chat
- **Req 1.1:** The UI must display an active chat window contextualized to the currently running node in the execution pipeline.
- **Req 1.2:** Users must be able to send text commands ("Change the color to blue", "Skip the DB test") that are injected into the active agent's prompt context on its next iteration loop.
- **Req 1.3:** Agents must explicitly acknowledge the user's intervention in their execution logs.

### Feature 2: Mandatory Approval Gates
- **Req 2.1:** Pipeline definitions must support a `requires_human_approval` boolean on any node/task.
- **Req 2.2:** When a gated node is reached, the UI must transition to an "Awaiting Approval" state, surfacing the output of the previous step for review.
- **Req 2.3:** The user must explicitly click "Approve & Continue" or "Reject & Provide Feedback" to unblock the pipeline.

### Feature 3: Error Escalation Routing
- **Req 3.1:** If an agent exhausts its retry limits or hits a critical exception, the pipeline must pause rather than fail entirely.
- **Req 3.2:** The `central_runner.py` must emit an "escalation" event via WebSockets.
- **Req 3.3:** The UI will present a modal or chat prompt describing the failure in plain English, offering the user choices (e.g., "Provide new API key", "Rewrite prompt", "Abort pipeline").

## 5. Success Metrics
- **Intervention Success Rate:** > 80% of paused pipelines successfully resume after human intervention.
- **User Trust Score:** Increase in qualitative user confidence due to the visibility of approval gates.
- **Error Recovery Time:** Decrease in time spent resolving agent execution failures.

## 6. Development Steps (Kickoff Plan)
1. **Backend Integration:** Update `central_runner.py` and Database schemas to support Paused/Awaiting states and intervention injection.
2. **WebSocket Events:** Add new WebSocket events for `pipeline_paused`, `awaiting_approval`, and `intervention_received`.
3. **Frontend UI Updates:** Modify `PipelineExecutionViewer.jsx` to include the Mid-Execution Chat and Approval Gate modals.
4. **Agent Context Management:** Ensure the `llm_runner.py` can dynamically append human feedback mid-execution without losing core identity instructions.
5. **QA & Evidence Collection:** Test the pipeline with simulated agent failures and verify the escalation routing and resolution workflows. Evidence Collector must sign off before merge.