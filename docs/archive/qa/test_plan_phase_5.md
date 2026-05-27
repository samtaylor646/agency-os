# E2E Test Plan & HITL Verification: Phase 5 (Launch & Growth)

## 1. Executive Summary
This document outlines the End-to-End (E2E) Test Plan and Human-in-the-Loop (HITL) verification steps for Phase 5. The primary objective is to validate production readiness, specifically focusing on blue-green deployment cutovers, rollback procedures, and strict adherence to data privacy compliance (GTM pixel consent barriers).

## 2. Testing Objectives
- **Zero-Downtime Deployment:** Validate the blue-green deployment strategy to ensure continuous availability during production rollout.
- **Rollback Integrity:** Ensure instant and safe reversion to the previous state without data loss or corruption if the new deployment fails.
- **Compliance & Privacy:** Verify that marketing and analytics tracking pixels (GA4, PostHog, Meta, Twitter) remain inactive until explicit user consent is granted.
- **HITL Checkpoints:** Formalize human validation gates required before critical production actions are executed.

## 3. E2E Test Scenarios

### 3.1. Blue-Green Cutover Test
**Objective:** Verify seamless traffic transition from the Blue (current) environment to the Green (new) environment.

**Test Steps:**
1.  **Preparation:** Deploy the new release to the isolated Green environment.
2.  **Health Check:** Run automated health checks (API endpoints, UI rendering, DB connectivity) against the Green environment.
3.  **Cutover Execution:** Trigger the DNS/Load Balancer switch to route traffic from Blue to Green.
4.  **Verification:**
    -   Monitor live traffic using Prometheus and Grafana.
    -   Verify error rates (5xx) remain below the 1% threshold.
    -   Verify application latency remains under 500ms.
    -   Confirm users maintain active sessions during the cutover.
5.  **Success Criteria:** Traffic successfully routes to the Green environment with zero downtime, no spike in error rates, and stable performance metrics.

### 3.2. Rollback State Integrity Test
**Objective:** Validate the ability to quickly revert to the Blue environment if the Green deployment introduces critical issues, ensuring backward compatibility.

**Test Steps:**
1.  **Preparation:** Assume the system is running on the Green environment following a cutover.
2.  **Simulated Failure:** Inject a simulated critical failure (e.g., elevated error rates or broken critical path).
3.  **Rollback Execution:** Trigger the immediate reversion via the ingress controller to route traffic back to the Blue environment.
4.  **Verification:**
    -   Confirm traffic is successfully routed back to Blue.
    -   Verify the database state remains consistent and intact (confirming non-destructive migrations).
    -   Ensure telemetry indicates a return to normal operational baselines.
5.  **Success Criteria:** System successfully reverts to the Blue environment instantly, resolving the simulated failure without data loss or corruption.

### 3.3. Compliance & GTM Pixel Consent Barrier Test
**Objective:** Verify that no marketing or analytics tracking scripts execute before receiving explicit user consent, complying with GDPR and CCPA.

**Test Steps:**
1.  **Initial Load:** Navigate to the application in a clean browser session (no existing cookies).
2.  **Verification (Pre-Consent):**
    -   Inspect network traffic and browser console.
    -   Confirm no requests are made to GA4, PostHog, Meta, Twitter, or any other GTM tracking domains.
    -   Confirm no related cookies are set.
3.  **Action (Grant Consent):** Interact with the Cookie Consent Management Platform (CMP) to explicitly grant consent (Opt-In).
4.  **Verification (Post-Consent):**
    -   Inspect network traffic.
    -   Confirm tracking pixels (GA4, PostHog, Meta, Twitter) now fire successfully.
    -   Verify appropriate cookies are set.
5.  **Action (Revoke Consent / Opt-Out):** Access privacy settings and revoke consent or trigger a "Do Not Sell" signal.
6.  **Verification (Post-Revocation):**
    -   Refresh the application.
    -   Confirm tracking pixels no longer fire and related tracking cookies are removed or invalidated.
7.  **Success Criteria:** GTM pixels are strictly blocked by default, only activating upon explicit consent, and correctly deactivating upon revocation.

## 4. Human-in-the-Loop (HITL) Verification Steps
To adhere to the HITL mandate, the following manual validation gates must be signed off by designated stakeholders.

### 4.1. Pre-Deployment Validation Gate
-   [ ] **Action:** Review staging test results, including the simulated blue-green cutover and rollback tests.
-   [ ] **Action:** Confirm all automated tests (unit, integration, E2E) pass.
-   [ ] **Action:** Review and approve the final production configuration.
-   **Sign-off:** DevOps Lead & Release Manager.

### 4.2. Cutover Authorization Gate
-   [ ] **Action:** Review real-time metrics of the Green environment before routing production traffic.
-   [ ] **Action:** Explicitly authorize the DNS/Load Balancer switch.
-   **Sign-off:** Incident Commander / DevOps Lead.

### 4.3. Marketing & GTM Go-Live Gate
-   [ ] **Action:** Review finalized marketing collateral, positioning matrices, and scheduled content.
-   [ ] **Action:** Explicitly authorize the activation of cross-channel marketing campaigns.
-   **Sign-off:** Product Marketing Manager.

### 4.4. Compliance Audit Verification Gate
-   [ ] **Action:** Perform manual inspection of the application to verify the GTM pixel consent barrier operates as described in Test Scenario 3.3.
-   [ ] **Action:** Verify OpenTelemetry traces and Promtail logs are actively scrubbing PII.
-   **Sign-off:** Legal & Compliance Officer / Evidence Collector.

## 5. Next Steps
1.  Distribute this test plan to the QA and DevOps teams.
2.  Execute test scenarios on the staging environment.
3.  Document all test results and secure HITL sign-offs prior to production launch.
