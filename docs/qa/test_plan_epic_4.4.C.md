# QA Test Plan: Epic 4.4.C - E2E Pod Testing

## 1. Overview
This test plan outlines the quality assurance strategy for Epic 4.4.C, which focuses on establishing an automated End-to-End (E2E) testing suite for the Pod lifecycle in AgencyOS. The suite will validate multi-agent interactions, message brokering, and semantic memory recall.

## 2. Scope
The scope of this test plan includes:
- Test Environment Isolation Verification
- Pod Initialization Automation
- Multi-Agent Messaging (N:N) Automation
- Semantic Memory Recall Automation
- Kill Switch Verification Automation

## 3. Test Scenarios

### 3.1 Test Environment Isolation Verification
- **Goal:** Ensure tests do not impact production or live databases.
- **Steps:**
  1. Inspect `server/tests/conftest.py` to verify test db and test redis configurations.
  2. Verify that `pytest` aborts if `APP_ENV=production`.
  3. Verify cleanup teardown fixtures.

### 3.2 Pod Initialization
- **Goal:** Verify multiple agents initialize correctly within a Pod.
- **Steps:**
  1. Trigger Pod Initialization test in `server/tests/test_e2e_pod_lifecycle.py`.
  2. **Expected Result:** Assert agents register with the broker, subscribe to topics, and context is loaded properly.

### 3.3 Multi-Agent Messaging (N:N)
- **Goal:** Verify messages are correctly routed between agents via `message_broker.py`.
- **Steps:**
  1. Run the multi-agent message routing test.
  2. Mock LLM responses to ensure determinism.
  3. **Expected Result:** Assert message order, proper topic subscription, and delivery to correct agent instances.

### 3.4 Semantic Memory Recall
- **Goal:** Validate `pgvector` memory retrieval.
- **Steps:**
  1. Run the semantic search test.
  2. Seed the test database with sample documents.
  3. **Expected Result:** Assert semantic search returns the context with expected similarity metrics.

### 3.5 Kill Switch Verification
- **Goal:** Verify that a kill switch signal halts all active agents in a Pod immediately.
- **Steps:**
  1. Run the kill switch scenario where a multi-step task is interrupted.
  2. **Expected Result:** Assert agents halt execution and pending messages are dropped.

## 4. Execution Strategy
- The test suite will be run locally via `pytest` by developers.
- It will be integrated into the CI/CD pipeline to gate any PRs merging into main.
