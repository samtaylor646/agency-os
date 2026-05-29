# Epic: Technical Debt - Nexus Pipeline Refactor (`central_runner.py`)

## 1. Executive Summary

**Epic Goal:** Refactor the monolithic `scripts/central_runner.py` into a modular, scalable, and maintainable component-based architecture within the `server/services` and `server/core` domains. This will resolve the critical technical debt identified in the Nexus Pipeline, improving system reliability, testability, and enabling parallel development.

**Business Value:**
* **Reduced Time-to-Market:** Modular architecture allows multiple engineers to work on the pipeline concurrently without merge conflicts.
* **Improved Reliability:** Smaller, focused components are easier to test and isolate failures, preventing cascading system crashes.
* **Scalability:** Enables independent scaling of specific pipeline stages (e.g., LLM execution vs. message routing).
* **Maintainability:** Reduces the cognitive load on developers, making onboarding and feature additions faster.

## 2. Problem Statement (The "Why")

Currently, `scripts/central_runner.py` acts as a monolithic orchestrator for the entire Nexus pipeline. It handles task routing, LLM execution coordination, validation, state management, and logging in a single file. This has led to several critical issues:
* **High Complexity:** The file is too large and complex, making it difficult to understand and modify safely.
* **Tight Coupling:** Components are tightly integrated, meaning a change in one area often breaks another seemingly unrelated area.
* **Testing Difficulties:** Unit testing specific logic is nearly impossible without mocking the entire system due to lack of dependency injection and isolated scopes.
* **Deployment Risks:** Any minor bug in the file can bring down the entire orchestration engine.

## 3. Architecture Vision

The goal is to move from a single script (`scripts/central_runner.py`) to a set of cohesive, decoupled services within the `server/` directory, adhering to single-responsibility principles.

**Target Architecture Components:**
1.  **`server/services/orchestrator_service.py`**: The high-level controller. It receives the initial request, breaks it down (DAG), and manages the overall lifecycle of the job. It does *not* execute tasks directly.
2.  **`server/services/task_router.py`**: Responsible for determining which specific agent or service should handle a given task based on the `.roomodes` configuration and agent capabilities.
3.  **`server/services/execution_engine.py`**: Interfaces with the `llm_runner.py` and `sandbox.py` to actually execute the tasks delegated by the router.
4.  **`server/core/state_manager.py`**: A centralized, persistent state machine (backed by Redis/Postgres) to track task progress, handle retries, and ensure idempotency.
5.  **`server/core/validation_middleware.py`**: A decoupled middleware layer (integrating with `validation_layer.py`) that strictly enforces rules and guardrails before and after execution.

## 4. Execution Plan (Step-by-Step Breakdown)

The engineering team will execute this refactor in distinct, verifiable phases to minimize disruption.

### Phase 1: Preparation & Scaffolding (Safe Isolation)
1.  **Audit `central_runner.py`**: Map out all existing functions and their dependencies.
2.  **Create Service Skeletons**: Create the empty files for the new architecture (`orchestrator_service.py`, `task_router.py`, `execution_engine.py`, `state_manager.py`).
3.  **Define Interfaces**: Define the Python classes and abstract base classes (ABCs) that will govern how these components communicate (e.g., Pydantic models for Task requests/responses).
4.  **Write Integration Tests (Baseline)**: Create a suite of end-to-end tests that verify the *current* behavior of `central_runner.py`. These must pass before and after the refactor.

### Phase 2: Extraction & Decoupling (The Core Refactor)
1.  **Extract State Management**: Move all in-memory tracking or ad-hoc state updates into the new `state_manager.py`. Refactor `central_runner.py` to use this new manager.
2.  **Extract Validation**: Decouple the validation logic into `validation_middleware.py` and ensure `central_runner.py` calls it cleanly.
3.  **Extract Routing**: Move the logic that selects the correct agent into `task_router.py`.
4.  **Extract Execution**: Move the LLM invocation and sandbox interaction logic into `execution_engine.py`.

### Phase 3: The Orchestrator Transition
1.  **Implement `orchestrator_service.py`**: Build the new orchestrator that purely coordinates the new services created in Phase 2.
2.  **Shadow Deployment**: Run `orchestrator_service.py` in parallel with `central_runner.py` for a specific subset of test tasks to verify parity.
3.  **Cutover**: Switch the main API endpoints in `server/main.py` and `server/api_server.py` to point to the new `orchestrator_service.py` instead of invoking `scripts/central_runner.py`.

### Phase 4: Cleanup & Hardening
1.  **Deprecate `central_runner.py`**: Mark the file as deprecated and eventually delete it.
2.  **Unit Coverage**: Ensure all new services have >90% unit test coverage.
3.  **Performance Review**: Verify that the decoupled architecture hasn't introduced unacceptable latency (monitor Redis/queue performance).

## 5. Success Criteria & Metrics

*   **Metric 1:** `scripts/central_runner.py` is entirely deleted from the codebase.
*   **Metric 2:** Cyclomatic complexity of the orchestration logic is reduced by at least 50% (measured via SonarQube or similar tool).
*   **Metric 3:** Test coverage for the new `server/services/` orchestration components exceeds 90%.
*   **Metric 4:** Zero regressions in existing end-to-end task completion rates during the cutover phase.

## 6. Dependencies & Risks

*   **Risk:** The cutover (Phase 3) might introduce subtle state management bugs.
    *   **Mitigation:** The shadow deployment strategy and heavy reliance on the baseline integration tests created in Phase 1.
*   **Dependency:** This epic requires the CI/CD pipeline to be stable so that integration tests can be run continuously during the refactor.

## 7. Approval Sign-offs Required
*   Backend Architecture Lead: _________
*   QA Lead (Evidence Collector): _________
*   Product Manager: _________
