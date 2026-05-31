# MkDocs Local Development Guide

## Overview
AgencyOS utilizes a "Pristine Source" Native Pipeline for building our internal MkDocs documentation. 

This means MkDocs automatically pulls content dynamically from the `/docs` and `/agents` directories without polluting those directories with build scaffolding, CSS, or `.pages` configurations.

## Architecture: The `.mkdocs_src` Virtual Build
To maintain strict governance over our `/docs` folder, all MkDocs configurations reside in a hidden directory at the root of the project called `.mkdocs_src/`.

*   **Symlinks:** Inside `.mkdocs_src/`, there are native OS symlinks pointing to `../docs` and `../agents`. These act as 0-byte portals. They are NOT duplicates.
*   **Scaffolding:** The custom `stylesheets/`, theme `overrides/`, and `.pages` configs live exclusively inside `.mkdocs_src/`.
*   **Git:** `.mkdocs_src/` is intentionally added to `.gitignore`. **Do not attempt to commit this directory.**

## How to Run the Documentation Locally

### 1. Install Dependencies
Ensure you have the required MkDocs packages installed in your local Python environment:
```bash
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin
```

### 2. Start the Local Server
From the root directory of the `agency-os` repository, run:
```bash
python3 -m mkdocs serve
```

*MkDocs will automatically trace the symlinks in `.mkdocs_src/` and build the dynamic navigation tree using the `awesome-pages` plugin.*

### 3. View the Site
Open your browser and navigate to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 4. Updating Documentation
You do not need to touch `mkdocs.yml` or run copy scripts when adding new files. 
Simply create your new markdown files natively within `/docs/` or `/agents/`, and the MkDocs live-reload server will automatically detect them and update the sidebar hierarchy!
