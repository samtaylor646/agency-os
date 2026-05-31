# Epic: Safe Best Practices Updates

## 1. Overview
This plan defines the official methodology, roles, and automated safeguards required to safely propagate and update best practices across the AgencyOS workspace and any child projects. It ensures that changes to our ecosystem's core rules do not introduce regressions or violate compliance mandates.

## 2. Evaluation of Standard Kickoff Protocol
The existing `docs/operations/standard_kickoff_protocol.md` was evaluated during this planning phase. 

**Conclusion:** The Standard Kickoff Protocol is highly relevant and will be established as the **new, enforced standard** for all best-practice update rollouts. Its structured, human-in-the-loop steps (particularly the mandatory Master Plan Check and Ecosystem Review Assessment) perfectly align with the goal of safe ecosystem-wide updates. This new Epic will directly integrate with that runbook, specifically utilizing the Ecosystem Review Board when sweeping best-practice changes impact multiple specialized agent workflows.

## 3. Methodology for Best Practice Updates

### Phase 1: Identification & Drafting (`product-manager` & `engineering-technical-writer`)
* **Trigger:** A new best practice, tooling upgrade, or architectural pattern is identified.
* **Action:** The `product-manager` drafts the updated rules in a centralized configuration proposal (e.g., updates to `config/settings.md` or `.clinerules`).

### Phase 2: Mandatory Review (`agents-orchestrator`)
* **Trigger:** The orchestrator identifies the Epic crosses a major rule threshold.
* **Action:** The `agents-orchestrator` triggers the Ecosystem Review Board (`./scripts/toggle_ecosystem_board.sh`) to audit the proposed best practices for blast radius, security, and cost. 
* **Key Approvers:** `support-legal-compliance-checker`, `engineering-backend-architect`, and `support-infrastructure-maintainer`.

### Phase 3: Controlled Rollout (`engineering-git-workflow-master`)
* Updates are pushed onto isolated branches (e.g., `epic-safe-best-practices-updates`).
* **Propagation:** Scripts or CLI tools systematically apply changes down to child project configurations to maintain parity.

### Phase 4: Automated Testing & HITL Verification (`testing-evidence-collector`)
* Automated CI/CD pipelines run on the workspace and child projects to verify that new best practices don't break existing builds or tests.
* `testing-evidence-collector` provides the HITL (Human-in-the-loop) summary report for final manual sign-off before merging into `main`.

## 4. Roles & `.roomodes` Assignments
Following the Standard Kickoff Protocol, the following specialized agents are mandated for best-practice updates:
* **`agents-orchestrator`**: Central coordinator enforcing this plan.
* **`product-manager`**: Scopes the specific updates and handles documentation.
* **`engineering-git-workflow-master`**: Manages isolated branching strategies across child projects.
* **`testing-evidence-collector`**: Validates the safe application of updates via regression tests.

## 5. Automated Safeguards
To guarantee safety during workspace updates, the following technical safeguards must be enforced:
1. **No Direct `main` Commits:** All best practice updates must utilize the standard branch-and-PR model.
2. **Ecosystem Board Tripwire:** Any modification to `.clinerules` automatically mandates an Ecosystem Board Review before proceeding.
3. **Child Project CI Enforcement:** Any push of global settings will trigger localized tests in all connected child projects (e.g., client/server test suites) to capture downstream regressions instantly.
