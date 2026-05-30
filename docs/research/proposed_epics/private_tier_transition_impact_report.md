# AgencyOS: Free Private Tier Transition Impact Report

This report outlines the operational, technical, and legal implications of moving the AgencyOS repository from a public status to a GitHub Free Private tier. The analysis focuses on Quality Assurance, Infrastructure (CI/CD), and Legal/Compliance considerations.

## 1. QA & Evidence Collection (The PR Review Challenge)

**The Issue:** 
On the GitHub Free tier, private repositories **do not have access to Branch Protection Rules**. This means we cannot natively enforce mandatory Pull Request approvals, status checks, or block direct commits to the `main` branch. This directly conflicts with our strict QA gates and Evidence Collector mandates.

**Mitigation & Manual Enforcement Strategy:**
1.  **Local Git Hooks:** We must implement strict client-side `.git/hooks/pre-push` scripts that automatically run `scripts/qa_runner.py` and `scripts/validation_layer.py`. The hook will abort the push if local tests fail.
2.  **Evidence Collector Sign-off Protocol:** We must encode a procedural rule in `config/settings.md` and `.clinerules` that forces the Evidence Collector agent to append a cryptographic-style hash or explicit signature to the PR description or commit message *before* a human manually hits the merge button.
3.  **Human-in-the-Loop Workflow:** Since GitHub won't block the merge, the orchestrator must enforce a local prompt requiring the user to type "Approve and Push" after reviewing the QA artifacts locally, strictly following our Human-in-the-Loop mandate.

## 2. Infrastructure & DevOps (The 2,000-Minute CI/CD Limit)

**The Issue:**
GitHub Free accounts are limited to **2,000 Actions minutes per month** for private repositories (public repositories have unlimited minutes). 

**Mitigation & Enforcement Strategy:**
1.  **Self-Hosted Runners:** We can bypass the 2,000-minute limit entirely by configuring local machines or our own existing cloud infrastructure as **Self-Hosted GitHub Runners**. Self-hosted minutes are unlimited and free on private repositories.
2.  **Optimize Trigger Conditions:** We must rewrite our workflow `.yml` files in `.github/workflows/` to trigger *only* on PR creation/updates targeting `main`, removing any `push: branches: ['*']` triggers that waste minutes on WIP commits.
3.  **Shift Left (Local Testing):** Rely heavily on local Docker environments (`docker-compose.yml`) and `pytest` for the bulk of the testing lifecycle, only relying on GitHub Actions for the final release gate.

## 3. Legal & Compliance (Open Source to Private Transition)

**The Issue:**
Taking an existing open-source project private alters the visibility but does not retroactively alter the rights previously granted to the public.

**Mitigation & Enforcement Strategy:**
1.  **Dependency Audit:** The Legal Compliance Checker agent should perform a full audit of `package.json` and `requirements.txt` to ensure no highly restrictive copyleft licenses (like AGPL) snuck in while it was public, which could legally complicate the private codebase.
2.  **Clean Break Tagging:** Create a definitive Git tag (e.g., `v-public-final`) right before switching to private. This establishes a clean legal boundary between the open-source legacy code and the new proprietary/private intellectual property.
