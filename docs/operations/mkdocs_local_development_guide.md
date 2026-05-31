# MkDocs Local Development Guide

## Overview
AgencyOS utilizes a **Pristine Source Dual-Routing Architecture** for building our internal MkDocs documentation. 

This means MkDocs automatically pulls content dynamically from the active `/docs` and `/agents` directories without polluting those directories with build scaffolding, CSS, or `.pages` configurations. Furthermore, the `archive` folder is completely isolated into a standalone site to prevent search index pollution.

## Architecture: The Virtual Build Sandboxes
To maintain strict governance over our pristine folders, all MkDocs configurations reside in two hidden directories at the root of the project:

### 1. `.mkdocs_src/` (The Primary Site)
*   **Selective Symlinks:** Inside `.mkdocs_src/docs/`, there are native OS symlinks pointing *only* to the active subfolders (`core`, `operations`, `technical`, `qa`, `research`). The `archive` folder is intentionally excluded.
*   **The Welcome Hub:** The landing page `index.md` resides solely in `.mkdocs_src/` to prevent polluting the `/docs` root.
*   **Scaffolding:** The custom `stylesheets/`, theme `overrides/`, and `.pages` configs live exclusively inside this hidden folder.

### 2. `.mkdocs_archive_src/` (The Historical Archive Site)
*   **Archive Symlink:** This sandbox contains a single symlink routing to `../docs/archive`.
*   **Isolation:** Built via `mkdocs_archive.yml`, this ensures deprecated files never pollute the primary search bar.

*Note: Both sandboxes are added to `.gitignore`. **Do not attempt to commit these directories.** *

---

## How to Run the Documentation Locally

### 1. Install Dependencies
Ensure you have the required MkDocs packages installed in your local Python environment:
```bash
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin
```

### 2. Start the Local Servers
Because we use a dual-routing architecture, you must run both sites simultaneously on different ports.

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
You do not need to touch `mkdocs.yml` or run copy scripts when adding new files. 
Simply create your new markdown files natively within `/docs/` or `/agents/`, and the respective MkDocs live-reload server will automatically detect them and update the sidebar hierarchy!
