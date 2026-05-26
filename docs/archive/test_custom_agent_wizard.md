# QA Test Plan: Custom Agent Creator Wizard

## Overview
This test plan provides step-by-step instructions to validate the functionality of the **Custom Agent Creator Wizard** within AgencyOS.

## Prerequisites
- AgencyOS must be running locally (frontend on port 5173, backend on port 8001).
- No external API key (like OpenAI) is required just to *create* the agent template. The wizard solely generates a configuration file.
- You do not need to log in through a traditional auth flow if you are using the local development environment, but you **must select an Active Workspace** in the UI sidebar/header. The wizard relies on `WorkspaceContext`.

## Test Execution Steps

### 1. Environment Setup
1. Verify the frontend and backend servers are running.
2. Navigate to `http://localhost:5173` in your browser.
3. Ensure a Workspace is selected from the Workspace dropdown/context switcher. (If not, create one).

### 2. Accessing the Wizard
1. Open the **Agency Panel** or navigate to the Custom Agent Creator section in the sidebar.
2. The UI should display the "Custom Agent Wizard" header.
3. *Expected Result:* Step 1 of 8 (Meta Configuration) should be visible.

### 3. Using the Auto-Fill Architect (Happy Path)
1. Click the **"Auto-Fill Architect"** button at the top right of the wizard.
2. *Expected Result:* All form fields across the 8 steps should be populated with default test data (Backend Architect).

### 4. Navigating Steps
1. Click **"Next"** to advance through Steps 1 to 8.
2. Verify the Step Indicator updates properly (blue for active, green checkmark for completed).
3. On Step 8, review the generated Markdown preview.
4. *Expected Result:* The markdown should correctly reflect the data in the form fields.

### 5. Submission and Creation
1. On Step 8, click the green **"Create Agent"** button.
2. *Expected Result:* A success message "Custom agent created successfully!" should appear.
3. The wizard form should reset to Step 1.
4. The new agent (e.g., "Backend Architect") should appear in the "Custom Agents Library" list at the bottom of the page.

### 6. Backend Verification (Evidence Collection)
1. In your VSCode terminal, check the `agents/` directory (specifically `agents/specialized/` or the domain selected).
2. *Expected Result:* A new `.md` file matching the agent name should exist, containing the exact markdown reviewed in Step 8.
