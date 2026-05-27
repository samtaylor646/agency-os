# Changelog

## [2026-05-27] - Executive Summary Redesign Strategy (Phase 1)
- **Added**: Defined core value proposition, market impact, and GTM positioning narrative for the CEO and CTO.
- **Added**: Created `docs/core/Executive_Summary_Strategy_Brief.md` for handoff to Product Manager and UX Architect.
- **Status**: Completed Phase 1 GTM strategy brief.

## [2026-05-27] - Executive Summary HTML Presentation Deck
- **Added**: Built a standalone HTML presentation `docs/operations/Executive_Summary_Presentation.html` based on the Executive Summary Report.
- **Changed**: Included Tailwind CSS via CDN for styling and Chart.js for data visualization.
- **Status**: Completed frontend implementation and pushed to `feature/executive-summary-spec`.

## [2026-05-27] - Executive Summary Report Generation
- **Added**: Authored the final Markdown version of the Executive Summary Report in `docs/operations/Executive_Summary_Report.md` based on `docs/operations/Executive_Summary_Report_Spec.md`.
- **Status**: Completed document generation.

## [2026-05-27] - Executive Summary Report Specification
- **Added**: Defined the comprehensive structure and content specification for the Executive Summary Report in `docs/operations/Executive_Summary_Report_Spec.md`.
- **Status**: Completed data gathering from recent changelogs and roadmaps to prepare for Technical Writer and Frontend Dev handoff.

## [2026-05-27] - Documentation Consolidation Epic
- **Changed**: Read `docs/qa/docs_git_analysis.md` and consolidated `/docs/core/` and other folders to establish absolute source of truth.
- **Changed**: Moved obsolete PRDs and legacy master plans from `docs/core/` to `docs/archive/`.
- **Changed**: Moved active strategy documents like GTM Strategy to `docs/operations/`.
- **Status**: Completed documentation review and consolidation across the workspace.

## [2026-05-27] - Update Git Workflow Rules
- **Changed**: Updated `docs/operations/git_workflow_rules.md` to enforce the Phase 5 End of Task Mandate. Final git commit and push are now strictly gated behind formal HITL UAT approval.
- **Changed**: Updated `docs/operations/standard_kickoff_protocol.md` to include the mandatory End of Task Mandate closing sequence (Docs/Memory -> HITL -> Git Workflow Master Handoff).

## [2026-05-27] - End-to-Task Workflow Process Update
- **Added**: Drafted Scope Document/PRD `docs/core/prd_workflow_process_update.md` based on `docs/operations/workflow_process_review.md`.
- **Changed**: Formally defined the Five-Phase Workflow and the Phase 5 End of Task Mandate (Docs/Memory -> HITL -> Git Master).

## [2026-05-27] - Epic: Custom Agent Remediation (Phase 3 Handoff)
- **Completed**: Phase 3 (Maintainability & Policy) is complete.
- **Changed**: Decoupled hardcoded port configurations using `VITE_API_URL` environment variables in `client/vite.config.js` and `deployment/docker-compose.yml`.
- **Added**: Drafted GDPR-compliant Data Governance Policy in `docs/operations/data_governance_policy.md`.
- **Status**: The Custom Agent Remediation epic is fully complete and ready for final review or closure.

## [2026-05-27] - Epic: Custom Agent Remediation (Phase 2 Handoff)
- **Verified**: Human-in-the-loop manual verification successfully passed for Custom Agent Remediation Phase 2.
- **Fixed**: Corrected `VITE_API_URL` proxy target fallback in `client/vite.config.js` to fix 401 Unauthorized errors during auto-login.
- **Verified**: Proved that backend rejects legacy flat payloads with a 422 error.
- **Verified**: Proved atomic transactions correctly roll back database insertions if file saving fails.
- **Status**: Formally closed out Phase 2 (Data Integrity & Schema Mapping). Next step is Phase 3 (Maintainability & Policy).

