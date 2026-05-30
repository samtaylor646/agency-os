# E2E QA Test Plan & HITL Verification: V2 Features (Build vs. Run & Studio UI)

## 1. Executive Summary
This document defines the automated End-to-End (E2E) testing strategy and Human-in-the-Loop (HITL) verification steps for the AgencyOS V2 "Build vs. Run Sandbox" and "Studio UI" features. As Evidence Collector, the goal is to guarantee the strict isolation, cost controls, UI transparency, and deployment integrity between the Build (Sandbox) and Run (Production) environments.

## 2. Testing Scope
*   **Build Mode (Sandbox):** Network isolation, LLM degradation, Semantic Caching, Mock Execution Engine.
*   **Studio UI:** Split-pane rendering, Trace View overlay, Cache/Degradation indicators, Promotion modal workflow.
*   **Run Mode (Production):** Premium LLM restoration, live API execution, state persistence, worker queue execution.
*   **Promotion Lifecycle:** Immutable snapshotting, version tagging, safe transition of execution context.

---

## 3. Automated End-to-End (E2E) Test Plan

### 3.1 Build Sandbox Isolation Tests
*   **Test Case E2E-B1: Model Degradation Proxy**
    *   *Action:* Trigger an agent execution in Build Mode requesting a premium model (`gpt-4o`).
    *   *Expected Result:* LLM Routing Proxy intercepts the call and executes against the fallback model (`gpt-4o-mini`).
*   **Test Case E2E-B2: Tool Mocking & Network Isolation**
    *   *Action:* Trigger an agent with a DB Write tool and an External HTTP Call tool in Build Mode.
    *   *Expected Result:* Mock Execution Engine returns simulated success. No actual DB writes occur. Network requests fail/are intercepted with a mock response.
*   **Test Case E2E-B3: Semantic Caching**
    *   *Action:* Execute two identical prompts sequentially in Build Mode.
    *   *Expected Result:* First call reaches LLM (degraded). Second call returns immediately from Redis semantic cache. Trace logs verify a cache hit.
*   **Test Case E2E-B4: Hard Token Limits**
    *   *Action:* Provide a prompt designed to trigger infinite looping or huge token generation.
    *   *Expected Result:* Execution halts at the hard token cap (e.g., 2000 output tokens), preventing runaway costs.

### 3.2 Run Production Lifecycle Tests
*   **Test Case E2E-R1: Premium Model Execution**
    *   *Action:* Execute an agent assigned a premium model in Run Mode.
    *   *Expected Result:* The full premium model (`gpt-4o`, `claude-3-opus`) is utilized and recorded in trace logs.
*   **Test Case E2E-R2: Live API Execution**
    *   *Action:* Trigger a benign external HTTP read tool in Run Mode.
    *   *Expected Result:* Real network request succeeds and returns live data.
*   **Test Case E2E-R3: Asynchronous Queue Fulfillment**
    *   *Action:* Dispatch a long-running multi-agent workflow in Run Mode.
    *   *Expected Result:* The job is enqueued in the message broker (RabbitMQ/Redis + Celery). Client does not timeout. Execution completes asynchronously and state persists to PostgreSQL.

### 3.3 Promotion & State Integrity Tests
*   **Test Case E2E-P1: Immutable Snapshotting**
    *   *Action:* Promote an agent from Build to Run. Fetch the generated JSON snapshot.
    *   *Expected Result:* Snapshot contains exact configuration, System Prompt, and Tool Registry.
*   **Test Case E2E-P2: Versioning Independence**
    *   *Action:* Promote an agent to `v1.0.0`. Edit the agent further in Build Mode. Run a production execution.
    *   *Expected Result:* Production execution strictly utilizes the `v1.0.0` snapshot configuration; Sandbox edits do not bleed into the Run environment until explicitly promoted.

---

## 4. Human-in-the-Loop (HITL) Verification Steps

As per the Human-in-the-Loop Mandate, automated tests alone are insufficient for phase gate approval. A QA human must manually verify the UX and fail-safes.

### Step 1: UI Visual Indicator Spot-Check
*   [ ] Verify the AgencyOS Studio UI prominently displays the **"BUILD MODE"** banner to prevent accidental production assumptions.
*   [ ] Send a test query in the Sandbox Chat pane. Verify the **"Simulated on [Model]"** and **"Cache Hit"** badges render correctly when applicable.
*   [ ] Trigger a mock tool execution. Verify the **"Mock Executed"** badge appears in the chat stream.

### Step 2: Trace View & Debugging Validation
*   [ ] Open the **Trace View** overlay in the Sandbox.
*   [ ] Manually inspect the displayed reasoning steps, token usage metrics, and intermediate mock tool payloads.
*   [ ] Confirm the UI provides a one-click **"Replay Test"** button and it functions intuitively.

### Step 3: Promotion Modal Workflow Review
*   [ ] Click the **"Promote to Production"** button.
*   [ ] Verify the promotion modal clearly outlines the changes (model upgrade, live API access enabled).
*   [ ] Ensure the user is forced to input or confirm a Semantic Version tag (e.g., `v1.0.0`).
*   [ ] Complete the promotion and verify the UI transitions smoothly from "BUILD MODE" to "RUN MODE" for that specific agent.

### Step 4: Final QA Gate Sign-Off
*   [ ] Evidence Collector (Agent) has verified all E2E automated test suites pass without failure.
*   [ ] QA Specialist (Human) has completed all HITL visual and interactive checks.
*   [ ] Sign-off approved for merging the V2 features into the `main` branch.
