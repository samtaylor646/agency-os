# Phase 5: Feedback Loops & Intervention Architecture

This document outlines the technical design for the Phase 5 "Feedback Loops & Intervention" features, specifically detailing how the `central_runner.py` (DAG orchestrator) will handle execution pauses, human approvals, error escalations, and the corresponding WebSocket architecture for the UI.

## 1. Core Concepts

The goal is to transition the DAG orchestrator from a "fire-and-forget" execution model to an interactive, stateful model that can pause, wait for human input, and resume with modified context.

We are introducing three new node states:
*   `PAUSED_AWAITING_APPROVAL`: The node requires human sign-off before proceeding.
*   `PAUSED_ERROR_ESCALATION`: The node has encountered a terminal/retried error and is awaiting human intervention to resolve.
*   `INTERVENED`: A transient state indicating new context/instructions have been received and the node should be re-run or the pipeline unblocked.

## 2. DAG Runner Modifications (`central_runner.py`)

### 2.1 Node Definition Updates
The `DAGNodeInput` and the internal `DAGOrchestrator.nodes` dictionary will be extended to support a `requires_human_approval` boolean flag.

```python
# In central_runner.py / server.schemas
class DAGNodeInput(BaseModel):
    task: str
    context_data: dict
    tenant_id: str
    requires_human_approval: bool = False
```

### 2.2 Pausing Execution (Approval Gates)
When the orchestrator processes a level in the topological sort, it will check the `requires_human_approval` flag.

1.  **Execution:** The node executes its task normally via `execute_node_with_retry`.
2.  **Pause Trigger:** If `requires_human_approval` is True, instead of marking the node as `COMPLETED` and moving to the next level, the runner changes the node's status to `PAUSED_AWAITING_APPROVAL`.
3.  **State Persistence:** The orchestrator persists the `PAUSED` state to the `WorkflowExecution` database record.
4.  **Event Emission:** The runner uses `message_broker` to publish an `awaiting_approval` event.
5.  **Yielding Execution:** The runner must yield control. Instead of blocking the thread actively, the `DAGOrchestrator.execute_workflow` method will need to implement a polling mechanism or subscribe to an `asyncio.Event` tied to the specific node ID to wait for the unblock signal.

### 2.3 Error Escalation Handling
If `execute_node_with_retry` exhausts its retry attempts (throwing a `TerminalNodeError` or unresolved `TransientNodeError`), the orchestrator catches this.

1.  **Pause Trigger:** Instead of immediately failing the workflow, the runner sets the node status to `PAUSED_ERROR_ESCALATION`.
2.  **Event Emission:** Publishes a `pipeline_paused` and `error_escalation` event via the `message_broker` containing the error details.
3.  **Yielding:** Similar to the approval gate, the runner waits for intervention.

### 2.4 Resuming Execution
When a user provides feedback (via UI to REST/WebSocket):
1.  **State Update:** The node's state is updated in the database to include the new human context (e.g., appended to `context_data`).
2.  **Unblocking:** The pending `asyncio.Event` inside `execute_workflow` is set, or the polling loop detects the `INTERVENTION_RECEIVED` status.
3.  **Re-Execution or Continuation:** 
    *   If it was an Approval Gate: The node status becomes `COMPLETED` and the DAG continues to the next level.
    *   If it was an Error Escalation / Mid-Execution Chat: The node is re-executed (`execute_node_with_retry` called again) with the newly injected user prompt appended to the task or context.

## 3. WebSocket Architecture (`websockets.py`)

Currently, `server/routers/websockets.py` only forwards messages from Redis (via `message_broker`) to the client. It needs to support bi-directional communication to handle user interventions in real-time.

### 3.1 Client-to-Server Events
The `websocket_endpoint` will be updated to actively parse incoming JSON payloads from the client:

```python
# Incoming Message Structure from Client
{
    "type": "intervention", # or "approve", "reject"
    "node_id": "node_123",
    "workflow_id": "wf_abc",
    "action": "approve_and_continue", 
    "payload": {
        "user_prompt": "Change the background to red." # Optional
    }
}
```

### 3.2 Handling Incoming Interventions
When the WebSocket receives an intervention message:
1.  **Validation:** Verify the user has permissions for the workspace/workflow.
2.  **Database Update:** Update the `WorkflowExecution` record to reflect the human input. 
3.  **Internal Pub/Sub:** Publish an internal event via `message_broker` (e.g., `intervention_received:{workflow_id}:{node_id}`) so the sleeping/waiting `central_runner.py` task can wake up.
4.  **Audit Logging:** Log the intervention to the Audit system (e.g., via `server.audit`).

### 3.3 Server-to-Client Events (Outbound)
The `central_runner.py` will emit the following new event types via `message_broker.publish()`, which the WebSocket will forward to the UI:

*   `pipeline_paused`: Emitted when the runner stops progressing.
*   `awaiting_approval`: Emitted specifically for gated nodes. Payload includes the output of the node that requires review.
*   `error_escalation`: Emitted when an agent fails. Payload includes error details and suggested recovery actions formatted by the LLM orchestrator.
*   `intervention_acknowledged`: Sent back to the client confirming the runner has received the input and is resuming.

## 4. State Management and Robustness

### 4.1 Zombie Prevention
Because pipelines can now pause indefinitely awaiting human input, a cleanup job or TTL mechanism should be implemented for long-running workflows to prevent memory leaks in the active runner processes. Alternatively, the orchestrator should be fully stateless, capable of completely shutting down and "resuming" a workflow from the database state when a webhook/intervention is received.

For Phase 5 MVP, holding the `asyncio` task open with a reasonable timeout (e.g., 24 hours), or switching the `execute_workflow` to a state-machine that can be re-invoked, is recommended. A state-machine approach is more robust:
If a node hits a pause state, `execute_workflow` saves state and *exits*. When an intervention API call is made, `execute_workflow` is called again, loads the state from the DB, sees the node is now unblocked, and continues processing the topological sort.

### 4.2 Agent Context Modification
When a user provides text via Mid-Execution Chat or Error Escalation, it will be injected into the `context_data` under a specific key (e.g., `HUMAN_INTERVENTION`). The `llm_runner.py` must be updated to explicitly prioritize instructions found under this key over its default instructions to ensure the agent obeys the override.