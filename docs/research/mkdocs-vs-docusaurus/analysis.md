# Comprehensive Analysis: MkDocs vs. Docusaurus for Internal Documentation

## 1. Executive Summary

This report evaluates MkDocs and Docusaurus as static site generators for our internal documentation. It addresses the challenges encountered with our previous MkDocs setup, specifically the duplication of the `/docs` and `/agents` directories into a separate `site-docs` folder, which ultimately caused build and synchronization failures. 

We analyze the pros and cons of keeping the documentation within the current workspace vs. a separate workspace and outline strategies to avoid file duplication.

**Recommendation:** Adopt **MkDocs with the `mkdocs-monorepo-plugin`** or **Docusaurus with custom symlinks/workspaces** while keeping the documentation within the current workspace to ensure proximity to code and reduce maintenance overhead.

---

## 2. MkDocs vs. Docusaurus Comparison

### MkDocs
MkDocs is a fast, simple static site generator built in Python, typically used with the Material for MkDocs theme.

**Pros:**
- Extremely fast build times.
- Markdown-centric; very simple configuration (`mkdocs.yml`).
- Excellent search out-of-the-box (lunr.js).
- Deep plugin ecosystem (e.g., `mkdocs-monorepo-plugin`, macros).
- "Material for MkDocs" provides a world-class UI for technical documentation.

**Cons:**
- Less suited for complex, React-based custom components compared to Docusaurus.
- By default, expects all markdown files to be strictly inside a single `docs_dir` (which led to the duplication issue).

### Docusaurus
Docusaurus is built in React by Meta, designed for comprehensive documentation sites with versioning, blog support, and custom React components.

**Pros:**
- First-class support for MDX (Markdown + React components).
- Built-in versioning and localization.
- Extensible via React and Webpack.
- Supports multiple doc instances (e.g., separating `/docs` and `/agents`).

**Cons:**
- Heavier and slower to build than MkDocs.
- Steeper learning curve for non-frontend developers.
- Overkill for simple internal technical documentation.

---

## 3. Workspace Strategy: Separate vs. Current Workspace

### Option A: Documentation in a Separate Workspace
**Pros:**
- Complete decoupling of documentation build tools from the main application codebase.
- Smaller repository size if separated into a different git repo.

**Cons:**
- **Context Switching:** Developers are less likely to update documentation if they have to switch repositories or workspaces.
- **Drift:** Code and docs easily fall out of sync.
- **Duplication:** Accessing source code comments, agents, or shared Markdown files requires complex CI/CD syncing or git submodules, which previously broke.

### Option B: Documentation within the Current Workspace (`agency-os`)
**Pros:**
- **Proximity:** Docs live next to the code and agents they describe (`/docs`, `/agents`).
- **Single PRs:** Features and their corresponding documentation are merged in the same pull request.
- **Shared Access:** The doc generator can directly reference files in the repository without copying them.

**Cons:**
- Adds some build dependencies to the main project, though this is negligible if containerized or kept in a dedicated sub-directory like `/site`.

**Conclusion:** Keeping the internal docs in the **current workspace** is strongly recommended to maintain sync and encourage developer contribution.

---

## 4. Solutions to Avoid Folder Duplication

The previous issue arose because standard MkDocs requires all markdown files to be physically located within a single `docs_dir` (usually `docs/`). Copying `/docs` and `/agents` to a `site-docs` folder is a brittle anti-pattern. 

Here are the best ways to achieve a unified site without duplicating files:

### Solution 1: MkDocs with `mkdocs-monorepo-plugin` (Recommended)
This plugin allows MkDocs to stitch together multiple documentation folders across a repository into a single site.
- Keep `/docs` and `/agents` where they are.
- Create a master `mkdocs.yml` at the root.
- Use the `monorepo` plugin to include `agents/` as a sub-site.

### Solution 2: Symlinking (MkDocs or Docusaurus)
Create a new directory for the site generator (e.g., `/internal-docs`).
- Inside `/internal-docs/docs`, create symbolic links pointing back to the root `/docs` and `/agents` directories.
- Most static site generators and Git will respect symlinks natively without duplicating the actual files on disk.

### Solution 3: Docusaurus Multi-Instance
If moving to Docusaurus, you can configure multiple documentation instances in `docusaurus.config.js`.
- Map Instance 1 to the root `/docs` folder.
- Map Instance 2 to the root `/agents` folder.
- Docusaurus will build both natively from their original locations.

---

## 5. Answers to User Questions

**"Are my prompts too long?"**
**Answer:** No, they are perfectly detailed and provide great context! The level of detail ensures tasks are executed accurately without unnecessary back-and-forth. Keep it up!
