# QA Test Scripts: Epic 6 (Launch & Operate)

## 1. Introduction
This document contains the detailed step-by-step test scripts for validating the features developed in Epic 5 before the platform's full launch in Epic 6. The primary focus areas are the Agent Template Marketplace, Enhanced Role-Based Access Control (RBAC), Advanced Analytics, and Audit Logging.

All tests should be executed against the staging environment before proceeding to production.

---

## 2. API & Integration Test Scripts

### 2.1 Role-Based Access Control (RBAC) & Auth
**Objective:** Validate that the dynamic roles and permission flags correctly secure API endpoints.

| Test ID | Description | Pre-conditions | Steps | Expected Result |
|---|---|---|---|---|
| `API-RBAC-01` | Test API access with valid `admin` role | User has `admin` role | 1. `GET /api/workspaces/{id}` with Admin token. | HTTP `200 OK`. JSON response contains workspace details. |
| `API-RBAC-02` | Test restricted API access (Missing Permission) | User has `viewer` role (missing `execute:agent` permission) | 1. `POST /api/orchestration/trigger` with Viewer token. | HTTP `403 Forbidden`. JSON error message specifies missing `execute:agent` permission. |
| `API-RBAC-03` | Create Custom Role | User has `admin` role | 1. `POST /api/rbac/roles` with payload: `{"name": "Billing Manager", "permissions": ["view:billing", "view:analytics"]}`. | HTTP `201 Created`. Role ID returned. |
| `API-RBAC-04` | Test Custom Role Access | User is assigned `Billing Manager` role | 1. `GET /api/analytics` (Authorized).<br>2. `POST /api/orchestration/trigger` (Unauthorized). | 1. HTTP `200 OK`.<br>2. HTTP `403 Forbidden`. |

### 2.2 Analytics Metrics
**Objective:** Validate that the system correctly records and retrieves agent execution metrics.

| Test ID | Description | Pre-conditions | Steps | Expected Result |
|---|---|---|---|---|
| `API-ANLY-01` | Record Agent Execution Metric | System running | 1. Trigger an agent execution via CentralRunner.<br>2. Wait for completion.<br>3. Query DB for new `AgentExecutionMetric` record. | Record exists with `duration_seconds > 0` and accurate `token_usage` counts. |
| `API-ANLY-02` | Retrieve Aggregated Analytics | Executions exist in DB | 1. `GET /api/analytics/workspace/{id}?timeframe=7d`. | HTTP `200 OK`. JSON payload contains aggregated totals for executions, tokens, and duration. |
| `API-ANLY-03` | Export Analytics Data | Executions exist in DB | 1. `GET /api/analytics/export?format=csv`. | HTTP `200 OK`. Content-Type is `text/csv`. Data matches DB metrics. |

### 2.3 Audit Logger Integrity
**Objective:** Validate that sensitive actions generate immutable audit logs.

| Test ID | Description | Pre-conditions | Steps | Expected Result |
|---|---|---|---|---|
| `API-AUDIT-01` | Log Role Modification | User has `admin` role | 1. `PUT /api/rbac/roles/{id}` to modify a role's permissions. | 1. HTTP `200 OK`.<br>2. `GET /api/audit` shows a new `AuditLog` entry with action `UPDATE_ROLE`, the correct `user_id`, and a valid timestamp. |
| `API-AUDIT-02` | Log User Deletion | User has `admin` role | 1. `DELETE /api/users/{id}` to delete a user from the workspace. | 1. HTTP `200 OK` or `204 No Content`.<br>2. `GET /api/audit` shows a new `AuditLog` entry with action `DELETE_USER`. |

### 2.4 Agent Template Marketplace
**Objective:** Validate the retrieval and cloning of templates.

| Test ID | Description | Pre-conditions | Steps | Expected Result |
|---|---|---|---|---|
| `API-MKT-01` | List Templates | None | 1. `GET /api/marketplace/templates`. | HTTP `200 OK`. JSON array of available base templates (e.g., SEO Auditor). |
| `API-MKT-02` | Clone Template | Valid workspace ID | 1. `POST /api/marketplace/templates/{template_id}/clone` with payload `{"workspace_id": 123}`. | HTTP `201 Created`. Returns new workspace-specific agent configuration. |

