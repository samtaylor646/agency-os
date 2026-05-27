# Production Analytics & Monitoring Specification

## 1. Overview
This specification details the production analytics, infrastructure monitoring alerts, and Go-To-Market (GTM) tracking pixels required for the Sprint 5.2 Launch of AgencyOS. It aligns with the Phase 5 Master Plan requirements to establish real-time analytics dashboards, monitor system health, and measure the effectiveness of simultaneous cross-channel marketing campaigns.

## 2. Infrastructure & Application Monitoring (Prometheus/Grafana)
We will utilize Prometheus for robust metrics collection and Grafana for visualization dashboards, ensuring high visibility into the blue-green deployment.

### 2.1 Core Infrastructure Metrics (SLIs)
*   **Node/Pod Resource Utilization:** CPU, Memory, and Disk I/O across the Kubernetes cluster.
*   **Network Traffic:** Ingress and egress bandwidth monitoring to detect anomalies or DDoS attempts.
*   **Database Connection Pools:** Monitor active connections, wait times, and query latency.

### 2.2 Application Performance Metrics
*   **API Latency:** Track 50th, 95th, and 99th percentile response times for all core endpoints.
*   **HTTP Error Rates:** Continuously monitor 4xx and 5xx HTTP status codes.
*   **Container Health:** Track container restarts, CrashLoopBackOff states, and Out-Of-Memory (OOM) kills.

### 2.3 Nexus Pipeline & Multi-Agent Metrics
*   **Pipeline Execution Time:** Average duration from task initiation to completion.
*   **Agent Handoff Success Rate:** Monitor the success/failure rate of context passing between specialized agents.
*   **LLM Provider Metrics:** Track API latency, rate limit hits, and token consumption (cost approximation) across OpenAI/Anthropic integrations.

## 3. GTM & Marketing Analytics (Tracking Pixels)
To accurately measure the effectiveness of the Cross-Channel Activation Strategy outlined in the GTM plan, we must deploy comprehensive tracking pixels and analytics tools.

### 3.1 Primary Analytics Platforms
*   **Google Analytics 4 (GA4):** Core web traffic analytics, session duration, bounce rates, and broad conversion funnels from the landing page.
*   **PostHog (or Mixpanel):** Deep product analytics tracking specific user actions (e.g., "Time-to-first-project-execution", "Number of agents utilized").

### 3.2 Channel-Specific Tracking Implementations
All URLs shared during launch must use standardized UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`).

*   **Twitter/X Pixel:** Track conversions specifically originating from our launch threads and "Automate Everything" messaging.
*   **Reddit Pixel:** Measure the quality and conversion rate of traffic driven by technical deep-dives in subreddits like r/devops and r/SaaS.
*   **Meta (Instagram) Pixel:** Track engagement and sign-ups resulting from high-impact UI/UX visual demonstrations.
*   **Bilibili / Xiaohongshu Tracking:** Utilize platform-specific conversion tracking mechanisms and strictly enforced UTM parameters to measure APAC market penetration from video shorts and multi-agent workflow visualizations.

## 4. Alerting Thresholds & Incident Response
Automated alerts must be configured via Alertmanager to trigger notifications in Slack and PagerDuty for the Incident Response Commander.

### 4.1 Critical Alerts (PagerDuty + Slack)
Requires immediate intervention and potential rollback from Green to Blue environment.
*   **High Error Rate:** 5xx HTTP Error Rate > 1% over a 5-minute rolling window.
*   **Severe Latency:** API 99th percentile latency > 1000ms for 5 minutes.
*   **Database Unavailability:** Database connection failures or latency spikes.
*   **Pipeline Failure:** Nexus Pipeline systemic failure rate > 10% across active users.

### 4.2 Warning Alerts (Slack Only)
Requires investigation but not immediate emergency response.
*   **Elevated Latency:** API 95th percentile latency > 500ms.
*   **Traffic Spike:** Sudden 3x increase in ingress traffic compared to the rolling 1-hour average.
*   **GTM Pixel Drop-off:** Zero conversion events recorded by tracking pixels within a 1-hour window during peak launch times (indicates potential tracking failure).

## 5. Post-Launch Dashboards
The Analytics Reporter and DevOps Engineer will ensure the following Grafana dashboards are staged and verified before the Go-Live Gate:

1.  **Executive Launch Dashboard:** High-level system health, concurrent active users, and global pipeline success rates.
2.  **GTM Conversion Dashboard (GA4/PostHog):** Real-time tracking of traffic sources, sign-ups, and the primary "Waitlist to Active Beta" conversion funnel.
3.  **Infrastructure Deep-Dive Dashboard:** Detailed pod-level metrics, database query traces, and latency histograms for root-cause analysis.
