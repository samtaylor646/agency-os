# Global Design System Plan

## 1. Overview
The global design system for the AgencyOS application is being overhauled to a unified, Atlassian-inspired aesthetic. This comprehensive redesign will elevate the user experience, ensuring a premium, cohesive, and intuitive interface across all touchpoints.

> **Parallel Execution Note:** This document is part of a three-pronged, coordinated parallel design effort. Decisions made here represent the core styling track and must flow seamlessly into the parallel structural tracks: the [Intro Page Redesign Plan](intro_page_redesign_plan.md) and the [Chat Scope Interface Redesign Plan](chat_scope_interface_redesign.md).

## 2. Global Design System: Atlassian-Inspired UI
All UI across the app will be updated to utilize a unified, Atlassian-inspired design system. This ensures consistency, professionalism, and ease of use characteristic of enterprise tools like Jira.

### Visual Design Principles
*   **Design Token Hierarchy:** To support Future expansions like Dark Mode, the design system will strictly separate Primitive Tokens (e.g., `blue-500`) from Semantic Tokens (e.g., `color-primary-action`).
*   **Typography:** Clean, highly legible sans-serif font stack (e.g., Inter, Roboto, or system fonts). Clear hierarchy with strong, contrasting headings and muted secondary text for dense information displays.
*   **Color Palette:**
    *   *Primary:* A dependable, enterprise blue (`#0052CC` or similar) for primary actions and highlights.
    *   *Backgrounds:* Subtle cool grays (`#F4F5F7`) for sidebars and secondary panels; crisp white (`#FFFFFF`) for main content areas and cards.
    *   *Borders:* Soft, 1px dividers (`#DFE1E6`) to separate structural elements without adding visual weight.
*   **Components:** Slightly rounded corners (border-radius: 4px to 8px), flat design with subtle, consistent shadows only on interactive, floating, or elevated elements (modals, dropdowns, tooltips, cards).
*   **Animations & State:** Snappy but smooth transitions (200-300ms ease-in-out) for menus, collapsible panels, and state changes. To support fluid search-bar transitions across routes, a singleton **"Global Prompt Context"** component must be established at the application root.

## 3. Accessibility & WCAG Compliance
A premium user experience must be inclusive. The redesigned application will adhere strictly to WCAG 2.1 AA standards, ensuring accessibility for all users.

### Core Accessibility Requirements
*   **WCAG 2.1 AA Standards:** All new components and layouts must meet or exceed WCAG 2.1 AA success criteria, particularly concerning perceivability and operability.
*   **High-Contrast Atlassian Color Compliance:** The new Atlassian-inspired color palette must be rigorously tested for contrast ratios. Text (including muted secondary text) against background colors must maintain a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text. Focus indicators and primary action buttons (e.g., `#0052CC`) must provide sufficient contrast against their surrounding elements.
*   **Keyboard Navigation & Focus Management:**
    *   Full navigability using only the `Tab`, `Shift+Tab`, `Enter`, `Space`, and Arrow keys.
    *   Visible focus indicators must be clearly defined for all interactive elements, matching the new design system's aesthetic without relying solely on color changes (e.g., using a pronounced focus ring).
*   **ARIA Roles & Semantic HTML:**
    *   Proper heading hierarchy (H1-H6) must be maintained to provide structural context for assistive technologies.

## 4. Teams and Responsibilities
To ensure the vital success of this global UI overhaul, the following tasks are explicitly assigned to specific agent profiles from the `/agents` directory:

### 1. Design & UX Architecture
*   **Agent Assigned:** `design-ux-architect`
*   **Second Chair / Reviewer:** `engineering-frontend-developer` (Ensures design tokens and Figma components are technically feasible and straightforward to implement).
*   **Tasks:** Defines overall layout strategies, navigation patterns, and user flows. Owns this document and ensures all components align with the Atlassian-inspired vision. Creates Figma components and design tokens.

