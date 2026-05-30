# Changelog

## [2026-05-30] - Epic: Executive Summary Generation Completed
- **Completed**: Generated the current Executive Summary for the Phase 5 Launch & Red Team Handoff.
- **Added**: Authored `docs/core/Phase_5_Executive_Summary.md` applying the SCQA framework and executive reporting guidelines.
- **Status**: Formally closed out the Executive Summary generation Epic and completed the epic handoff.

## [2026-05-30] - Epic 8: Async Database Refactor Completed
- **Completed**: Phase 2 of the Async DB Refactor is complete.
- **Completed**: The entire Async Database Refactor Epic (Epic 8) has passed the final QA Gauntlet and is officially completed.

## [2026-05-29] - Epic: Phase 7 MCP Skills Architecture Completed
- **Completed**: QA officially signed off on the MCP Skills Architecture Epic.
- **Added**: Integrated official Python MCP Client SDK into `llm_runner.py` for routing tool calls via the Model Context Protocol.
- **Added**: Built `agent-architect.md` meta-prompt and `AgentUpgraderWorker` Redis queue to automatically upscale open-source PRPM `agents.md` files.
- **Added**: Implemented "Friction by Design" Security Gate UI components (`AgentApprovalModal.jsx`) ensuring human-in-the-loop explicit consent for MCP capabilities.
- **Added**: Completed PRD, Technical Specifications, and QA sign-offs in `docs/`.
- **Status**: Formally closed out Epic 7 and prepared branch `epic/mcp-skills-architecture` for merge to main.

## [2026-05-29] - Epic: Technical Debt Execution (Phase 4 Hardening)
- **Completed**: QA officially signed off on the Technical Debt Sprint.
- **Added**: Implemented Docker Sandbox Resource Quotas and Firecracker MicroVM integration planning.
- **Added**: Built a `SandboxReaper` background daemon to prune orphaned containers and stabilize local deployments.
- **Added**: Integrated Redis Pub/Sub decoupling for WebSocket messaging in `server/services/message_broker.py` and `server/routers/websockets.py`.
- **Changed**: Reverted Async Database Refactor (SQLAlchemy 2.0 `AsyncEngine`) due to cascading QA test failures, moving it back to the backlog for a dedicated Sprint.
- **Status**: Branch `epic/tech-debt-execution` formalized, pushed, and ready for merge.

## [2026-05-29] - Epic: Phase 6 Template Library & Dynamic API Routing Completed
- **Completed**: Phase 6 Epic is officially complete and QA signed off.
- **Added**: Implemented Template Library features, dynamic API routing (OpenAI/Anthropic/Gemini), and Rollback mechanisms.
- **Status**: Formally closed out Phase 6.

## [2026-05-29] - Epic: Feedback Loops & Intervention (Phase 5) Completed
- **Completed**: Phase 5 Feedback Loops Epic is officially complete.
- **Added**: Documentation for Architecture, Tech Debt, Risk Assessment, and PRD finalized.
- **Added**: Formal QA Sign-off for Phase 5 Feedback Loops (`docs/qa/Phase5_Feedback_Loops_QA_Signoff.md`).
- **Added**: Implemented new `Paused` and `Awaiting_Approval` states in the execution engine.
- **Added**: Added WebSocket events for real-time pipeline status updates.
- **Added**: Built `PipelineExecutionViewer` Mid-Execution Chat UI for human-in-the-loop interventions.
- **Status**: Formally closed out Phase 5 Epic. Transitioned to Phase 6: Operate & Evolve.

## [2026-05-29] - Epic: Feedback Loops & Intervention (Phase 5) Kickoff
- **Added**: Authored `docs/core/Epic_Phase5_Feedback_Loops_PRD.md` defining requirements for Mid-Execution Chat, Mandatory Approval Gates, and Error Escalation.
- **Status**: Initiated new epic based on `docs/core/Roadmap.md` Phase 5 goals. Ready for engineering kickoff.

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
