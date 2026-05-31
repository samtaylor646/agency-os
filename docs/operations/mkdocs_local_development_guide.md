# MkDocs Local Development Guide

## Overview
AgencyOS utilizes a consolidated **`site-docs/` Architecture** for building our internal MkDocs documentation. 

This means MkDocs automatically pulls content from the `site-docs/` directory, which acts as the unified `docs_dir`. We moved away from hidden virtual build sandboxes and symlinks to prevent cross-platform build errors, while still keeping our documentation cleanly organized and styled.

## Architecture: The `site-docs/` Root
To maintain strict governance, all MkDocs configurations and source files reside under the `site-docs/` directory:

### 1. `site-docs/` (The Primary Site)
*   **Unified Source:** The `site-docs/` folder contains all active documentation (`docs/`), agent profiles (`agents/`), and the main landing page (`index.md`).
*   **Scaffolding & Theming:** The custom `stylesheets/`, Atlassian-style theme `overrides/`, and configurations live exclusively inside this folder so they do not pollute other areas of the repository.
*   **mkdocs.yml:** The primary configuration file located at the project root points its `docs_dir` directly to `site-docs`.

### 2. Historical Archive Site
*   **Archive Isolation:** We maintain a separate `mkdocs_archive.yml` configuration.
*   This ensures deprecated files never pollute the primary search bar or main navigation.

---

## How to Run the Documentation Locally

### 1. Install Dependencies
Ensure you have the required MkDocs packages installed in your local Python environment:
```bash
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin
```

### 2. Start the Local Servers
Because we use an archive separation architecture, you can run both sites simultaneously on different ports if needed.

**Start the Primary Site (Port 8000):**
Open a terminal and run:
```bash
python3 -m mkdocs serve
```

**Start the Archive Site (Port 8001):**
Open a *second* terminal window and run:
```bash
python3 -m mkdocs serve -f mkdocs_archive.yml -a 127.0.0.1:8001
```

### 3. View the Sites
*   **Primary Site:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
*   **Archive Site:** [http://127.0.0.1:8001/](http://127.0.0.1:8001/) (Or simply click the *🗄️ Historical Archive* link at the bottom of the primary site's sidebar).

### 4. Updating Documentation
You do not need to touch `mkdocs.yml` when adding new standard Markdown files. 
Simply create your new markdown files natively within `site-docs/docs/` or `site-docs/agents/`, and the MkDocs live-reload server will automatically detect them and update the sidebar hierarchy! **Crucial:** Never overwrite the `overrides/` folder or change `theme.custom_dir` in `mkdocs.yml`, as this will break our custom Atlassian theme styling.
