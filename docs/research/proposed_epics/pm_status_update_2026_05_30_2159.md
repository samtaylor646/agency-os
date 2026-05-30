# Product Management Status Report - AgencyOS
**Date:** May 30, 2026

*This report incorporates the findings from the Ecosystem Review Board audit.*

## 1. What can AgencyOS do in a container environment?
Containerization is a mandatory core security feature for AgencyOS, utilizing a "Sidecar Pattern" detailed in [`docs/technical/Platform_Status_and_Containerization_Strategy.md`](../technical/Platform_Status_and_Containerization_Strategy.md):
* **Blast Radius Containment:** Custom agents spin up in isolated Docker containers (or gVisor/Firecracker microVMs), preventing malicious logic from accessing host files.
* **Network & Tool Isolation:** Enforces strict egress filtering so agents can only communicate with explicitly allowlisted APIs (e.g., `api.github.com`).
* **Resource Caps:** Implements hard CPU and memory limits to automatically throttle or kill agents stuck in infinite recursive loops.

## 2. What is needed to make this app standalone for enterprise or public usage?
AgencyOS is currently in Phase 4 (Quality & Hardening) and is **not** ready for a public release. To advance, we must pass the "Quality Gauntlet" and implement the safeguards mandated by the Ecosystem Review Board in [`docs/research/proposed_epics/Epic_9_Ecosystem_Review_Board_Audit.md`](./Epic_9_Ecosystem_Review_Board_Audit.md):
* **Infrastructure Hardening:** Deploy PgBouncer in transaction pooling mode and provision dedicated PostgreSQL Read Replicas to handle high-volume async marketplace traffic without DB connection exhaustion.
* **Legal & Compliance Gates:** Establish a mandatory "click-wrap" ToS/EULA that secures a royalty-free license for the platform to distribute assets, while strictly holding creators liable for malicious agents via indemnification.
* **Security & Trust Verification:** Require cryptographic asset signing for `agents.md`, enforce Automated Static Analysis (SAST) prior to marketplace publication, and utilize Subresource Integrity (SRI) for secure downloads.
* **Execution Circuit Breakers:** Implement max-iteration hard caps, per-DAG spend ceilings, and an administrative Global Package Quarantine Switch to instantly recall compromised assets.

## 3. What are the features we need?
Based on our active technical specs and the [`docs/research/proposed_epics/prd_epic_system_guardrails.md`](./prd_epic_system_guardrails.md):
* **System-Enforced Guardrails:** An `OrchestratorIsolationMiddleware` that physically prevents the orchestrator from writing code without proper delegation, transitioning our rules from `.clinerules` to hard-coded system constraints.
* **Mandatory HITL Checkpoints:** Programmatic stops requiring human approval before major phase transitions or code merges.
* **Enterprise Gating:** Restricting advanced capabilities like Cyclical DAG execution and SSO strictly behind higher-tier Enterprise subscription plans.
* **MCP Skills Architecture:** Completing Epic 7 to enable a Redis-backed Agent Upscaler that turns passive agents into active workers.

## 4. What are the features to consider?
* **Verified Creator Tiering:** A vetting program (KYC, historical metrics, SLAs) for marketplace creators to prevent "asset dumping" and build enterprise trust, as outlined in the Business Strategy audit.
* **Standardized Guardrail Exports:** Exporting our middleware logic to external tools (like Kinetik OS) to ensure uniform agent behavior across ecosystems, detailed in [`docs/research/proposed_epics/kinetik_export_guardrails.md`](./kinetik_export_guardrails.md).
* **Automated Data Lifecycle Policy:** Transitioning "hot" SOC2 audit logs to cold S3 storage after 30-90 days to contain database costs.

## 5. What is in the research pipeline that needs to be considered for more work or move to a feature backlog?
The following documents have now been reviewed by the Ecosystem Review Board and are ready for final human approval to transition from `docs/research/proposed_epics/` into the active development backlog (`docs/core/`):
* **Epic 9 Marketplace Launch PRD:** [`docs/research/proposed_epics/Epic_9_Marketplace_Launch_PRD.md`](./Epic_9_Marketplace_Launch_PRD.md)
* **Epic 9 Ecosystem Review Board Audit:** [`docs/research/proposed_epics/Epic_9_Ecosystem_Review_Board_Audit.md`](./Epic_9_Ecosystem_Review_Board_Audit.md)
* **System Guardrails Epic:** [`docs/research/proposed_epics/prd_epic_system_guardrails.md`](./prd_epic_system_guardrails.md)
* **Template Finalization Draft:** [`docs/research/proposed_epics/epic_agency_os_template_finalization.md`](./epic_agency_os_template_finalization.md)
