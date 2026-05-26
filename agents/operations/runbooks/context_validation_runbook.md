# Context Validation Runbook

## Objective
To provide a structured process for the Context Review Board to validate rules, context files, and agent instructions for scalability, technical soundness, and QA compliance.

## Prerequisites
- Access to `.clinerules`, `config/settings.md`, and any proposed architectural changes.
- Availability of the Backend Architect, Senior Developer, Evidence Collector, and Product Manager.

## Phase 1: Preparation
1. **Gather Materials**: Compile the latest versions of `.clinerules` and `config/settings.md`.
2. **Identify Deltas**: Highlight any recent changes or newly proposed rules.

## Phase 2: Board Review Steps

### 1. Scalability Assessment (Backend Architect)
- Do the routing rules support the addition of new agents and directories without conflict?
- Are the documentation routing paths distinct and scalable as the project grows?
- Do Docker and container constraints align with infrastructure limits?

### 2. Technical Soundness Assessment (Senior Developer)
- Are the Epic workflow rules practical for daily developer operations?
- Do the branching and commit requirements align with standard `git` best practices?
- Is the "No Unsolicited Advice" protocol clearly actionable?

### 3. QA Compliance Assessment (Evidence Collector)
- Is the "STRICT QA GATE" properly defined and enforceable?
- Are there clear definitions of what constitutes "automated tests and formal sign-off"?
- Can the required QA artifacts be effectively tracked in `docs/qa/`?

### 4. Workflow Alignment Assessment (Product Manager)
- Do the rules support smooth epic transitions and sprint management?
- Are memory maintenance protocols (.roo/memory) sufficient to prevent context loss during handoffs?

## Phase 3: Resolution & Sign-Off
1. **Compile Findings**: Document any discrepancies, missing safeguards, or overly restrictive rules.
2. **Draft Adjustments**: Propose specific edits to `.clinerules` or `config/settings.md`.
3. **Sign-Off**: Require unanimous approval from the board.
4. **Publish**: Output the final review to `docs/operations/context_board_review.md`.