### 2. Frontend Engineering
*   **Agent Assigned:** `engineering-frontend-developer`
*   **Second Chair / Reviewer:** `design-ux-architect` (Conducts visual QA during implementation to ensure code perfectly matches design system fidelity).
*   **Tasks:** Oversees the implementation of the new design system in code (Tailwind configuration, CSS modules, or styled-components). Manages the global layout shell and state updates.

### 3. Quality Assurance
*   **Agent Assigned:** `testing-evidence-collector`
*   **Second Chair / Reviewer:** `design-inclusive-visuals-specialist` (Provides specialized oversight on WCAG 2.1 AA compliance, contrast ratios, and accessibility testing).
*   **Tasks:** Develops comprehensive visual regression test plans and manual test checklists to ensure the new design system is applied perfectly across all browsers and devices. Verifies responsive behavior and WCAG compliance.

### 4. Product & Project Management
*   **Agent Assigned:** `product-manager`
*   **Second Chair / Reviewer:** `git-workflow-master` (Ensures that the epic breakdown and task routing adhere strictly to the project's git branching and handoff mandates).
*   **Tasks:** Prioritizes tasks, defines MVP scope for the redesign, manages sprint boards, and ensures the redesign aligns with broader product strategy and epic workflows.

## 5. Global User Flow Impact
Transitioning to an Atlassian/LLM-style paradigm introduces significant alterations to the navigation and user journeys across the entire application:
*   **Fluid Navigation Paradigm:** Moving away from distinct page reloads, the app will adopt a single-page application (SPA) feel with a persistent collapsible left sidebar. Global navigation, recent workspaces, and settings become accessible overlays rather than distinct URL destinations.
*   **Intent-Driven Onboarding:** The global user flow is inverted; instead of navigating to a specific module to start work, users land on an empty-state central prompt where their initial intent dictates the workspace's configuration.
*   **Contextual Multi-Pane Workflows:** Traditional top-down page layouts are replaced with a persistent active workspace center and a collapsible right-hand detail drawer. This consolidates data presentation, ensuring users don't need to leave the "active chat" context to view settings, extracted details, or PRDs.
*   **Component Universality:** All form fields, buttons, and modals across existing pages (Marketplace, RBACManager, AnalyticsDashboard) will dynamically adopt the Atlassian styling tokens, bringing disparate views into unified aesthetic compliance.

## 6. Operational Procedures & Handoffs
To comply with global `.clinerules` and ensure a smooth transition from design to development, the following operational procedures are mandated for this phase.

### Git & Branching Strategy
*   **Epic Branch:** All work related to the global design system redesign must occur on a dedicated epic branch (e.g., `epic/ui-redesign-global-system`).
*   **Strict Sequencing Rule:** To prevent massive merge conflicts on shared layout components, the `epic/ui-redesign-global-system` branch MUST be completed and merged into a shared staging branch *before* the `intro-page` and `chat-scope` feature branches are created off of it.
*   **Feature Branches:** Developers must branch off the epic branch for specific component implementations and submit Pull Requests back to the epic branch.
*   **No Main Commits:** Direct commits to `main` are strictly prohibited.

### Design to Development Handoff Protocol
*   The `design-ux-architect` must finalize all Figma components and design tokens (JSON/CSS variables) and link them in this document or a central repository.
*   A formal handoff meeting (or async sign-off) must occur before frontend engineering begins.

### QA Gate & Final Sign-off
*   Before the epic branch can be merged into `main`, the `testing-evidence-collector` must provide a formal sign-off report.
*   The sign-off must include visual regression test results, responsive layout checks, and automated accessibility (WCAG 2.1 AA) reports.

| Role | Agent | Sign-off Status | Date | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Design Architect** | `design-ux-architect` | [ ] Pending | | Design tokens & Figma components finalized |
| **Frontend Lead** | `engineering-frontend-developer` | [ ] Pending | | Code implementation complete |
| **QA / Evidence Collector** | `testing-evidence-collector` | [ ] Pending | | Visual regression & accessibility passed |
| **Product Manager** | `product-manager` | [ ] Pending | | Epic goals met, ready for merge |
