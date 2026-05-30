# AgencyOS Comprehensive Feature & Requirement Checklist

This document serves as the exhaustive checklist of all expected features and requirements for the entire AgencyOS application at the current stage, synthesized from the `docs/core/` directory.

## 1. Frontend Features & User Interface
- [ ] **Conversational UI:** Persistent, context-aware, chat-centric interface acting as the primary entry point for new projects and micro-tasks.
- [ ] **Split-Screen Review Component:** UI allowing users to view the chat alongside auto-updating, generated documents (Draft PRD, Tech Spec, Task List).
- [ ] **Custom Agent Creator Wizard:** Multi-step React frontend wizard to generate robust `agency-agents` compliant files for user-defined agents.
- [ ] **Execution Dashboard:** Real-time visual representation of active agents, their current tasks, and live logs.
- [ ] **Pod Orchestration UI:** Multi-Agent Chat Interface displaying collaborative Pod interactions (N:N agent communication).
- [ ] **Memory Inspector Panel:** UI component allowing users to inspect what agents recall from semantic memory.
- [ ] **Marketplace UI Components:** Foundational components (cards, grids, details) for sharing and discovering agents/pods.
- [ ] **Administration Settings:** Fully functional integration of RBAC, API Keys, and Audit Logs configuration.
- [ ] **Draft Projects:** Persistent chat state automatically saved if a user navigates away.
- [x] **Mid-Execution Chat:** Ability for users to chat with the Orchestrator while agents are working to intervene or redirect.
- [x] **Approval Gates UI:** Interactive prompts requiring explicit human approval before agents proceed to major phases.
- [x] **Error Escalation UI:** Automated alerts via chat with context and proposed solutions upon task failure.
- [x] **Template Library:** Start projects based on pre-defined templates (e.g., "SaaS Starter").
- [x] **Robust API Selector:** Advanced model selection including dynamic reasoning effort and model routing.
- [ ] **Voice Interface (Future Phase 6):** Voice-to-text input for initial project scoping.

## 2. Backend Capabilities & Orchestration
- [x] **LLM Runner Integration:** Connection of frontend chat UI to backend LLM engine (OpenAI/Anthropic) for basic conversational scoping and intent parsing.
- [x] **Auto-Scoping & Document Generation Engine:** Services to dynamically generate PRDs, Architecture Specs, and Task Checklists based on conversation.
- [x] **Document Ingestion Pipeline:** Parsing and extraction of requirements from uploaded documents (PDF, Markdown, TXT) to automatically seed the execution pipeline.
- [x] **Nexus Pipeline DAG Orchestration:** Translation of Markdown task lists into actionable Directed Acyclic Graphs (DAGs) for `central_runner.py`.
- [x] **Dynamic Agent Selection:** Automated mapping of tasks to appropriate specialized agents from the registry.
- [x] **Custom Agent CRUD API:** Complete lifecycle management API (`POST`, `PUT`, `DELETE` `/api/custom-agents/{agent_id}`) with rigorous validation.
- [x] **Message Broker Integration:** Redis Pub/Sub integration for asynchronous agent communication within Pods.
- [x] **Semantic Memory API:** Integration of a self-hosted Vector Database (`pgvector` via PostgreSQL) for agent memory retrieval and storage.
- [x] **DAG State Persistence:** Tracking workflow execution state in a `workflow_executions` database table for pause/resume capabilities and checkpointing.
- [x] **Real LLM Runtime Integration in DAG:** Execution of real LLM tasks within the orchestrator (replacing mock functions).
- [x] **DAG Resilience & Failure Handling:** Configurable retry logic with exponential backoff for transient errors, and graceful handling of partial node failures.
- [x] **Strict Context Schema Validation:** Pydantic schema validation enforced for inputs/outputs between agents/nodes.
- [x] **Decoupled Markdown Generation:** Markdown generation logic for custom agents separated into `agent_config_service.py`.
- [x] **Transactional Integrity:** Database changes roll back if associated file/storage write operations fail.
- [x] **Storage Abstraction Layer:** Support for scalable Cloud Storage (AWS S3) and local filesystem fallback with strict tenant isolation.

## 3. Infrastructure, Security, & DevOps Requirements
- [ ] **Multi-Tenancy & Workspaces:** Secure, logical isolation of data, projects, and resources per client/team.
- [ ] **Role-Based Access Control (RBAC):** Granular permission settings dictating human and agent access.
- [ ] **Comprehensive Audit Logging:** Immutable tracking of all human and agent actions.
- [ ] **Secure Execution Sandbox:** Isolated environments for agents to run scripts safely.
- [ ] **LLM Kill Switch & Blast Radius Containment:** Mechanisms to halt autonomous DAGs and contain potential run-away processes.
- [ ] **Blue-Green Deployment Infrastructure:** Declarative IaC (Terraform/Kubernetes YAMLs) supporting zero-downtime traffic cutover via Ingress Controllers/Load Balancers.
- [ ] **Automated Rollback Procedures:** Instant reversion capabilities to previous environments with backward-compatible (non-destructive) database migrations.
- [ ] **Observability & Monitoring Stack:** Prometheus for metrics (CPU, Memory, Latency), OpenTelemetry for distributed tracing, and Loki/ELK for centralized logging.
- [ ] **Automated Alerting:** Incident triggers (PagerDuty/Slack) configured for critical SLIs (e.g., >1% 5xx errors, >500ms API latency).
- [ ] **Scalable Storage Provisioning:** S3-compatible buckets with IAM roles granting scoped permissions (`s3:PutObject`, `s3:GetObject`, etc.) restricted to tenant prefixes.

## 4. Product Milestones, Testing & Quality Gates
- [ ] **Phase 3 Scalability Hardening:** Resilient DAG, Custom Agent S3 storage, transactional safety.
- [ ] **Phase 4 QA Gauntlet:** Load testing of message broker and vector DB, comprehensive E2E testing of Pod lifecycle, and security audits.
- [ ] **Phase 5 Go-to-Market (GTM) Launch:** Cross-channel activation, community seeding, production analytics tracking, and blue-green rollout.
- [ ] **Strict QA Gates:** Minimum 85% line coverage for modified services, 100% pass rate for integration/unit suites, zero static analysis errors.
- [ ] **Human-in-the-Loop Validation:** Explicit, documented human sign-off required for Phase handoffs, UAT, deployment cutovers, and strategic marketing launches.
- [ ] **Legal & Compliance Frameworks:** Implementation of Terms of Service, UGC Liability Frameworks, and GDPR policies.
