# Compliance & Data Privacy Audit Report: AgencyOS V2 "Build vs. Run" Paradigm

**Date:** 2026-05-28
**Auditor:** Legal Compliance Checker
**Documents Audited:**
1. `docs/research/twin_so_analysis/v2/build_vs_run_sandbox_spec.md`
2. `docs/research/twin_so_analysis/v2/studio_ui_user_journey.md`

## 1. Executive Summary
The proposed "Build vs. Run" architecture demonstrates a strong foundational understanding of environment isolation and secret management. The bifurcation between the Sandbox (Build) and Production (Run) environments significantly reduces the risk of accidental data leaks or unauthorized external API interactions during the development phase. However, significant compliance gaps exist regarding data retention, personally identifiable information (PII) handling, and access controls within the logging and caching mechanisms.

## 2. Key Findings & Compliance Risks

### 2.1. The Sandbox Environment (Build Mode)
*   **Positive Controls:** The implementation of "Secret Manager Masking," network isolation, and mocked API responses are robust security measures that protect production credentials and data.
*   **Risk - Semantic Caching (Redis):** The specification states that a Redis semantic cache will store "vector embeddings of recent user prompts." 
    *   *Compliance Issue:* Users (developers/prompt engineers) may inadvertently include PII or sensitive corporate data in their test prompts. Storing these embeddings without explicit Time-To-Live (TTL) expiration or PII scrubbing mechanisms violates data minimization principles (GDPR/CCPA).
*   **Risk - Trace View Data Exposure:** The Studio UI proposes a "Trace View overlay" that shows "intermediate tool payloads."
    *   *Compliance Issue:* Even in a mocked environment, test payloads might contain sensitive data structure information. If actual data is used for testing, this exposes it directly to the UI. There must be assurances that mocked payloads do not reflect real user data.

### 2.2. The Production Environment (Run Mode)
*   **Risk - Persistent State Management (PostgreSQL):** The specification mandates that "Execution state, memory, and intermediate tool outputs are persistently logged to the PostgreSQL database, ensuring traceability."
    *   *Compliance Issue:* This is the most critical privacy risk. Unfiltered, permanent logging of all AI agent interactions and tool outputs creates a massive liability. If an agent processes PII, PHI (HIPAA), or financial data, persisting this data in plain text violates multiple compliance frameworks.
    *   *Remediation Required:* Implement automated PII scrubbing before data is written to the execution logs. Establish strict, automated data retention policies (e.g., delete logs after 30/60/90 days unless legally required otherwise).

### 2.3. Operational & Governance Gaps
*   **Lack of Audit Trails for Promotion:** The "Promotion Flow" details versioning but lacks an explicit audit trail detailing *who* promoted an agent to production and *when*. This is necessary for SOC 2 and ISO 27001 compliance.
*   **Data Subject Access Requests (DSAR):** There is no mention of how the system will handle user requests to delete or retrieve their data from the persistent logs or semantic memory.

## 3. Required Remediation Plan

To ensure the "Build vs. Run" architecture meets legal and regulatory standards, the following features must be added to the engineering specifications:

1.  **Data Minimization & Retention:**
    *   Define strict TTLs for the Redis Semantic Cache.
    *   Implement an automated data lifecycle policy for the PostgreSQL persistent state logs (e.g., auto-deletion after a defined period).
2.  **Data Sanitization (PII Scrubbing):**
    *   Integrate a PII scrubbing service or middleware that redacts sensitive information from prompts before they are cached in Redis.
    *   Redact sensitive data from "intermediate tool outputs" before they are logged to PostgreSQL or displayed in the UI's Trace View.
3.  **Access Control & Audit Logging:**
    *   Implement Role-Based Access Control (RBAC) governing who can view the Trace View and execution logs.
    *   Record immutable audit logs for all "Promote to Production" actions, capturing the user ID, timestamp, and version deployed.
4.  **Compliance with DSAR:**
    *   Ensure all persistent storage (database and cache) is indexed in a way that allows for the extraction or deletion of specific user data to comply with "Right to be Forgotten" requests.

## 4. Conclusion
While the structural isolation of the Sandbox is commendable, the logging and caching mechanisms require immediate revision to prevent the system from becoming a repository of unmanaged sensitive data. Addressing the remediation plan before implementation begins will significantly reduce legal and compliance liabilities.