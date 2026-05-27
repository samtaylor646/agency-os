# Changelog

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
