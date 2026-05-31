# Strategy: Internal Build Docs vs. External App Docs

## 1. Context & Team Thoughts

The team recently investigated replacing or improving our MkDocs documentation system. User feedback highlighted a few key constraints and requirements:
1. **The Navigation Struggle:** In the past (specifically around branches `epic/mkdocs-atlassian-rebuild` and `epic/mkdocs-symlink-evaluation`, commit `2f24383`), significant effort was required to auto-generate the left sidebar for MkDocs using custom scripts like `scripts/generate_nav.py` or the `awesome-pages` plugin. This proved brittle and difficult to maintain.
2. **Preserving Internal Docs:** The internal documentation detailing the build process, architecture, and agent schemas (currently residing in `/docs` and `/agents`) is critical and must remain structurally intact to avoid disrupting developer workflows and history.
3. **Future External Docs:** As AgencyOS nears completion, we need a robust solution for *external, user-facing documentation* (e.g., user guides, API usage for customers, integration tutorials).

**Team Consensus:** 
The team agrees that mixing internal architecture/build docs with external user-facing docs in the same exact framework instance is an anti-pattern. Internal docs need to live close to the code (in `/docs` and `/agents`) and prioritize speed and simplicity for developers. External docs need a polished UI, versioning, search, and marketing integration, prioritizing the end-user experience.

---

## 2. Architectural Strategy

We propose a **Bifurcated Documentation Strategy**: keeping internal build docs lightweight and native, while spinning up a dedicated, feature-rich instance for external app documentation.

### A. Internal Docs (Build Process, Agents, Technical Architecture)
**Goal:** Zero-friction maintenance for developers; preserve existing `/docs` and `/agents` folder structures; avoid complex navigation generation scripts.

*   **Tooling:** **MkDocs** (Material theme) combined with the **`mkdocs-monorepo-plugin`** or native symlinks (as evaluated in `epic/mkdocs-symlink-evaluation`).
*   **Structure:** Leave `/docs` and `/agents` exactly where they are in the root directory.
*   **Navigation:** Instead of relying on brittle Python scripts (`generate_nav.py`) to auto-crawl and build nav trees, we will define explicit navigation in a root `mkdocs.yml` or use the `awesome-pages` plugin *only* if configured securely without copying directories. The `monorepo` plugin natively handles including outside folders without duplicating files.
*   **Audience:** Developers, Internal Orchestrators, Mode Agents.

### B. External Docs (User Guides for AgencyOS)
**Goal:** Polished, versioned, easily searchable user guides hosted on a separate domain (e.g., `docs.agencyos.dev`).

*   **Tooling:** **Docusaurus** or a completely distinct **MkDocs** instance housed in a separate directory (e.g., `/client/docs` or a separate repository).
*   **Structure:** Create a clean, isolated environment strictly for user-facing content (e.g., "Getting Started", "How to Deploy Agents", "Billing"). 
*   **Navigation:** Managed entirely within the selected framework's standard configuration (e.g., Docusaurus `sidebars.js`). Since this content is written for users, it will be manually structured and highly curated, negating the need for auto-generation scripts.
*   **Audience:** End-users, Customers, Third-party integrators.

---

## 3. Recommended Next Steps

1.  **Deprecate Custom Auto-Nav Scripts:** Officially retire `scripts/generate_nav.py` and other hacky workarounds from the `mkdocs-atlassian-rebuild` branch. Rely on standard MkDocs plugin configurations (like `mkdocs-monorepo-plugin`) to stitch `/docs` and `/agents` together.
2.  **Solidify Internal Config:** Update `mkdocs.yml` to point natively to the current workspace structure.
3.  **Bootstrap External Docs:** Initialize a Docusaurus or MkDocs site in a new `/user-docs` (or separate repo) when we are ready to write the customer-facing guides.

*This strategy satisfies the requirement to preserve internal build history while scaling gracefully to accommodate future customers.*