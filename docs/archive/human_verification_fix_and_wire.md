# Human Verification Test Scripts: Fix & Wire Sprint

This document outlines the step-by-step manual test scripts required to verify the features developed during the "Fix & Wire" sprint. It covers both **Agency Admin** and **Client** user flows.

## Setup Instructions
1. Ensure the Agency OS application is running locally or in the staging environment.
2. You will need access to two accounts or open two separate incognito/browser profiles:
   * **Agency Admin Account**
   * **Client Account**
3. Ensure the database is seeded with initial testing data (if running locally, run `python seed_db.py`).

---

## Test Case 1: Inviting a New User to a Workspace

### Scenario 1.1: Agency Admin Invites a Client
* **Role:** Agency Admin
* **Prerequisites:** Logged in as Agency Admin, navigated to a specific Workspace.
* **Steps:**
  1. Navigate to **Workspace Settings** > **Members**.
  2. Click the **Invite User** button.
  3. Enter a valid email address for the new user.
  4. Select the role **Client Approver** from the dropdown.
  5. Click **Send Invitation**.
* **Expected Outcome:**
  * A success toast notification appears confirming the invitation was sent.
  * The newly invited user appears in the Members list with a "Pending" status.

### Scenario 1.2: Client Attempts to Invite a User (Negative Test)
* **Role:** Client
* **Prerequisites:** Logged in as Client, navigated to the same Workspace.
* **Steps:**
  1. Navigate to **Workspace Settings** > **Members**.
* **Expected Outcome:**
  * The **Invite User** button should be disabled or hidden entirely, as Clients do not have permission to invite new users.

---

## Test Case 2: Editing a User's Role

### Scenario 2.1: Agency Admin Changes User Role
* **Role:** Agency Admin
* **Prerequisites:** Logged in as Agency Admin. Workspace has at least one other active user.
* **Steps:**
  1. Navigate to **Workspace Settings** > **Members**.
  2. Locate an existing user in the list (e.g., currently an "Admin" or "Client").
  3. Click the **Edit Role** (or context menu -> Edit) button next to their name.
  4. Change the role to **Client Approver**.
  5. Click **Save** or **Update**.
* **Expected Outcome:**
  * A success notification appears.
  * The Members list immediately reflects the updated role ("Client Approver") for that user.
  * *Verification:* Log in as that user to verify their UI now restricts admin-only features.

---

## Test Case 3: Managing API Keys (Generating and Revoking)

### Scenario 3.1: Agency Admin Generates a New API Key
* **Role:** Agency Admin
* **Prerequisites:** Logged in as Agency Admin.
* **Steps:**
  1. Navigate to **Settings** > **API Keys** (or Credentials Manager).
  2. Click **Generate New Key**.
  3. Enter a descriptive name for the key (e.g., "Zapier Integration").
  4. Click **Create**.
* **Expected Outcome:**
  * The new API key is generated and displayed *once* (with a copy-to-clipboard button).
  * After closing the modal, the key appears in the active keys list (partially obscured).

### Scenario 3.2: Agency Admin Revokes an API Key
* **Role:** Agency Admin
* **Prerequisites:** Logged in as Agency Admin, with at least one active API Key present.
* **Steps:**
  1. Navigate to **Settings** > **API Keys**.
  2. Locate the previously created API key.
  3. Click the **Revoke** or **Delete** (trash can) icon next to the key.
  4. Confirm the revocation in the confirmation dialog.
* **Expected Outcome:**
  * The key is immediately removed from the active keys list.
  * (Technical verification) Subsequent API calls using that key return a 401 Unauthorized error.

---

## Test Case 4: Exporting Data (CSV/Downloads)

### Scenario 4.1: Exporting Audit Logs
* **Role:** Agency Admin
* **Prerequisites:** Logged in as Agency Admin, system has generated some audit events.
* **Steps:**
  1. Navigate to **Audit Logs**.
  2. Apply any desired filters (e.g., Date Range = Last 7 Days).
  3. Click the **Export to CSV** (or Download) button.
* **Expected Outcome:**
  * A CSV file is successfully downloaded to the local machine.
  * Opening the CSV reveals the correct, appropriately filtered audit log data including timestamps, users, actions, and IP addresses.

### Scenario 4.2: Exporting Analytics Data
* **Role:** Agency Admin / Client
* **Prerequisites:** Logged in, navigated to **Analytics Dashboard** containing populated graphs/tables.
* **Steps:**
  1. Navigate to **Analytics Dashboard**.
  2. Locate the primary data table or a specific chart.
  3. Click the **Export** button.
* **Expected Outcome:**
  * A file (CSV or PDF depending on implementation) is downloaded.
  * The downloaded file accurately reflects the data currently displayed on the dashboard.