## [2026-05-27] - Epic: Project Scope UI Remediation
- **Added**: Implemented file upload component in `client/src/ChatScopeInterface.jsx` supporting `.txt`, `.md`, and `.pdf` files.
- **Changed**: Modified `WorkspaceContext.jsx` API interceptor to support native `FormData` uploads by omitting default JSON headers.
- **Added**: QA Sign-off test and formal handoff document (`docs/qa/qa_signoff_epic_project_scope_remediation.md`).
- **Changed**: Archived old infrastructure plans to avoid confusion.


## [2026-05-27] - Sprint 4: Secure Execution Sandbox (Infrastructure Remediation)
- **Added**: Implemented Docker-based isolated execution environment in `server/services/sandbox.py`.
- **Added**: Built API endpoint `/api/v1/sandbox/execute` in `server/routers/sandbox.py` for dispatching untrusted code.
- **Changed**: Modified `scripts/central_runner.py` to route node execution to the Secure Sandbox when `agent_name` is `"CodeSandbox"`.
- **Added**: Generated sprint handoff documentation `docs/archive/sprint_4_sandbox_handoff_summary.md` and pushed branch `epic/sprint-4-secure-sandbox`.

## [2026-05-27] - Sprint 3: Real-Time Orchestration (Infrastructure Remediation)
- **Added**: Implemented Redis & FastAPI WebSockets in `server/routers/websockets.py` and connected it in `server/main.py`.
- **Changed**: Instrument DAG Orchestrator in `scripts/central_runner.py` to publish real-time events (`node_start`, `node_complete`, `node_failed`, `workflow_start`, `workflow_complete`, `workflow_failed`) to Redis using `message_broker`.
- **Changed**: Refactored frontend components (`PipelineExecutionViewer.jsx` and `PodChatContainer.jsx`) to connect to WebSocket endpoints and render backend execution states instead of simulated mocks.
- **Completed**: End-to-end integration mapping from DAG Python runner -> Redis -> FastAPI WebSockets -> React frontend.
## [2026-05-27] - Epic 4.4.C & Phase 4 Handoff
- **Completed**: Epic 4.4.C (Comprehensive E2E testing of the Pod lifecycle) is officially complete.
- **Status**: Formally closed out Phase 4. Next step identified as Phase 5, Sprint 5.1 (GTM Strategy).
- **Added**: Created PRD for Epic 5.1.A (`docs/core/prd_epic_5.1.A_gtm_strategy.md`) to kick off Launch & Growth.

## [2026-05-27] - Epic 4.4.A: LLM Kill Switch Architecture
- **Added**: Implemented `KillSwitch` service backed by Redis in `server/services/kill_switch.py`.
- **Added**: REST API endpoints for kill switch management (`/kill-switch/activate`, `/kill-switch/deactivate`, `/kill-switch/status`) in `server/api_server.py`.
- **Changed**: Modified `DAGOrchestrator.execute_workflow` in `scripts/central_runner.py` to poll kill switch state and halt N:N Pod executions if activated.
- **Added**: Technical documentation in `docs/technical/llm_kill_switch_architecture.md`.
- **Added**: Runbook for containing blast radiuses in `agents/strategy/runbooks/scenario-autonomous-blast-radius.md`.

## [2026-05-26] - Phase 5 Kickoff
- **Status**: Transitioned Phase 5 from Pending to In Progress.
- **Added**: Linked Phase 5 Master Plan in `AgencyOS_Phases_Master_Plan.md`.

## [2026-05-26] - Phase 4 Handoff
- **Completed**: Phase 4 officially completed.
- **Added**: Consolidated Phase 4 handoff summary generated at `docs/archive/phase_4_handoff_summary.md`.

## [2026-05-25] - Epic: Fix Custom Agent Wizard Error
- **Fixed**: Custom Agent Creator UI failed to send `Authorization` and `X-Tenant-ID` headers to the backend, causing 401 Unauthorized errors.
- **Changed**: `client/src/CustomAgentCreator.jsx` to dynamically fetch the token from `localStorage` and `activeWorkspace` from `WorkspaceContext`.
- **Added**: Added `validation_layer.py` per epic instructions.
- **Added**: Added Evidence documentation in `docs/qa/evidence_epic_fix_custom_agent.md`.

