# Rollback Runbook

## 1. Objective
To rapidly restore AgencyOS service to a known good state (the Blue environment) in the event of critical failures, degraded Service Level Indicators (SLIs), or major user-facing bugs detected post-cutover to the Green environment.

## 2. Trigger Conditions
Execute this runbook if any of the following occur during or immediately after the Blue-Green cutover:
- Error rates (HTTP 5xx) exceed 1% over a 5-minute window.
- API latency exceeds 500ms for P90 over a 5-minute window.
- Critical multi-agent pipelines fail continuously.
- Container crash loop backoffs detected in the Green environment.
- Explicit human decision based on visual/manual QA failure post-launch.

## 3. Instant Reversion Procedure (App-Level Rollback)
Because the Blue environment is kept running during the "bake period" after a Blue-Green deployment, rollback is primarily a traffic routing operation.

1. **Update Routing:**
   - Immediately update the load balancer or Ingress controller routing rules to point live traffic back to the Blue environment.
   - Example (Kubernetes Ingress): Revert the `service.name` to point back to the Blue service.
2. **Verify Traffic Flow:**
   - Check load balancer metrics to confirm traffic is flowing to Blue pods.
   - Verify that Error Rates and Latency metrics begin to stabilize and return to baseline.

## 4. Database Reversion (Data-Level Rollback)
*Note: Our deployment strategy requires database migrations to be backward-compatible for at least one release cycle. Therefore, application-level rollback (Step 3) usually does not require database rollback.*

If a destructive or incompatible database change was accidentally deployed and caused the failure:
1. **Identify the Migration:** Identify the specific schema change or migration script that caused the issue.
2. **Execute Down Migration:**
   - Run the designated "down" migration script to revert the database schema to the previous state.
   - Example: `npm run migrate:undo` or `alembic downgrade -1`.
3. **Verify Data Integrity:** Ensure no critical user data generated during the Green window was lost or corrupted during the schema reversion. (Use database backups if necessary).

## 5. Post-Rollback Actions
1. **Quarantine Green:**
   - Do NOT immediately delete the failing Green environment.
   - Isolate it (e.g., remove from any internal routing) to allow developers to inspect logs, memory dumps, and traces to identify the root cause.
2. **Incident Report:**
   - Incident Response Commander initiates a blameless post-mortem.
   - Document the timeline, trigger conditions, root cause analysis, and remediation steps.
3. **Notify Stakeholders:**
   - Inform the engineering team, product managers, and human reviewers that a rollback occurred and deployment is halted until the root cause is resolved.

## 6. Restarting Deployment
- Once the root cause is identified and fixed, a new release candidate (e.g., Green-v2) must go through the entire CI/CD pipeline, automated testing, and human validation gates before attempting another Blue-Green cutover.
