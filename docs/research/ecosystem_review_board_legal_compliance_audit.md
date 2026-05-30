# Phase 0: Ecosystem Review Board - Legal & Compliance Audit

**Date:** 2026-05-30
**Reviewer:** Legal Compliance Checker
**Target:** `agency-os` baseline repository (Template Finalization)

## Executive Summary
An audit of the baseline `agency-os` repository was conducted to identify legal, IP, and compliance gaps prior to template finalization and distribution. Several critical omissions were found that could expose downstream users and the template creators to liability or regulatory non-compliance.

## Identified Gaps (Must be fixed in Phase 1)

### 1. Missing Open-Source Licensing
- **Issue:** There is no `LICENSE` or `LICENSE.md` file in the root directory.
- **Risk:** Without an explicit open-source license (e.g., MIT, Apache 2.0), the code is under exclusive copyright by default, creating IP risks and usage ambiguity for anyone cloning the template. 
- **Recommendation:** Add a standard open-source `LICENSE` file to the repository root.

### 2. Missing Terms of Service & Privacy Policy Placeholders
- **Issue:** While a `terms_of_service_ugc.md` exists in the `docs/operations/` directory, there are no explicit placeholders or structural requirements (e.g., in the web client or root structure) prompting the deployer to provide their own public-facing Terms of Service or Privacy Policy.
- **Risk:** Deployers may launch the template without proper legal agreements covering User-Generated Content (UGC), AI-Generated Content (AIGC), and GDPR compliance.
- **Recommendation:** Add `TERMS_OF_SERVICE_TEMPLATE.md` and `PRIVACY_POLICY_TEMPLATE.md` to a visible location (or root), and ensure the frontend template includes footer links/placeholders for these documents.

### 3. Insufficient AI Safety & Compliance Constraints in Agent Configurations
- **Issue:** `config/agent_base.yaml` contains operational constraints but lacks explicit compliance, safety, and data privacy constraints.
- **Risk:** Agents may generate non-compliant outputs, exfiltrate Personally Identifiable Information (PII), or violate usage policies without explicit baseline boundaries.
- **Recommendation:** Update `config/agent_base.yaml` constraints to include explicit rules against PII mishandling, malicious generation, and require adherence to data privacy guidelines.

### 4. Data Retention Policies Not Codified in Configuration
- **Issue:** `docs/operations/data_governance_policy.md` mandates a 30-day TTL for logs and PII minimization. However, there are no corresponding environment variables or configuration placeholders in `config/` (or a `.env.example`) to technically enforce this policy.
- **Risk:** Deployers may violate GDPR storage limitation principles by indefinitely retaining logs and PII if the technical defaults don't mirror the written policy.
- **Recommendation:** Add configuration placeholders (e.g., `LOG_RETENTION_DAYS=30`, `PII_REDACTION_ENABLED=true`) to the baseline configuration templates to align technical defaults with the Data Governance Policy.

## Conclusion
These gaps must be addressed in Phase 1 to ensure the `agency-os-template` provides a legally sound, compliant, and safe foundation for end-users.