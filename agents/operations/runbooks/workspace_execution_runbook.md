# Workspace Execution Runbook

This runbook details the specific phases and tasks required for the Housekeeping Team to address findings from the recent workspace assessment.

## Phase 1: Backend Cleanup
**Assigned to:** Backend Architect

**Tasks:**
1. Fix dependency bloat in `server/requirements.txt`:
   - Remove duplicate or conflicting entries for `flask` and `fastapi`.
   - Remove `python-multipart` if duplicated or obsolete.
2. Remove obsolete deployment configurations:
   - Delete the obsolete `deployment/Dockerfile`.

## Phase 2: Script & Bloat Cleanup
**Assigned to:** Senior Developer

**Tasks:**
1. Delete the bloated `scripts/archive/` directory.
2. Delete `server/tests/archive/` directory if it exists.

## Phase 3: Documentation Routing & Compliance
**Assigned to:** Technical Writer

**Tasks:**
1. Relocate `docs/research/agencyos_competitor_analysis.md` to `docs/core/` (or `docs/archive/` if no longer relevant).
2. Delete the non-compliant `docs/research/` folder to adhere to documentation routing rules.
