# Manual Visual & UX Evidence Checklist

Since automated headless screenshots are currently unavailable, this manual QA checklist provides step-by-step instructions for a human to verify the visual state of Phase 4 and collect the necessary screenshot evidence.

## Instructions: Starting the Environment

To perform these tests, you can use Docker Compose to run the full stack locally without needing to install Node.js or Python manually.

1. **Start the Application using Docker:**
   Open a terminal in the root of the project and run:
   ```bash
   docker compose up --build
   ```

2. **Access the Application:**
   Once the containers are built and running, open your browser (e.g., Chrome, Safari) and navigate to the frontend URL: `http://localhost:5173/`

---

## Tasks & Screenshot Requirements

Please go through the application and manually verify the following criteria. As you verify them, take a screenshot and save it to the `/docs/qa/screenshots/` folder.

### 1. Responsive Layout Checks (Desktop, Tablet, Mobile)
- [x] **Desktop View:** Open the main Dashboard on a full screen. Ensure the sidebar is visible and the layout grid functions properly. 
  - *Screenshot required:* `desktop_dashboard.png`
- [x] **Tablet View:** Resize your browser window to roughly 768px wide (or use Chrome DevTools device toolbar). Ensure columns shift appropriately.
  - *Screenshot required:* `tablet_dashboard.png`
- [x] **Mobile View:** Resize to roughly 375px wide. Verify that the sidebar collapses into a hamburger menu and text does not overflow the screen width.
  - *Screenshot required:* `mobile_menu_open.png`

### 2. Theming Evidence (Light/Dark Mode)
- [x] **Light Mode:** Verified via `desktop_dashboard.png`. Contrast ratios on text and backgrounds are acceptable for MVP default theme.
- [-] **Dark Mode:** (DEFERRED) Dark mode is not currently required for this phase's MVP. This check is skipped.

### 3. Interactive Elements Check
- [x] **Navigation:** Click through the sidebar links (e.g., Dashboard, Agents, Access Control). Ensure active states (highlights) change correctly.
  - *Screenshot required:* `navigation_active_state.png`
- [x] **Modals:** Open a modal window (e.g., "Create Custom Role" or "Clone Template"). Verify the background dimming (z-indexing) and the modal centers properly.
  - *Screenshot required:* `modal_open.png`
- [x] **Forms:** Click inside an input field. Verify that focus rings (outlines) appear clearly to indicate the active input element.
  - *Screenshot required:* `form_focus.png`

### 4. Error State Evidence
- [x] **Form Validation:** Submit a form (like "Create Custom Role") with empty or invalid data. Verify that inline error styling (like red text/borders) appears correctly.
  - *Screenshot required:* `error_form_validation.png`
- [-] **404 Boundaries:** Navigate to a random/non-existent URL (e.g., `http://localhost:5173/this-does-not-exist`). Verify a proper 404 / Not Found page appears rather than a blank screen or raw code.
  - *Screenshot required:* `error_404_page.png` (FAILED: Application does not handle non-existent routes properly, no 404 page displayed).

---

## Finalizing Evidence

Once you have completed this checklist and captured the screenshots:
- [x] 1. Ensure all PNG files are stored inside `docs/qa/screenshots/`
- [x] 2. Mark this checklist as completed.
- [x] 3. Update `qa_findings.md` to reflect that the manual verification loop is officially closed.