## [2026-05-26] - Epic: Technical Debt & Security Remediation (Custom Agent Creation)
- **Fixed**: Removed hardcoded tenant ID fallback in `client/src/CustomAgentCreator.jsx` and `server/dependencies.py` to enforce strict boundaries.
- **Fixed**: Removed request body echoing in global exception handler (`server/main.py`) to prevent PII leaks.
- **Changed**: Refactored `CustomAgentCreate` schema to enforce nested structure and implemented legacy mapping adapter in `client/src/CustomAgentCreator.jsx`.
- **Changed**: Decoupled hardcoded port configurations using `VITE_API_URL` environment variables in `client/vite.config.js` and `docker-compose.yml`.
- **Added**: Drafted GDPR-compliant Environment Data Segregation and Log Retention policies in `docs/operations/gdpr_compliance_policies.md`.
- **Added**: Added strict tenant isolation tests and provided formal QA sign-off in `docs/qa/custom_agent_tenant_isolation_qa_signoff.md`.

## [2026-05-26] - Hotfix: Custom Agent Wizard & Dev Environment (fix/custom-agent-403)
- **Fixed**: Dev environment reactivity broken in Docker; updated `client/vite.config.js` to enable filesystem polling (`watch: { usePolling: true }`).
- **Verified**: Human-in-the-loop manual verification successfully passed for Custom Agent creation via UI.

## [2026-05-26] - Epic: Phase 4 Sprint 4.3 - Frontend Marketplace UI
- **Added**: Implemented `PodChatContainer`, `AgentMessageBubble`, and real-time session streaming for the Pod View interface.
- **Added**: Built `MemoryInspectorSidebar` and `ContextCard` components to visualize Semantic Memory and RAG data context.
- **Added**: Created the `MarketplaceGrid`, `EntityCard`, `EntityDetailModal`, and `FilterSidebar` for the AgencyOS marketplace discovery flow.
- **Verified**: Formal QA signoff documented in `docs/archive/qa_signoff_phase_4_sprint_4.3.md`.

## [2026-05-26] - Epic: Phase 4 Sprint 4.2 - Semantic Memory Layer
- **Added**: Upgraded infrastructure to `pgvector` for semantic search (Docker, Kubernetes, CI).
- **Added**: Implemented `OpenAIEmbeddingProvider` (`text-embedding-3-small`) and FastAPI embedding abstraction.
- **Added**: Document chunking, ingestion, and vector semantic retrieval logic.
- **Added**: Security and QA measures, including RBAC filtering on `workspace_id`, test plans, and data poisoning prevention logic.
- **Verified**: Formal QA signoff documented in `docs/archive/qa_signoff_phase_4_sprint_4.2.md`.

## [2026-05-26] - Epic: Phase 4 Sprint 4.1 - Message Broker & Semantic Storage
- **Added**: Implemented `message_broker.py` for Redis Pub/Sub async agent communication (Epic-4.1.A).
- **Added**: Added `pgvector` extension and `vector` column to `documents` table via Alembic for semantic memory (Epic-4.1.B).
- **Added**: Wrote unit tests for `message_broker.py` to satisfy QA gates.
- **Fixed**: Updated `test_chat.py` payloads to include the required `doc_type` to resolve 422 errors.

- Phase 3 Rebuild Sprint: Completed Epic B (Custom Agent Storage & Lifecycle Management) and DevOps & Infrastructure configuration.

### Epic 4.4.A - QA Sign-Off
- QA tests for the LLM Kill Switch written and passed successfully.
- Added `server/tests/test_kill_switch.py`.
- Documented QA sign-off in `docs/qa/qa_signoff_phase_4_epic_4.4.A.md`.

