# Standard Kickoff Protocol

## Overview
This runbook defines the strict, human-in-the-loop protocol for initiating any new Phase, Epic, or Sprint within AgencyOS. It enforces proper documentation, compliance checks, and explicitly links tasks to the correct specialized agents defined in `.clinerules` and `/agents`.

## 1. MANDATORY: The Master Plan Check
**CRITICAL RULE:** Before any kickoff begins, the `agents-orchestrator` MUST locate and read the active Master Plan document (e.g., `docs/core/phase_4_master_plan.md`). 

The `agents-orchestrator` must **never hallucinate or invent task assignments**. All roles, epics, and subtasks are already explicitly assigned within the Master Plan. The `agents-orchestrator`'s role is merely to coordinate the agents listed in that plan.

## 2. The Kickoff Team (Explicit `.roomodes` Slugs)
To fulfill the `.clinerules` mandate, the `agents-orchestrator` MUST use the `switch_mode` or `new_task` tool to assign the following steps to these explicit agent slugs. Generic roles are strictly forbidden.

* **`agents-orchestrator`**: The central coordinator. Reads the Master Plan, triggers the sequence, and enforces the protocol.
* **`product-manager`**: Drafts the PRD or scope document based on the Master Plan.
* **`engineering-backend-architect` / `design-ux-architect`**: Drafts technical specs and architectural plans.
* **`support-legal-compliance-checker`**: Audits the design for regulatory or data privacy compliance.
* **`testing-evidence-collector`**: Drafts the QA Test Plan and HITL verification steps.
* **`engineering-git-workflow-master`**: Checks out the isolated feature/epic branch.

## 3. Step-by-Step Kickoff Sequence

### Step 1: Initiation & Requirements (`product-manager`)
* `agents-orchestrator` reads the active Master Plan.
* `product-manager` writes the formal PRD/scope document for the specific Epic.

### Step 2: Ecosystem Review Assessment (`agents-orchestrator`)
* Evaluate if the Epic crosses a major Phase Gate, involves third-party integrations, or is a core architectural pivot.
* *Action:* Toggle the Ecosystem Review Board ON (via `./scripts/toggle_ecosystem_board.sh`) if required by the Master Plan.

### Step 3: Technical Design & Legal Review
* `engineering-backend-architect` (or UX counterpart) drafts the Technical Design document, explicitly verifying against existing architecture to prevent circular dependencies.
* `support-legal-compliance-checker` audits the design and drafts a compliance sign-off document.

### Step 4: QA & Acceptance Planning (`testing-evidence-collector`)
* `testing-evidence-collector` drafts the E2E Test Plan and Human-in-the-Loop (HITL) instructions.

### Step 5: Environment & Branch Prep (`engineering-git-workflow-master`)
* `engineering-git-workflow-master` checks out the dedicated git branch (e.g., `epic/X.Y-feature`). Ensures `main` is clean, up-to-date (`git pull origin main`), and free of uncommitted changes before branching.

### Step 6: Final Kickoff Summary & HITL Approval (`agents-orchestrator`)
* `agents-orchestrator` generates a final summary of all generated documents and git states.
* **CRITICAL:** The `agents-orchestrator` lists the exact agent slugs assigned to the *implementation* phase, **reading these directly and exclusively from the Master Plan.**
* Prompts the human user for explicit consent to begin the implementation phase.

## 4. End of Task Mandate (Closing Sequence)
Before any Epic or Phase can be considered complete, the following mandatory closing sequence MUST be executed in exact order:

1. **Docs/Memory Finalization:** 
   * Update `.roo/memory/changelog.md` and `.roo/memory/active_context.md`.
   * Ensure all new documentation is routed to the correct `docs/` subfolder.
2. **HITL Approval:**
   * A human must be explicitly prompted for User Acceptance Testing (UAT) and formal review/approval.
3. **Git Workflow Master Handoff:**
   * Hand off to the `engineering-git-workflow-master` to ensure a formal `git commit` encapsulates all changes on the epic's branch.
   * Push the commit to the remote repository (`git push`) to finalize synchronization and officially record the handoff.

## 5. Ecosystem Review Board & Rule Toggling Policy
If toggled ON during Step 2, the `agents-orchestrator` MUST halt forward progress and summon the cross-functional audit (Legal, Finance, Infrastructure, etc.) before writing code. This protects against architectural blind spots during major platform shifts. It should be toggled OFF for standard daily sprints.
