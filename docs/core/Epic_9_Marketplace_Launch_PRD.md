# Epic 9: Marketplace Launch & PRPM Integration PRD

## 1. Executive Summary
Epic 9 transitions AgencyOS from a closed ecosystem to a public marketplace, allowing users to share and monetize custom agents, workflows, and prompts via the PRPM (Package Repository & Package Manager) integration. To protect the platform from the existential risks introduced by User-Generated Content (UGC) and Cyclical DAG execution, strict security, infrastructure, and legal safeguards must be implemented prior to launch.

## 2. Strategic Objectives
*   **Launch Public Marketplace:** Enable community-driven growth and establish AgencyOS as the premier agent ecosystem.
*   **Establish Verified Creator Tier:** Seed the marketplace with high-quality, safe, and audited assets to prevent "asset dumping" and build user trust.
*   **Infrastructure Hardening (Read-Heavy Scale):** Protect the core application from OOM crashes and connection exhaustion caused by the new asynchronous architecture (Epic 8) under heavy read loads.
*   **Ecosystem Protection:** Enforce strict sandboxing, max-iteration caps, and kill switches to contain runaway API costs and malicious behavior.

## 3. Product Requirements

### 3.1. Legal, Compliance & Monetization
*   **ToS/EULA Gate:** Mandatory click-through agreement defining IP ownership and creator indemnification for malicious agents.
*   **Verified Creator Program:** Initial launch restricted to vetted creators to ensure quality control. Standard transparent revenue take-rates established.
*   **Enterprise Gating:** Advanced orchestration features like Cyclical DAGs and SSO must be gated behind Enterprise subscription plans.

### 3.2. Security & Blast Radius Containment
*   **Asset Signing & Validation:** Require cryptographic signing for `agents.md` assets. Perform Automated Static Analysis (SAST) before marketplace publication.
*   **Subresource Integrity (SRI):** Validate all packages pulled from `prpm.dev`.
*   **Cyclical DAG Circuit Breakers:** 
    *   Hard max-iteration caps to prevent infinite loops.
    *   TTL/Timeout locks for all DAG runs.
    *   Spend ceilings enforced per DAG run to prevent API token burn.
*   **Global Package Quarantine Switch:** Ability for administrators to instantly delist and recall compromised PRPM marketplace assets.

### 3.3. Infrastructure & Performance (The PgBouncer Strategy)
*   **Connection Multiplexing:** Deploy PgBouncer in `transaction` pooling mode to multiplex high-volume async client requests through a small, fixed pool of actual database connections.
*   **Read-Replica Routing:** Provision PostgreSQL Read Replicas and a dedicated PgBouncer instance to handle all `GET` marketplace queries, keeping the primary DB safe for writes.
*   **Failsafes & Observability:**
    *   Set `query_wait_timeout` to 5-10 seconds to return fast 503s rather than queueing requests indefinitely.
    *   Implement alerting on PgBouncer's `cl_waiting` (Client Waiting Queue) to trigger infrastructure scaling when the queue spikes.
    *   Migrate SOC2 audit logs from hot DB to cold S3 storage after 30-90 days to contain storage costs.

## 4. Prioritized Backlog (Upcoming Sprints)

### Sprint 1: Infrastructure & Hardening
*   [ ] Provision PostgreSQL Read Replicas for Marketplace traffic.
*   [ ] Deploy PgBouncer (Transaction Mode) & Configure App Routing (`GET` to Read Replicas).
*   [ ] Implement PgBouncer timeout configurations and `cl_waiting` alerting.
*   [ ] Implement Tiered Storage Strategy (S3 migration for old audit logs).

### Sprint 2: Ecosystem Protection & Security
*   [ ] Develop and enforce hard max-iteration caps and TTL/Timeouts for Cyclical DAGs.
*   [ ] Implement per-DAG spend ceilings.
*   [ ] Build Global Package Quarantine Switch.
*   [ ] Integrate SAST checks and Cryptographic Signing for `prpm.dev` uploads.
*   [ ] Enforce Subresource Integrity (SRI) on package downloads.

### Sprint 3: Legal, Quality Control & Launch Prep
*   [ ] Implement Click-through ToS/EULA flow for creators and users.
*   [ ] Develop "Verified Creator" onboarding flow, tagging, and curation tools.
*   [ ] Implement Enterprise Subscription gating for Cyclical DAGs & SSO.
*   [ ] Final UAT and Sign-off by Ecosystem Review Board.