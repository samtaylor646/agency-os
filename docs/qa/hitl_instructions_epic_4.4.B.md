# Human-in-the-Loop (HITL) Review Instructions: Epic 4.4.B

## Overview
This document provides the exact, copy-paste commands and steps required for the human operator to manually verify Epic 4.4.B (Load Testing Concurrency Update) before merging it into the `main` branch.

## Step 1: Check out the Epic Branch
To begin your review, you must first switch your local workspace to the branch where the changes were made:
```bash
git checkout epic/4.4.B-load-testing
```

## Step 2: Review the Code Changes
Open the following file in your VSCode editor and visually inspect the changes:
- `scripts/load_test.py`
**What to look for:** The script should now utilize `asyncio` and `aiohttp` to send concurrent requests, rather than looping synchronously. 

## Step 3: Run the Verification Test (Optional)
If you wish to see the code execute:
1. Open a new terminal and start the server:
   ```bash
   python3 server/api_server.py
   ```
2. Open a second terminal and execute the load test:
   ```bash
   python3 scripts/load_test.py --pods 50
   ```
3. Verify the output displays "Starting load test with 50 concurrent pods..."

## Step 4: Approve and Merge
If the code looks correct and meets the requirements, execute the following commands to merge the work into the production `main` branch:
```bash
git checkout main
git merge epic/4.4.B-load-testing
git push origin main
```

If the code requires changes, do not merge. Instead, reply to the Orchestrator with your requested modifications.