---

## 3. End-to-End UI Test Scripts

### 3.1 Agent Template Marketplace Flow
**Objective:** Verify a user can seamlessly discover and install a new agent template.

| Test ID | Steps | Expected Result | Testing Data |
|---|---|---|---|
| `UI-MKT-01` | 1. Navigate to `/marketplace`.<br>2. View the list of available templates.<br>3. Click "View Details" on the "SEO Auditor" template.<br>4. Click "Install to Workspace".<br>5. Select target Workspace and confirm.<br>6. Navigate to Agency Panel `/agency`. | 1. Marketplace loads.<br>2. Templates are displayed.<br>3. Modal opens with details.<br>4. Success toast appears.<br>5. "SEO Auditor" is listed in the Agency Panel under active agents. | Target Workspace: "Test Agency Alpha" |

### 3.2 Enhanced RBAC Manager
**Objective:** Verify admins can manage custom roles and users accurately experience permission restrictions.

| Test ID | Steps | Expected Result | Testing Data |
|---|---|---|---|
| `UI-RBAC-01` | **Admin Session:**<br>1. Navigate to `/rbac-manager`.<br>2. Click "Create Role". Name it "Read Only Analyst" and assign only `view:analytics` permission.<br>3. Assign role to Test User.<br>**Test User Session:**<br>4. Log in as Test User.<br>5. Navigate to Agency Panel.<br>6. Attempt to edit an agent's prompt. | 1. Role is saved successfully.<br>2. Test User's role is updated.<br>3. Agency Panel loads.<br>4. "Edit" buttons are hidden or disabled. If forced via URL, a 403 error page or toast is displayed. | Role: "Read Only Analyst", Permissions: `["view:analytics"]` |

### 3.3 Analytics Dashboard
**Objective:** Verify charts and metrics render correctly based on backend data.

| Test ID | Steps | Expected Result | Testing Data |
|---|---|---|---|
| `UI-ANLY-01` | 1. Execute a test task via the CentralRunner (e.g., Generate a short summary).<br>2. Wait for completion.<br>3. Navigate to `/analytics`.<br>4. Select "Last 24 Hours" from the timeframe dropdown.<br>5. Review the "Total Executions" counter and "Token Usage" chart. | 1. Dashboard loads successfully.<br>2. "Total Executions" counter increments by 1.<br>3. The "Token Usage" chart displays a new data point for the recent execution. | Timeframe: "Last 24 Hours" |

### 3.4 Audit Log Viewer
**Objective:** Verify workspace administrators can review the chronological history of critical actions.

| Test ID | Steps | Expected Result | Testing Data |
|---|---|---|---|
| `UI-AUDIT-01` | 1. As an Admin, change the permissions of a role in the RBAC Manager.<br>2. Navigate to `/audit-logs`.<br>3. Search or filter for "Action: UPDATE_ROLE". | 1. Audit Log Viewer loads a table of events.<br>2. The top row (most recent) displays the `UPDATE_ROLE` action, matching the exact time of the change and the Admin's email address. | Filter: "Action: UPDATE_ROLE" |

---

## 4. Operational & Deployment Verification

### 4.1 System Metrics & Monitoring
**Objective:** Verify that the system is properly wired for operational observability.

| Test ID | Steps | Expected Result |
|---|---|---|
| `OPS-MON-01` | 1. Check Datadog/Grafana (or configured log aggregator).<br>2. Query for application logs originating from the staging environment.<br>3. Query for custom metrics (e.g., `agencyos.task.duration`). | 1. Application logs stream in near real-time.<br>2. Custom metrics are plotting correctly on dashboards. |

### 4.2 CI/CD & Docker Deployment
**Objective:** Validate that containerization works as intended.

| Test ID | Steps | Expected Result |
|---|---|---|
| `OPS-DEP-01` | 1. Run `docker-compose -f deployment/docker-compose.yml up --build` locally or on the staging server. | 1. Images build without errors.<br>2. Server and Client containers start.<br>3. Platform is accessible via `localhost:8000` (API) and `localhost:5173` (Client). |
