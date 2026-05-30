# Documentation Safeguard Plan

## 1. Executive Summary
A recent incident involving an automated script (`archive_docs.py` / `archive_docs.sh`) resulted in the accidental archiving and removal of active QA tracking files, breaking the synchronization between our documentation and the active codebase. 

This document outlines a comprehensive mitigation plan to implement technical and procedural safeguards, ensuring that active project documentation remains protected from unintended modifications or deletions by automated processes.

## 2. Technical Safeguards

### 2.1 Pre-Commit Hooks
To catch unintended documentation modifications early in the development lifecycle, we will implement local pre-commit hooks using the `pre-commit` framework.

**Implementation Details:**
*   **Protected Paths:** Define a strict list of directories that are "append/edit only" and block `git rm` or `git mv` actions unless explicitly bypassed with a confirmed override flag. 
    *   `docs/qa/QA_INDEX.md`
    *   `docs/qa/*_suite.md`
    *   `docs/qa/master_*.md`
    *   `docs/operations/Project_Tracking_and_Dependencies.md`
*   **Hook Script (`.githooks/pre-commit-doc-check`):** A bash script that intercepts file deletions in the `docs/` folder (excluding `docs/archive/`) and prompts the developer for explicit confirmation, or fails the commit outright if executed by an automated process.

### 2.2 CI/CD Validation Checks
We will add a GitHub Actions workflow to run validation on all Pull Requests to ensure active docs aren't silently archived.

**Implementation Details:**
*   **Action:** `Doc-Integrity-Check`
*   **Trigger:** On `pull_request` against `main` or release branches.
*   **Logic:** 
    1. Run `git diff --name-status origin/main` to identify deleted or moved files.
    2. Check if any affected file matches our protected documentation patterns (`docs/qa/*`, `docs/technical/*`, `docs/operations/*`).
    3. If an active document is moved to `docs/archive/` or deleted, the CI check automatically fails unless the PR contains a specific label (e.g., `doc-archival-approved`) applied by an administrator.

### 2.3 Strict Script Exclusion Logic
All utility scripts (Python, Bash, Node) that perform file manipulations must adhere to a strict whitelist/blacklist architecture.

**Implementation Details:**
*   **Centralized File System Utilities:** Scripts must use a central module (e.g., `scripts/validation_layer.py`) for file manipulation instead of raw `shutil.move` or `mv` commands.
*   **Exclusion Patterns:** The central utility must strictly ignore tracking files. Example logic:
    ```python
    PROTECTED_FILES = [
        "QA_INDEX.md",
        "Project_Tracking_and_Dependencies.md",
        "manual-test-plan.md"
    ]
    if any(protected in filepath for protected in PROTECTED_FILES):
        raise ProtectedFileError(f"Cannot archive active tracking file: {filepath}")
    ```

## 3. Governance and Procedural Policies

### 3.1 Script Review Policy
Any new script or modification to an existing script located in `scripts/`, `sandbox_tmp/`, or root that executes file system commands (`rm`, `mv`, `cp`, or python equivalents) must require a secondary review from a DevOps/Infrastructure engineer.

### 3.2 Human-in-the-Loop Archival
Fully automated archiving is strictly forbidden. 
*   Archiving tasks must be treated as dedicated sprint tasks.
*   Scripts meant to clean up directories must run in a "Dry Run" mode by default, outputting a list of files to be moved.
*   A human must explicitly pipe the output into the execution command or pass a `--force-execute` flag after reviewing the output.

## 4. Implementation Roadmap
1.  **Immediate (Next 24h):** Add `.githooks` restrictions for `docs/qa` and `docs/operations`.
2.  **Short Term (Sprint):** Implement the `Doc-Integrity-Check` GitHub Action.
3.  **Long Term:** Refactor all existing utility scripts to run through `scripts/validation_layer.py` to enforce the exclusion logic globally.
