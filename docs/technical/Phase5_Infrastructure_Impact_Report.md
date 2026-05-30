# Impact Assessment: Phase 5 HITL Feedback Loops

## 1. Hardware Kill Switch Architecture Impact
**Current State:** The `KillSwitch` service relies on `central_runner.py` polling `kill_switch.is_active()` at the start of every topological level execution.
**Impact & Risks:**
* **Blocking Waits:** The introduction of "Paused" and "Awaiting Approval" states in Phase 5 means the DAG execution might block while waiting for user input. If the orchestrator blocks synchronously, it will not poll the Kill Switch during the wait period. 
* **Recommendation:** The wait/polling loop for user approval in `central_runner.py` must continually check the `kill_switch.is_active()` status to ensure a global or tenant-level kill command can immediately terminate a paused pipeline without waiting for the user to click "Approve" or "Reject".
* **State Management:** The kill switch logic must be updated to safely transition a pipeline from `PAUSED` or `AWAITING_APPROVAL` directly to `KILLED_BY_SWITCH`.

## 2. Sandbox Execution Timeouts Impact
**Current State:** `SecureSandbox` (`server/services/sandbox.py`) uses a fixed 10-second `subprocess` timeout for isolated Docker executions.
**Impact & Risks:**
* **Uninterruptible Execution:** If the pipeline is paused or a user intervenes mid-execution via chat ("Skip the DB test"), any code already actively running in the sandbox will continue until it hits the 10-second timeout or completes.
* **Resource Leaks (Orphaned Containers):** If user intervention causes the pipeline to abort or skip the current node while the sandbox is still running, the system must ensure the background Docker container is properly terminated instead of leaving it orphaned to consume resources until its timeout.
* **Recommendation:** If human intervention requires immediately halting the current node, the orchestrator needs a mechanism to signal `SecureSandbox` to kill the underlying `subprocess` and Docker container prematurely, rather than just ignoring its eventual result.

## Conclusion
The HITL pausing mechanisms must be designed as asynchronous wait loops that respect the global Kill Switch, and any active Sandbox executions must be explicitly terminated if a user intervention aborts the current node's context.