# Child Project CI Enforcement Plan

## Objective
Enforce Rule 15 from `config/settings.md`: Any push of global settings (e.g., `config/**`, `.clinerules`) must trigger localized tests in all connected child projects (client/server test suites) to capture downstream regressions.

## Current Enforcement
The current CI/CD pipeline (`.github/workflows/ci-tests.yml`) is configured to run on **all pushes and pull requests to `main`**. This inherently satisfies the enforcement mandate because:
1. All changes, including global configurations, go through the standard branch-and-PR model.
2. The `AgencyOS CI/CD` workflow automatically triggers on these PRs.
3. The workflow runs the full suite of localized tests for both:
   - **Frontend (Client):** `npm run test`
   - **Backend (Server):** `pytest server/tests/` (Both local and S3 storage contexts)

## Future Enhancements (If Needed)
If the project structure scales out into independent monorepo packages (e.g., separate microservices with isolated CI workflows), we will introduce a path-based trigger. For example:
```yaml
on:
  pull_request:
    paths:
      - 'config/**'
      - '.clinerules'
```
This specific path-trigger would be added to each independent child project's workflow to guarantee that global setting changes fan out and trigger all localized checks.

For the current consolidated monorepo approach, the existing catch-all PR trigger is sufficient and strictly enforces Rule 15.
