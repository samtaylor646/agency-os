# Human-in-the-Loop (HITL) Review Instructions: Epic 4.4.C

## Overview
This document provides instructions to manually verify Epic 4.4.C (Comprehensive E2E testing of the Pod lifecycle).

## Step 1: Check out the Epic Branch
```bash
git checkout epic/4.4.C-e2e-testing
```

## Step 2: Review E2E Test Scripts
Open `server/tests/test_e2e_pod_lifecycle.py` and verify it contains tests for hitting the `/execute` DAG Orchestrator endpoint.

## Step 3: Run the tests (Optional)
```bash
python3 -m pytest server/tests/test_e2e_pod_lifecycle.py
```

## Step 4: Approve and Merge
```bash
git checkout main
git merge epic/4.4.C-e2e-testing
git push origin main
```
