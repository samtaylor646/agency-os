# GitHub Repository Setup Guide

This guide ensures that the GitHub repository settings align with the strict `agency-os` rules, specifically enforcing the Human-in-the-Loop Mandate, Epic Workflow Hand-offs, and QA Quality Gates.

## 1. General Settings
Navigate to the **Settings** tab in your GitHub repository.

### Features
*   **Wikis:** `Disabled` (Unchecked). Documentation lives in the `docs/` folder to ensure it passes through the CI/CD pipeline and code review process (e.g., using MkDocs/Docusaurus).
*   **Issues:** `Enabled` (Check the box to track internal work).
*   **Pull requests:** `Enabled` (Ensure this is checked, but optionally restricted via Moderation Options if public).

### Pull Requests (Merging Workflow)
To maintain a clean Git history and enforce the monorepo standard:
*   **Allow merge commits:** `Disabled` (Unchecked)
*   **Allow squash merging:** `Enabled` (Checked) - This is the mandatory merging strategy.
*   **Allow rebase merging:** `Disabled` (Unchecked)
*   **Always suggest updating pull request branches:** `Enabled` (Checked)
*   **Automatically delete head branches:** `Enabled` (Checked)

---

## 2. Moderation Options (Public Repositories)
If the repository is public but you want to prevent unauthorized interaction:
1. Navigate to **Settings > Moderation options > Interaction limits**.
2. Enable the **Limit to repository collaborators** setting.
3. This restricts pull requests, issue creation, and comments to authorized team members only.

---

## 3. Branch Protection Rules / Rulesets (Protecting `main`)
To enforce **Rule 8 (No direct commits to main)** and **Rule 9 (Strict QA Gate)**, you must configure a Ruleset for the `main` branch.

1. Navigate to **Settings > Rules > Rulesets**.
2. Click **New branch ruleset**.
3. **Name:** e.g., "Protect Main Branch".
4. **Enforcement status:** Set to `Active`.
5. **Target branches:** Add target -> Include by pattern -> `main`.

### Required Rules
Check the following boxes:

*   **Require a pull request before merging**
    *   *Required approvals:* `1`
    *   *Dismiss stale pull request approvals when new commits are pushed:* Checked
    *   *Require conversation resolution before merging:* Checked
*   **Require status checks to pass**
    *   *Require branches to be up to date before merging:* Checked
    *   *Status checks:* Click `+` and search for the names of your CI jobs (e.g., `test`, `build`, or `AgencyOS CI/CD`). **This physically prevents merging if tests fail.**
*   **Bypass list**
    *   Ensure that you (and Administrators) do NOT bypass these rules. The rules must apply universally.

---

*This document was generated as part of the `agency-os` scaffolding configuration to ensure infrastructure consistency.*