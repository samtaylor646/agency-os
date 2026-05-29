# Phase 5 Feedback Loops PRD: Risk Assessment & North Star Drift Report

## 1. Overview
This document consolidates the technical risk assessment of the `docs/core/Epic_Phase5_Feedback_Loops_PRD.md`. It incorporates architectural findings related to WebSockets and Redis, infrastructure considerations regarding the LLM Kill Switch and Secure Sandbox, and QA implications for End-to-End (E2E) testing.

## 2. North Star Drift Analysis
**Conclusion: The Phase 5 PRD DOES NOT drift from the North Star vision, but it introduces architectural complexity that must be carefully managed to avoid critical breakages.**

The "North Star" of AgencyOS is to provide an autonomous, scalable, and safe multi-agent orchestration platform (NEXUS) with strong Human-in-the-Loop (HITL) oversight. 
The Phase 5 PRD explicitly builds toward this by adding mandatory approval gates and mid-execution chat interventions. However, the *implementation details* introduce risks to the existing deterministic, asynchronous pipeline architecture. 

## 3. Technical Findings & Risk Assessment

### 3.1. WebSockets & Redis Integration
*   **Current State:** AgencyOS relies on Redis Pub/Sub (`message_broker.py`) for inter-agent communication and WebSockets (`server/routers/websockets.py`) to stream real-time updates to the React frontend.
*   **Phase 5 Impact:** The PRD requires emitting "escalation" and "pipeline_paused" events via WebSockets, and injecting user feedback ("intervention_received") into an active, running DAG.
*   **Risks:**
    *   **State Management:** Transitioning a running async pipeline into a "Paused/Awaiting" state across distributed workers introduces a high risk of race conditions. Redis must be used to reliably track and broadcast the exact pause state across all API nodes.
    *   **Connection Drops:** If a WebSocket connection drops while a pipeline is waiting for human approval, the system must retain the pending approval state durably (in PostgreSQL) so the user can resume upon reconnection. 

### 3.2. Infrastructure Impact (Kill Switch & Sandbox)
*(Sourced from `docs/technical/Phase5_Infrastructure_Impact_Report.md`)*
*   **Hardware Kill Switch:** 
    *   **Risk:** The orchestrator currently polls the kill switch flag between topological levels. If `central_runner.py` blocks synchronously waiting for user approval, it will fail to poll the kill switch. A rogue or stalled pipeline cannot be terminated during an approval wait.
    *   **Mitigation:** Wait loops must be asynchronous and continuously poll `kill_switch.is_active()`, transitioning from `AWAITING_APPROVAL` to `KILLED_BY_SWITCH` if triggered.
*   **Sandbox Timeouts:** 
    *   **Risk:** The Secure Sandbox currently uses a fixed 10-second `subprocess` timeout. Mid-execution user interventions that abort or skip nodes will leave orphaned Docker containers running in the background until they time out.
    *   **Mitigation:** `central_runner.py` must signal `SecureSandbox` to explicitly kill the underlying `subprocess` and Docker container upon an intervention abort.

### 3.3. E2E Testing Impact (Evidence Collector Findings)
*(Sourced from `docs/qa/Automated_Testing_Standards.md` and related E2E specs)*
*   **Current State:** Strict QA gates require 100% pass rates for integration tests and comprehensive E2E tests before merging.
*   **Phase 5 Impact:** The introduction of paused states and asynchronous human intervention shatters the current deterministic nature of the automated E2E testing suite.
*   **Risks:**
    *   **Test Timeouts:** Automated E2E tests (e.g., Playwright) running against the UI will hang when the DAG hits an Approval Gate unless the test harness is explicitly updated to simulate human clicks or API approvals.
    *   **Mocking Complexity:** Mocking the bi-directional chat intervention mid-pipeline requires sophisticated asynchronous test fixtures that can inject events via WebSockets while the DAG is suspended.
    *   **Mitigation:** The Evidence Collector must update `tests/e2e/test_pod_lifecycle.py` and the UI test suite to explicitly handle `PAUSED` and `AWAITING_APPROVAL` states, providing simulated inputs to unblock the pipeline during CI runs.

## 4. Final Recommendation
Proceed with Phase 5, but update the PRD's engineering scope to mandate:
1.  Asynchronous wait loops in `central_runner.py` that respect the Kill Switch.
2.  Explicit container termination protocols in `SecureSandbox`.
3.  A dedicated sub-task for updating the E2E test suite to handle asynchronous pauses and simulated human approvals.