### Sprint 4.4 / Phase 4 Completion
- Completed Epic 4.4.B: Asynchronous load testing implementation.
- Completed Epic 4.4.C: E2E Pod Lifecycle testing.
- Resolved duplicate import architectural debt in `api_server.py`.
- Formally closed out Phase 4 and generated `docs/archive/phase_4_completion_handoff.md`.

## 2026-05-27: Ticket 2.3 Frontend Global State Migration
* Audited static state components and wired them to backend endpoints using `apiFetch`.
* Refactored `WorkspaceContext.jsx`, `CreateWorkspaceModal.jsx`, `AuditLogViewer.jsx`, `Marketplace.jsx`, `RBACManager.jsx`, and `PodChatContainer.jsx` to fetch data from real API endpoints instead of static mock arrays.
* Ensured no static mock data remains in standard UI flows.

## 2026-05-27: Phase 5 Sprint 5.1 Completion
* Created branch `epic/phase-5-launch-and-growth`
* Business Strategist defined `docs/core/GTM_Strategy.md` and `docs/core/Messaging_Matrix.md`
* Content Creator defined `docs/core/Launch_Blog_Post.md`, `docs/operations/Cross_Channel_Activation_Strategy.md`, and `docs/operations/Content_Staging_Pipeline.md`
* DevOps Engineer defined `docs/operations/blue_green_deployment_runbook.md` and `docs/operations/rollback_runbook.md`
* Analytics Reporter defined `docs/operations/production_analytics_spec.md`
* Human Validation Gate explicitly approved by user

## 2026-05-27: Phase 5 Sprint 5.2 and 5.3 Completion
* Backfilled Standard Kickoff Protocol for Phase 5 (PRD, Tech Spec, Compliance Signoff, Test Plan).
* Executed blue-green deployment (`deployment_log_5.2.A.md`).
* Triggered marketing blasts (`marketing_activation_log_5.2.B.md`).
* Executed community engagement (`community_engagement_log_5.2.C.md`).
* Compiled 48-hour Executive Summary (`post_launch_synthesis_sprint_5.3.md`).

- 2026-05-27: Updated `docs/qa/master_human_verification_plan.md` to incorporate Phase 5 Sequence Validation rules, ensuring human verification of memory updates before final Git approval.

## [2026-05-27] QA Documents Git Analysis
- Performed analysis of all files in `docs/qa/`.
- Generated `docs/qa/qa_docs_git_analysis.md` summarizing file dates, recent commits, and cross-referencing with project timeline.
- Identified older sprints and point-in-time test plans as candidates for archival to streamline QA document tracking.
Archived old QA documents
- Created subdirectories `core`, `operations`, and `technical` in `docs/archive` to maintain category structure for archived documents.

## [2026-05-27] - Documentation Move Reversal
- **Fixed**: Reverted accidental move of active documentation folders, restoring `docs/core/`, `docs/operations/`, and `docs/technical/`.
- **Added**: Created matching empty archive directories (`docs/archive/core/`, `docs/archive/operations/`, `docs/archive/technical/`) reflecting true intent.
## [2026-05-27] - Archiving Superseded Technical Documentation
- **Changed**: Cross-referenced files in `/docs/technical` with their git commit history.
- **Changed**: Moved identified old and superseded files (past phase assessments, old sprint specs, and deprecated design plans) to `/docs/archive/technical/` to keep the technical documentation folder clean and relevant.

## [2026-05-27] - Archiving Superseded Operations Documentation (Epic consolidation)
- **Changed**: Moved old operations logs, sprint plans, and Phase assessments to `/docs/archive/operations/`.
- **Changed**: Consolidated all recent archive moves (technical, qa, operations) into the `epic/archive-docs` branch.
- **Verified**: Confirmed documentation routing rules (no files at the root of `docs/`).

## [2026-05-27] - Archive Root Consolidation
- **Changed**: Categorized and moved all loose files in `/docs/archive/` root into their respective subdirectories (`core`, `technical`, `operations`, `qa`).
- **Verified**: Confirmed no loose files remain in the root of `/docs/archive/`.
