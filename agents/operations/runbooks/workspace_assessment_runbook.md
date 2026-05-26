# Workspace Assessment Runbook

**Purpose:** A non-destructive assessment plan to evaluate workspace health, identify bloat, and propose safe, structural improvements.

## Execution Plan

### Phase 1: Dependency & Root File Audit
*   **Objective:** Identify critical vs. clutter files at the root directory level and audit project dependencies.
*   **Actions:**
    *   Inventory all root-level files and categorize them (critical, active, clutter).
    *   Review dependency files for unused, redundant, or outdated packages.
    *   Document findings without deleting any files.

### Phase 2: Build & Infrastructure Health Check
*   **Objective:** Ensure Docker environments and network configurations are stable.
*   **Actions:**
    *   Inspect `Dockerfile` and `docker-compose.yml` setups.
    *   Verify container runtime stability and build success rates.
    *   Check active terminals for zombie processes or port conflicts (e.g., lingering services on port 8001).

### Phase 3: Documentation Consolidation Review
*   **Objective:** Identify remaining `/docs` cleanup needs and `/scripts/archive/` bloat.
*   **Actions:**
    *   Audit the `/docs/` directory structure against the strict documentation routing rules.
    *   Identify miscategorized, duplicate, or deprecated documentation.
    *   Evaluate the `/scripts/archive/` folder to assess if contents should be permanently removed or kept for historical reference.

### Phase 4: Rules Recommendation Report
*   **Objective:** Propose safe `.clinerules` or `validation_layer.py` updates based on the audit.
*   **Actions:**
    *   Compile the findings from Phases 1, 2, and 3 into a comprehensive summary.
    *   Draft actionable recommendations for ongoing workspace hygiene.
    *   Propose concrete rule additions or modifications for `.clinerules` and `validation_layer.py` to prevent future clutter.