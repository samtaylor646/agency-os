# Strategic Roadmap: Fixing Kinetik-OS Faults

## 1. Objective

Provide a strategic, non-code roadmap to resolve the structural and procedural deficiencies in the Kinetik-OS build environment by applying the strict operational mandates of AgencyOS. The goal is to enforce AI alignment, optimize project execution, and eliminate architectural drift without directly modifying existing core code.

## 2. Step 1: Implement the Specialized Agent Hierarchy

*   **Action:** Scaffold the `/agents` directory structure within the Kinetik-OS environment.
*   **Execution:** Create specific agent profile markdown files (e.g., `architect.md`, `qa_engineer.md`) that explicitly define boundaries, skills, and restrictions.
*   **Rule Enforcement:** Implement the **Routing First Mandate**. All tasks must be assessed and delegated to the appropriate domain expert rather than handled by a generic AI instance.

## 3. Step 2: Establish the Documentation Source of Truth

*   **Action:** Restructure the Kinetik-OS documentation to follow the strict AgencyOS `/docs/` hierarchy.
*   **Execution:** Create the following directories:
    *   `docs/core/`: For "North Star" product requirements.
    *   `docs/technical/`: For architecture and API specifications.
    *   `docs/operations/`: For runbooks and guides.
    *   `docs/qa/`: For testing evidence.
    *   `docs/research/`: For research documents, competitive analysis, and exploratory technical documentation.
    *   `docs/archive/`: For deprecated and legacy files.
*   **Rule Enforcement:** Enforce the rule that all agents must validate their approach against `docs/core/` before initiating work.

## 4. Step 3: Implement Orchestrator and Checklist Protocols

*   **Action:** Introduce a central task management mechanism driven by an orchestrator.
*   **Execution:** Deploy a `.rootasks` markdown checklist. Break down large Kinetik-OS tasks into single, atomic steps.
*   **Rule Enforcement:** The Orchestrator agent will manage this checklist. No task can be marked complete, and no subsequent task can be started, without the Orchestrator verifying the completion of the current step.

## 5. Step 4: Enforce QA and Human-in-the-Loop Gates

*   **Action:** Apply rigid quality assurance and human verification phase gates.
*   **Execution:** Require explicit sign-off from the QA agent (`Evidence Collector`) and a human operator before code is merged or a major project phase is considered complete.
*   **Rule Enforcement:** Activate the **Human-in-the-Loop Mandate**. Agents must halt and request human validation during technical design phases, UI/UX checkpoints, and final UAT.

## 6. Step 5: Execute Public Repository Security Transition

*   **Action:** Secure the repository prior to public transition to prevent credential exposure and supply-chain vulnerabilities.
*   **Execution:**
    *   **Secrets Audit:** Scrub git history using tools like `git-filter-repo` and immediately revoke any previously committed secrets. Verify strict `.gitignore` rules.
    *   **Branch Protection:** Enforce rules on the main branch requiring PR reviews, passing status checks, and GPG signed commits.
    *   **Security Policies:** Add `SECURITY.md` for responsible disclosure and enable Private Vulnerability Reporting.
    *   **Automated Scanning:** Enable GitHub Dependabot, CodeQL, and Secret Scanning.
    *   **Repository Settings:** Apply a formal open-source `LICENSE` and restrict third-party GitHub Actions to prevent malicious workflows.
*   **Rule Enforcement:** These security gates **must** be implemented and verified before the repository visibility is flipped from private to public.
