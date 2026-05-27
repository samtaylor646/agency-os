# Technical Design Document: Epic 4.4.C - E2E Pod Testing

## 1. Introduction
This document outlines the technical architecture and implementation strategy for automated End-to-End (E2E) testing of the Pod lifecycle in AgencyOS, fulfilling the requirements of Epic 4.4.C. The goal is to establish a robust testing suite using `pytest` that validates multi-agent interactions, message brokering, and semantic memory recall, without introducing side-effects to the production database or live message queues.

## 2. Architecture Overview
The E2E testing suite will leverage `pytest` as the core testing framework. To ensure tests are isolated, repeatable, and fast, the architecture will employ dependency injection and containerized mock services (or lightweight local instances like SQLite for DB and in-memory brokers) where appropriate, although the goal is to test the integration with `message_broker.py` (Redis) and `pgvector`.

### 2.1 Test Environment Isolation
To prevent side-effects during testing:
- **Database (`pgvector`)**: Tests will utilize a dedicated test database schema or a separate ephemeral PostgreSQL container with the `pgvector` extension. Database connections within the application will be overridden using FastAPI dependency overrides to point to this test database. Transactions will be rolled back after each test case to ensure a clean state.
- **Message Broker (`message_broker.py` / Redis)**: Tests will either use an isolated Redis logical database (e.g., DB 1 or 2 instead of default 0) or an in-memory mock if strict unit-level speed is preferred. However, for true E2E testing as specified, an isolated Redis namespace or logical database will be used to validate the actual pub/sub mechanics of `message_broker.py`.

### 2.2 Core Components

#### 2.2.1 The Test Runner (`pytest`)
- Located in `server/tests/test_e2e_pod_lifecycle.py`.
- Responsible for orchestrating the test setup (fixtures), execution, and teardown.
- Will use `pytest-asyncio` to handle asynchronous operations intrinsic to the LLM runners and message brokers.

#### 2.2.2 Multi-Agent Simulation
- Agents will not make actual LLM calls during standard E2E tests to save costs and ensure deterministic results.
- `server/services/llm_runner.py` will be mocked or patched using `unittest.mock` to return predefined responses based on the input prompt context.
- The `message_broker.py` will act as the conduit, routing simulated messages between agents (e.g., an Orchestrator sending a task to an Analyst, and the Analyst replying).

## 3. Integration Points

### 3.1 `message_broker.py` Integration
The `message_broker` manages communication between agent pods.
- **Test Strategy**: The test suite will initialize the `message_broker` connected to the test Redis instance.
- **Verification**: Tests will assert that when Agent A publishes a message to Topic X, Agent B (subscribed to Topic X) receives the message correctly. We will validate message payload serialization/deserialization and routing logic.

### 3.2 `pgvector` and Semantic Memory Integration
Agent memory is stored in PostgreSQL utilizing the `pgvector` extension for similarity search.
- **Test Strategy**: The test suite will seed the test database with specific mock conversational histories and documents.
- **Verification**: Tests will simulate an agent querying its memory (via `server/services/semantic_search.py`) and assert that the retrieved context matches the expected relevant mock data based on vector similarity thresholds.

## 4. Test Scenarios (The Pod Lifecycle)

### 4.1 Pod Initialization
- **Scenario**: Initialize a Pod with multiple agents (e.g., Orchestrator, Researcher, Writer).
- **Assertions**: Verify agents are registered with the broker, subscribe to correct topics, and load their initial context.

### 4.2 Multi-Agent Messaging (N:N)
- **Scenario**: Orchestrator sends a broadcast message. Researcher responds. Writer waits for Researcher.
- **Assertions**: Verify message order, correct routing, and state transitions of individual agents without race conditions.

### 4.3 Semantic Memory Recall
- **Scenario**: Agent is prompted with a query requiring historical context.
- **Assertions**: Verify the semantic search service queries `pgvector` and returns the relevant context accurately, injecting it into the simulated LLM prompt.

### 4.4 Kill Switch Verification
- **Scenario**: Trigger the Kill Switch (via `server/services/kill_switch.py`) while a Pod is actively processing a complex multi-step task.
- **Assertions**: Verify all agents halt execution immediately, pending messages in the broker are discarded or flagged as cancelled, and no further simulated LLM calls are attempted. This proves blast radius containment.

## 5. Security & Side-Effect Mitigation
- **Strict Environment Variables**: Tests will aggressively validate that `APP_ENV` is set to `testing`. If `APP_ENV=production`, the test suite will immediately abort.
- **Data Teardown**: Pytest fixtures will guarantee that any data written to the test `pgvector` instance or test Redis database is truncated after the test session completes.

## 6. Next Steps
1. Configure `pytest.ini` for the test environment.
2. Implement database and Redis test fixtures in `server/tests/conftest.py`.
3. Develop the mock LLM responder for deterministic agent behavior.
4. Draft the test cases in `server/tests/test_e2e_pod_lifecycle.py`.
