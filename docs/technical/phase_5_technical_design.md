# Technical Design Document: Phase 5 - Launch & Growth

## 1. Executive Summary
This document outlines the technical architecture for Phase 5 (Launch & Growth), satisfying the requirements mapped out in `docs/core/prd_phase_5.md`. The core focus of this technical design is to guarantee a zero-downtime launch, high-fidelity observability, and a safe, backward-compatible rollback posture. This includes detailing the Blue-Green deployment architecture, integrating Prometheus/Grafana and OpenTelemetry, and strict guidelines for database backward compatibility.

## 2. Blue-Green Deployment Architecture

The deployment pipeline is orchestrated to ensure the application experiences zero downtime during updates, utilizing a declarative IaC model across Kubernetes and Terraform.

### 2.1 Infrastructure Layout
*   **Dual Environments:** At any time during the deployment cycle, two identical production environments (Blue and Green) coexist within the Kubernetes cluster. 
    *   **Blue:** Currently handling live user traffic.
    *   **Green:** Newly deployed version handling pre-release automated/manual testing traffic.
*   **Ingress & Routing:** The primary point of traffic control is the Kubernetes Ingress Controller (e.g., NGINX or AWS ALB). It routes external traffic to the appropriate service. 

### 2.2 Cutover Workflow
1.  **Deployment:** CI/CD pipeline deploys the new release artifact (Green) and its corresponding ConfigMaps/Services into the cluster alongside Blue.
2.  **Internal Testing:** 
    *   Traffic is routed to Green via specialized HTTP headers (e.g., `X-Environment: green`) or a dedicated private URL. 
    *   Automated End-to-End (E2E) suites validate the deployment.
3.  **Human Gate:** Explicit manual approval must be logged before live traffic is shifted.
4.  **Traffic Switch (The Cutover):** The Ingress configuration is updated dynamically (e.g., swapping the `service.name` selector from `agencyos-blue-svc` to `agencyos-green-svc`). Traffic shifts instantly.
5.  **Bake Period:** The Blue environment remains active and untouched for 24-48 hours. If critical SLIs trigger alarms, an instantaneous Ingress rollback to Blue is executed. Decommissioning of Blue only occurs post-bake period.

## 3. Database Backward-Compatibility & Rollback Safety

The most significant risk during a Blue-Green deployment is data structure drift between the two versions. To facilitate instantaneous traffic routing rollbacks without risking data loss or requiring complex database restorations, we enforce strict backward compatibility.

### 3.1 Non-Destructive Migrations Mandate
All database migrations for a given release MUST be strictly additive. They must be compatible with **both** the currently running code (Blue) and the newly deploying code (Green).
*   **Allowed Operations:** Adding tables, adding nullable columns, adding indexes.
*   **Prohibited Operations:** Renaming tables, renaming columns, deleting tables, dropping columns, altering column types.
*   **Multi-Phase Deprecation:** If a column must be dropped or renamed, it requires a 3-release cycle:
    1.  *Release N:* Add the new column, write to both columns, read from the old.
    2.  *Release N+1:* Read from the new column, write to both. Backfill data.
    3.  *Release N+2:* Remove the old column.

### 3.2 Data-Level Rollback Procedures
*   Because migrations are additive, an application-level rollback (re-pointing the Ingress to Blue) handles 99% of failures safely. Blue simply ignores the new, unused columns added by Green.
*   In the event of an actively harmful/destructive database error escaping the pipeline, explicit down-migrations (e.g., `alembic downgrade -1` or `npm run migrate:undo`) are required.

## 4. Observability & Monitoring Integrations (Prometheus & Grafana)

To establish real-time feedback loops and incident response triggers for the Phase 5 GTM launch, we employ a unified observability stack.

### 4.1 Telemetry Collection
*   **Metrics:** Prometheus natively scrapes node exporters, kube-state-metrics, and the AgencyOS application `/metrics` endpoints.
*   **Distributed Tracing:** OpenTelemetry (OTel) SDKs are instrumented in the backend to pass trace IDs across microservices and agents, providing deep visibility into Nexus Pipeline latency.
*   **Logs:** Promtail/Loki handles centralized log aggregation, perfectly correlating with Prometheus metric spikes.

### 4.2 Key Alerting Thresholds (Alertmanager)
Alerts are dynamically routed to PagerDuty and Slack channels for the Incident Response Commander.
*   **Critical Alerts (Page):**
    *   HTTP 5xx Error Rate > 1% over a 5-minute rolling window.
    *   API Latency P99 > 1000ms for 5 minutes.
    *   Database connection drops or exhaustion.
*   **Warning Alerts (Slack Only):**
    *   API Latency P95 > 500ms.
    *   Sudden traffic spikes (3x over a 1-hour average).

### 4.3 Analytics Dashboards
Grafana serves as the single pane of glass, featuring three core launch dashboards:
1.  **Executive Launch Dashboard:** Concurrent connections, active Multi-Agent pipelines, and high-level health.
2.  **Infrastructure Deep-Dive:** Pod/Node utilization (CPU/Mem/Disk I/O), Database metrics (Query wait times, connection pools).
3.  **LLM Telemetry:** Monitoring token consumption (cost approximations), rate-limit events, and OpenAI/Anthropic API latency.

## 5. Security & Human-in-the-Loop Validation

As outlined in the standard rules and protocols:
*   No deployment to Green will happen without CI/CD test gates passing.
*   No cutover to Green will occur without explicit, documented Human-in-the-Loop sign-off on visual and functional QA.
*   GTM pixel integrations (GA4, PostHog, Meta, Twitter) are isolated from core backend processes to prevent UI tracking scripts from creating application-level memory leaks or latency.
