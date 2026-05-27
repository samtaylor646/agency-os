# HITL Instructions: Epic 4.4.C - E2E Pod Testing

## 1. Objective
A human-in-the-loop (HITL) review is required to verify the new automated E2E Pod lifecycle test suite. This verification ensures that the test suite runs successfully, isolates itself from the main application, and adequately covers multi-agent scenarios.

## 2. Prerequisites
- Docker should be running (for local ephemeral postgres/redis if used, or to spin up the AgencyOS stack).
- Python environment properly configured.

## 3. Verification Steps

### Step 1: Execute the Test Suite
Run the full `pytest` suite for E2E Pod Lifecycle tests.
```bash
# Ensure you are in the workspace root
cd /Users/samtaylor/Dev/projects/Agency/agency-os

# Run the test suite specifically targeting E2E Pod lifecycle tests
pytest server/tests/test_e2e_pod_lifecycle.py -v
```

**Expected Result:** All tests (Pod Initialization, Messaging, Semantic Memory, Kill Switch) should pass with `PASSED` status.

### Step 2: Validate Environment Isolation
Verify that running the tests did not leak data into the default local database or Redis instance.
```bash
# Check standard APP_ENV setting logic in conftest
cat server/tests/conftest.py | grep APP_ENV
```

**Expected Result:** You should see safeguards asserting that `APP_ENV != "production"`. 

### Step 3: Review Test Fixture Isolation
Review the test suite structure manually to ensure mocking and DB rolling back are in place.
```bash
cat server/tests/test_e2e_pod_lifecycle.py
```

**Expected Result:** Look for database transaction rollbacks, or isolated namespace usages in Redis, and `unittest.mock` usage for LLMs.

## 4. Sign-Off
Once the test output is verified to be 100% passing and the test isolation mechanism is visually confirmed, the Evidence Collector can formally sign off on this Epic and allow the feature branch to be merged into `main`.
