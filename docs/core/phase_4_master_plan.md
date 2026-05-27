# Phase 4 Master Plan: Pods, Memory, & Marketplace Ecosystem

## 1. Executive Summary
Following the successful stabilization of the DAG orchestrator in Phase 3, Phase 4 focuses on advancing the core capabilities of AgencyOS. Based on the reassessment reports from the Backend and UX Architects, this phase will introduce multi-agent Pods, long-term Semantic Memory, and the foundational Marketplace UX, while continuing to harden the platform.

## 2. Goals & Objectives
*   **Enable Complex Collaboration:** Move beyond 1:1 agent interactions to support N:N collaborative Pods.
*   **Implement Persistent Context:** Integrate a semantic memory layer to allow agents to recall past interactions and context.
*   **Establish Marketplace Foundations:** Build the UI components and backend schemas necessary for sharing and discovering agents/pods.
*   **Maintain Quality:** Enforce strict QA gates, requiring robust test coverage for all new architectural components.

## 3. Sprint Plan & Resource Allocation

### Sprint 4.1: Message Broker & Semantic Storage Foundation
*   **Duration:** 2 Weeks
*   **Focus:** Core backend infrastructure for Pods and Memory.
*   **Epics:**
    *   `Epic-4.1.A`: Integrate lightweight message broker (Redis Pub/Sub) for async agent communication, including updating `docker-compose.yml` and Kubernetes manifests. (Backend Architect, DevOps Engineer)
    *   `Epic-4.1.B`: Integrate self-hosted Vector Database (`pgvector` via PostgreSQL) to minimize external dependencies for semantic memory storage. (Backend Architect, DevOps Engineer)
    *   `Epic-4.1.C`: Update `design_tokens_and_layout_spec.md` with Marketplace UI components. (UX Architect)

### Sprint 4.2: Pod Orchestration & Memory API
*   **Duration:** 2 Weeks
*   **Focus:** Building APIs on top of the new infrastructure.
*   **Epics:**
    *   `Epic-4.2.A`: Refactor `central_runner.py` to support event-driven Pod execution. (Backend Architect, Senior Developer)
    *   `Epic-4.2.B`: Develop CRUD endpoints for Pod management. (Senior Developer)
    *   `Epic-4.2.C`: Develop Memory retrieval and storage APIs for agents. (Senior Developer)

### Sprint 4.3: UI Implementation & Marketplace Components
*   **Duration:** 2 Weeks
*   **Focus:** Frontend realization of Pods, Memory, and Marketplace.
*   **Epics:**
    *   `Epic-4.3.A`: Implement Multi-Agent Chat Interface (Pod view). (Frontend Developer, UX Architect)
    *   `Epic-4.3.B`: Implement Memory Inspector panel in the UI. (Frontend Developer, UX Architect)
    *   `Epic-4.3.C`: Build foundational Marketplace UI components (Cards, grids, details). (Frontend Developer)

### Sprint 4.4: Hardening & QA Gauntlet
*   **Duration:** 2 Weeks
*   **Focus:** Security, load testing, and comprehensive QA.
*   **Epics:**
    *   ~~`Epic-4.4.A`: Security audit of Pod messaging, implement LLM Kill Switch, and validate blast radius containment for autonomous DAGs.~~ (COMPLETED)
    *   ~~`Epic-4.4.D`: Finalize Marketplace Terms of Service and User Generated Content (UGC) Liability Framework.~~ (COMPLETED)
    *   `Epic-4.4.B`: Load testing of the new message broker and vector DB, expanding `scripts/load_test.py` to simulate concurrent Pods. (DevOps Engineer, Infrastructure Maintainer)
    *   `Epic-4.4.C`: Comprehensive E2E testing of the Pod lifecycle, ensuring automated test scripts are required before main merge. (Evidence Collector)

## 4. Roles & Responsibilities
*   **Product Manager:** Backlog grooming, sprint planning, and feature validation.
*   **Backend Architect:** System design for Message Broker and Vector DB integration.
*   **UX Architect:** Multi-agent UI patterns and Marketplace design system.
*   **Senior Developer / Frontend Developer:** Implementation of backend APIs and frontend components.
*   **DevOps Engineer / Infrastructure Maintainer:** Infrastructure setup, scaling, and load testing.
*   **Incident Response Commander:** Security runbooks, Kill Switch validation, and blast radius testing.
*   **Legal Compliance Checker:** TOS, IP protection, and UGC Liability frameworks.
*   **Evidence Collector:** QA gatekeeping and test automation.

## 5. Success Criteria
*   Agents can successfully communicate asynchronously within a Pod.
*   Agents can retrieve relevant historical context from the Vector DB.
*   The UI displays multi-agent conversations clearly.
*   Marketplace foundational components are built and documented.
*   All new features pass the automated QA gauntlet with >80% coverage.
