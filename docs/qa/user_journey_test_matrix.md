# Role & Journey Matrix: QA Testing Framework

## 1. Executive Summary
This document defines the Role-Based Access Control (RBAC) personas and outlines the end-to-end user journeys for AgencyOS. It serves as the primary testing matrix for the QA team and the Evidence Collector agent to validate permissions, user flows, and strict environment separation (Build vs. Run).

## 2. User Roles & Permitted Actions

### 2.1 System Roles (Human)

| Role Name | Description | Permitted Actions | Restricted Actions |
| :--- | :--- | :--- | :--- |
| **Workspace Admin** | Full access to workspace configuration and billing. | Manage RBAC, create/delete workspaces, view billing, promote agents to Production. | System-level infrastructure changes. |
| **Solution Architect** | Designs multi-agent pods and complex workflows. | Access Studio UI, define Agent architectures, configure tools, view Trace Overlays, trigger E2E Sandbox tests. | Direct code deployments bypassing CI/CD. |
| **Prompt Engineer** | Focuses on agent personas, system prompts, and behavior. | Access Studio UI (Build Mode), modify system prompts, run Sandbox tests, view token usage, initiate promotion requests. | Promote directly to Production (requires Admin approval). |
| **Developer** | Integrates agents with external systems and custom APIs. | Add custom tools, configure external API keys, view system logs, manage backend worker queues. | Modify core AgencyOS framework code without QA sign-off. |
| **QA Specialist** | Performs Human-in-the-Loop (HITL) testing and validation. | Run E2E tests, access QA dashboards, review Trace Views, approve/reject Phase Gates, approve Production promotions. | Modify production configurations. |
| **Content Editor** | Manages data ingestion and knowledge base content. | Upload documents, manage Semantic Storage vectors, update Agent context data. | Modify Agent logic or tooling. |

### 2.2 System Roles (Agent)

| Agent Role | Description | Permitted Actions |
| :--- | :--- | :--- |
| **Evidence Collector** | Automated QA and validation agent. | Run automated E2E tests, evaluate test coverage, block merges on failure, log QA evidence. |
| **Orchestrator** | Central execution coordinator. | Route tasks to specialized agents, manage execution state, trigger Phase Gate reviews. |

---

## 3. QA Test Journeys (Step-by-Step)

The following journeys must be executed by the QA team (Automated and HITL) to validate role restrictions and functionality.

### Journey 1: Agent Creation & Sandbox Testing (Prompt Engineer)
*Target Role: Prompt Engineer*
1. **Login & Navigate**: User logs in and navigates to the AgencyOS Studio interface.
2. **Configure**: User defines a new agent, setting the System Prompt and adding a mock DB Write tool.
3. **Verify Build Mode**: *QA Check:* Confirm the UI prominently displays the "BUILD MODE" banner.
4. **Test Execution**: User submits a test query in the right-hand Sandbox pane.
5. **Verify Mocking & Degradation**: *QA Check:* Confirm the UI indicates "Simulated on gpt-4o-mini" and the tool displays a "Mock Executed" badge.
6. **Iterate & Cache**: User edits the prompt and clicks "Replay Test".
7. **Verify Caching**: *QA Check:* Confirm the "Cache Hit" indicator appears and response time is near-instant.

### Journey 2: Promotion to Production (Solution Architect / Admin)
*Target Role: Solution Architect (Request) -> Workspace Admin (Approve)*
1. **Initiate Promotion**: Solution Architect reviews the Sandbox performance and clicks "Promote to Production".
2. **Review Modal**: *QA Check:* Confirm the promotion modal warns of model upgrades (e.g., to `gpt-4o`) and live data access.
3. **Version Tagging**: User inputs a Semantic Version tag (e.g., `v1.0.0`).
4. **Confirmation**: Workspace Admin confirms the promotion.
5. **Verify Run Mode**: *QA Check:* UI shifts from "BUILD MODE" to "RUN MODE".
6. **Immutable Snapshot**: *QA Check:* Backend verifies an immutable configuration snapshot was generated.
7. **Production Test**: Run a benign query in Run Mode and verify live API access and premium model usage in trace logs.

### Journey 3: RBAC Enforcement & Failure Testing (QA Specialist)
*Target Role: QA Specialist*
1. **Role Context Switch**: QA Specialist assumes the role of a "Prompt Engineer".
2. **Attempt Unauthorized Action**: Attempt to forcefully promote an agent to production without Admin approval.
3. **Verify Block**: *QA Check:* System throws a 403 Forbidden error and UI blocks the action.
4. **Assume Developer Role**: Switch to "Developer" role.
5. **Attempt Tool Creation**: Create a new external HTTP tool.
6. **Verify Success**: *QA Check:* Tool is successfully added to the workspace registry but isolated to Build Mode until promoted.

### Journey 4: Human-in-the-Loop (HITL) Gate Approval
*Target Role: QA Specialist / Workspace Admin*
1. **Trigger Workflow**: A long-running multi-agent workflow reaches a predefined Phase Gate.
2. **Execution Pause**: *QA Check:* Orchestrator agent pauses execution and flags for human review.
3. **Review Context**: QA Specialist reviews the Trace View and intermediate outputs.
4. **Approve Gate**: QA Specialist clicks "Approve".
5. **Resume Execution**: *QA Check:* Workflow resumes execution in the queue.

## 4. Automation Mapping
*   **Journeys 1 & 3** are primarily covered by `e2e/test_sandbox.py` and Role validation scripts.
*   **Journeys 2 & 4** require explicit Human-in-the-Loop (HITL) manual execution combined with Evidence Collector automated assertions.