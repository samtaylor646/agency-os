# Automated Testing Standards

## 1. Philosophy
* **Shift-Left Approach:** Testing is integrated early in the development lifecycle. Developers are responsible for writing tests alongside feature code.
* **Test Pyramid Strategy:** The majority of tests should be fast, isolated Unit Tests, supported by a solid layer of Integration Tests, and capped with critical path End-to-End (E2E) tests.
* **Evidence-Based QA:** Code must be proven to work via automated tests before merging. The Evidence Collector agent enforces strict test passing criteria on all PRs.
* **Deterministic LLM Testing:** Due to the non-deterministic nature of LLMs, agent logic must be tested using mocked responses and predefined prompt-completion pairs.

## 2. Testing Layers

### 2.1. Unit Testing
* **Framework(s):** 
  * Backend: `pytest` (Python)
  * Frontend: `Vitest` / `Jest` & React Testing Library (JavaScript/React)
* **Coverage Goal:** Minimum 85% line coverage for core services; 100% for critical security and RBAC logic.
* **Scope:** 
  * Individual functions, classes, and isolated UI components.
  * Mocks must be used for all external dependencies (databases, external APIs, LLM providers).

### 2.2. Integration Testing
* **Framework(s):** 
  * Backend: `pytest` with `pytest-asyncio` and test databases (SQLite in-memory or isolated PostgreSQL schemas).
* **Scope:** 
  * API endpoints, database interactions (CRUD operations via SQLAlchemy), and multi-component workflows.
  * Agent-to-Agent communication flows within a mocked DAG (Directed Acyclic Graph) environment.
* **Execution:** Run against a localized, containerized test environment resembling production.

### 2.3. End-to-End (E2E) Testing
* **Framework(s):** Playwright
* **Scope:** 
  * Full user journeys simulating real browser interactions (e.g., user login, creating a custom agent, running a pipeline).
  * WebSocket connectivity and live UI updates during agent executions.
* **Execution:** Run in the CI pipeline against a fully stood-up staging environment.

### 2.4. Agentic & LLM Evaluations
* **Framework(s):** Custom evaluation scripts (`scripts/qa_runner.py`), Promptfoo (optional).
* **Scope:** 
  * Evaluating agent outputs against expected formats (JSON schemas, strict formatting).
  * Testing guardrails, kill-switches, and fallback mechanisms when LLM services degrade.

## 3. CI/CD Integration
* **Blocking PRs:** All tests must pass before a Pull Request can be merged into `main`. The CI pipeline will automatically reject PRs with failing tests or decreased code coverage.
* **Execution Environments:**
  * **PR Checks:** Runs Unit and Integration tests within isolated GitHub Actions runners.
  * **Deployment Gates:** E2E tests run prior to swapping blue/green environments or deploying to production.
* **Artifacts:** Test reports and visual evidence (from failed UI tests) are attached to the CI build artifacts for the Evidence Collector to review.

## 4. Naming & Organization
* **File Naming:** 
  * Python: `test_<module_name>.py`
  * Frontend: `<ComponentName>.test.jsx` or `<ComponentName>.spec.js`
* **Structure:** Test files should mirror the `src` / `server` directory structure (e.g., `server/routers/api.py` -> `server/tests/test_api.py`).
* **Descriptions:** Use descriptive test names that state the expected behavior (e.g., `def test_agent_kill_switch_terminates_pipeline_on_malicious_input():`).
