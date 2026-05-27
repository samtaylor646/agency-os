# Blue-Green Deployment Runbook

## 1. Objective
To execute a zero-downtime deployment for AgencyOS using a Blue-Green deployment strategy. This ensures that a new version (Green) can be fully tested in a production environment before live traffic is routed to it from the current version (Blue).

## 2. Prerequisites
- **Infrastructure as Code (IaC):** Production environment provisioned via Terraform/Kubernetes YAMLs.
- **Container Registry:** New Docker images are built and pushed to the container registry.
- **Backward-Compatible Database:** Ensure all database migrations applied to the Green environment are backward-compatible with the Blue environment.
- **Approvals:** Human validation gate (GTM & Launch Readiness Gate) must be signed off.

## 3. Preparation
1. **Verify Current State (Blue):**
   - Ensure the Blue environment is healthy and handling current traffic.
   - Monitor metrics (Prometheus/Grafana) for standard baselines.

2. **Deploy Green Environment:**
   - Deploy the new release alongside the active Blue environment.
   - In Kubernetes, deploy the Green Deployment, ConfigMaps, and Services.
   - Do NOT update the main Ingress controller yet.

## 4. Validation (Green)
1. **Health Checks:**
   - Verify all pods in the Green deployment are `Running` and `Ready`.
2. **Automated Testing:**
   - Execute automated end-to-end (E2E) test suites against the Green service endpoints.
3. **Manual Sanity Check:**
   - Operations and QA teams perform manual checks using a private Green URL or specific HTTP headers to route traffic to the Green environment.

## 5. Cutover (Traffic Switch)
1. **Human Sign-off:** Obtain explicit human sign-off immediately prior to the cutover.
2. **Update Routing:**
   - Update the load balancer or Ingress controller routing rules to point live traffic to the Green environment.
   - Example (Kubernetes Ingress): Change the `service.name` to point to the Green service.
3. **Monitor Transition:**
   - Monitor application metrics (latency, error rates, CPU/Memory) for any anomalies.
   - Watch logs for unexpected errors or trace spikes.

## 6. Post-Deployment
1. **Bake Period:**
   - Leave the Blue environment running for a defined "bake period" (e.g., 24-48 hours) to allow for instant rollback if issues arise.
2. **Decommission Blue:**
   - Once the Green environment is deemed stable and the bake period is over, scale down and remove the Blue environment resources to save costs.
   - The Green environment now becomes the new Blue for the next cycle.

## 7. Emergency
- If critical anomalies or SLI degradation occur post-cutover, immediately execute the [Rollback Runbook](./rollback_runbook.md).
