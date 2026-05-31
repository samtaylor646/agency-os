# PRD: MkDocs Dual Routing Architecture & UX

## 1. Executive Summary
Following the successful deployment of the `.mkdocs_src` virtual sandbox, we must refine the user experience and architectural purity of the documentation. Currently, the `archive` folder is automatically pulled into the main search index, polluting results. Additionally, the navigation lacks a cohesive "Welcome Hub" and legacy breadcrumbs.

This Epic scopes the creation of a "Dual Routing Architecture." We will use virtual sandboxes to surgically isolate the `archive` folder into a standalone MkDocs instance, while injecting a high-value Welcome Hub and restoring the legacy breadcrumb trail to the primary site.

## 2. Core Requirements
1. **Search Isolation (Plan A):** The `archive` folder must be completely excised from the primary `mkdocs.yml` build to ensure clean search results. A secondary build (`mkdocs_archive.yml`) running via a new `.mkdocs_archive_src` sandbox will serve the historical files.
2. **The Welcome Hub:** The primary site must feature an informative "Welcome to AgencyOS Internal Docs" landing page. This page will reside exclusively within `.mkdocs_src/index.md` to strictly honor the rule against adding scaffolding or index files to the actual `/docs` root.
3. **Legacy Breadcrumbs:** Both sites must restore the `features: - navigation.path` MkDocs Material setting to display a breadcrumb trail with a Home icon and a disabled active-page link.
4. **Seamless Navigation:** The primary site must feature an external link (`🗄️ Historical Archive`) at the bottom of the navigation menu that redirects users to the isolated Archive site.

## 3. Scope & Dependencies
- **In Scope:** Creating `.mkdocs_archive_src`, updating `.mkdocs_src` symlinks to specifically exclude `archive`, rewriting `.mkdocs_src/index.md` into the Welcome Hub, configuring `mkdocs_archive.yml`, and updating the `.pages` navigation.
- **Out of Scope:** Restructuring or cleaning up the actual markdown content inside the `archive` folder.

## 4. Success Criteria
- Running `mkdocs serve` on the primary site yields 0 search results for known archival documents.
- The Welcome Hub provides a clear overview without violating `/docs` folder purity.
- The Breadcrumb trail is visible on all pages.
- Clicking the Archive link in the sidebar successfully navigates the user to the secondary site.
