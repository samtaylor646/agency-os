# AgencyOS: User Roles, Journeys, and HITL Testing Guide

This document outlines the core user roles within AgencyOS, maps their primary journeys, and provides a comprehensive, step-by-step guide for performing Human-in-the-Loop (HITL) quality assurance testing using direct API interactions.

---

## 1. User Roles

AgencyOS implements a strict Role-Based Access Control (RBAC) system. The core roles include:

1. **Platform Administrator (`admin`)**
   - **Capabilities:** Full system access. Can create workspaces, manage billing, configure system-wide kill switches, audit logs, and assign user roles.
   - **Primary Focus:** Security, compliance, and workspace provisioning.

2. **Agent Developer / Orchestrator (`developer`)**
   - **Capabilities:** Can create, configure, and modify Custom Agents, construct Directed Acyclic Graphs (DAGs) for Pipelines, and manage marketplace assets.
   - **Primary Focus:** Building and testing agent workflows and pipeline orchestration.

3. **Project Manager / Operator (`manager`)**
   - **Capabilities:** Can trigger pipelines, manage project tracking, interact with chat scopes, and—critically—approve or reject Human-in-the-Loop (HITL) gates.
   - **Primary Focus:** Overseeing agent task execution and providing domain expertise for HITL approvals.

4. **Observer (`viewer`)**
   - **Capabilities:** Read-only access to analytics, audit logs, and completed pipeline outputs.
   - **Primary Focus:** Monitoring performance and outcomes without execution rights.

---

## 2. User Journeys

### Journey A: Workspace Setup & Role Assignment
**Actor:** Platform Administrator
1. Logs into the platform.
2. Navigates to Workspace Settings.
3. Provisions a new workspace.
4. Invites team members and assigns RBAC profiles (e.g., assigning a user to the `developer` role).

### Journey B: Pipeline Construction & HITL Gate Configuration
**Actor:** Agent Developer
1. Selects specialized agents (e.g., `testing-evidence-collector`, `frontend-developer`).
2. Constructs a workflow pipeline.
3. Explicitly inserts a **HITL Approval Gate** between the build phase and the deployment phase.
4. Saves and publishes the pipeline to the workspace.

### Journey C: Execution & HITL Approval (The Core Loop)
**Actor:** Project Manager
1. Triggers the published pipeline.
2. Monitors the execution viewer as agents perform their tasks.
3. Pipeline pauses at the configured **HITL Approval Gate**.
4. Reviews the generated artifact (e.g., design document or code commit).
5. Provides explicit consent (Approve/Reject) with optional feedback.
6. Pipeline resumes or routes to a remediation loop based on input.

---

## 3. HITL (Human-in-the-Loop) Testing Guide

This section provides explicit instructions for QA teams to validate the RBAC policies and HITL gates. These scripts assume the AgencyOS backend is running locally on `http://localhost:8000`.

### Prerequisites: Authentication Setup

First, generate authentication tokens for our test personas. We will use a script to simulate logging in as an Admin and a Manager.

```bash
#!/bin/bash
# test_auth_setup.sh - Setup tokens for QA

BASE_URL="http://localhost:8000"

# 1. Login as Admin to get Admin Token
ADMIN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin@agencyos.dev", "password": "securepassword123"}' | jq -r .access_token)

echo "Exporting Admin Token..."
export ADMIN_TOKEN="$ADMIN_TOKEN"

# 2. Login as Manager to get Manager Token
MANAGER_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "pm@agencyos.dev", "password": "securepassword123"}' | jq -r .access_token)

echo "Exporting Manager Token..."
export MANAGER_TOKEN="$MANAGER_TOKEN"
```

### Step 1: Validate RBAC Restrictions on Pipeline Creation

Ensure that a Project Manager *cannot* create a new custom pipeline (only Developers/Admins should).

**Test Script:**
```bash
#!/bin/bash
# Test Manager Pipeline Creation (Should Fail - 403 Forbidden)

curl -s -X POST "http://localhost:8000/api/pipelines/create" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Unauthorized Pipeline",
        "steps": [{"agent": "researcher", "action": "scrape"}]
      }' -w "\nHTTP Status: %{http_code}\n"
```
*Expected Result:* HTTP 403 Forbidden.

### Step 2: Trigger a Pipeline with a HITL Gate

Use the Admin token (or Developer token) to trigger a pre-configured test pipeline that contains a mandatory HITL gate.

**Test Script:**
```bash
#!/bin/bash
# Trigger pipeline execution and capture the Execution ID

EXECUTION_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/pipelines/run" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pipeline_id": "test-hitl-pipeline-001"}')

EXECUTION_ID=$(echo $EXECUTION_RESPONSE | jq -r .execution_id)
echo "Pipeline triggered. Execution ID: $EXECUTION_ID"
export EXECUTION_ID="$EXECUTION_ID"
```

### Step 3: Verify the Pipeline Halts at the HITL Gate

Poll the execution status to confirm that the pipeline has paused and is explicitly waiting for human input.

**Test Script:**
```bash
#!/bin/bash
# Check status of the pipeline

curl -s -X GET "http://localhost:8000/api/pipelines/execution/$EXECUTION_ID/status" \
  -H "Authorization: Bearer $MANAGER_TOKEN" | jq .

# Expected Output snippet:
# {
#   "status": "PAUSED_PENDING_HITL",
#   "pending_gate_id": "gate-review-001",
#   "artifact_url": "/api/documents/artifact-123"
# }
```

### Step 4: Execute the HITL Approval

As a Project Manager, review the artifact and send the explicit approval payload to unlock the gate and allow the pipeline to proceed.

**Test Script:**
```bash
#!/bin/bash
# Approve the HITL Gate

curl -s -X POST "http://localhost:8000/api/pipelines/execution/$EXECUTION_ID/hitl-approve" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "gate_id": "gate-review-001",
        "decision": "APPROVED",
        "feedback": "The generated tests look correct. Proceed to merge.",
        "reviewer_id": "pm@agencyos.dev"
      }'
```
*Expected Result:* HTTP 200 OK. Output should indicate `status: RESUMED`.

### Step 5: Verify Pipeline Completion

Check the pipeline status one last time to ensure it completed successfully after the human intervention.

**Test Script:**
```bash
#!/bin/bash
# Verify final completion

curl -s -X GET "http://localhost:8000/api/pipelines/execution/$EXECUTION_ID/status" \
  -H "Authorization: Bearer $MANAGER_TOKEN" | jq -r .status

# Expected Output:
# COMPLETED
```

---

## 4. HITL Audit and Compliance Verification

AgencyOS requires that all HITL interactions are securely logged in the audit trail. QA must verify that the approval event is recorded immutably.

**Test Script:**
```bash
#!/bin/bash
# Fetch Audit Logs for the specific execution

curl -s -X GET "http://localhost:8000/api/audit/logs?execution_id=$EXECUTION_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.logs[] | select(.event_type == "HITL_DECISION_RECORDED")'

# Expected Output should show the explicit decision (APPROVED), the timestamp, and the reviewer_id.
```

### End of Testing Guide
If any of these gates fail, ensure to log a bug against the `middleware_audit.py` or the `server/routers/pipelines.py` orchestrator layers.
