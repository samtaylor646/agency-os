# QA Test Plan: MkDocs Native Pipeline

## Objective
Verify that the native MkDocs pipeline utilizing `mkdocs-awesome-pages-plugin` builds without error, successfully resolves the `agents/` directory without duplication, and dynamically auto-generates the left navigation sidebar matching the legacy format.

## HITL Verification Steps
1. **Build Verification:** Run `mkdocs build` locally. Confirm the console shows no missing file warnings and completes successfully.
2. **Dynamic Sidebar Test:** 
   - Add a temporary file `docs/core/test_dynamic.md`.
   - Rebuild.
   - Visually confirm `test_dynamic` appears in the left sidebar automatically.
3. **Agent Integration Test:** Navigate to the `Agents` section in the UI. Confirm the `academic/`, `sales/`, and other subfolders properly loaded via the symlink without creating duplicated files in a `site-docs` folder.
4. **Visual Parity:** Verify that `Inter` font is applied, and the custom theme color palette is intact (loading from `docs/overrides` and `docs/stylesheets/custom.css`).

