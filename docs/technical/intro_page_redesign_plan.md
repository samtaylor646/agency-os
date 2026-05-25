# Intro Page Redesign Plan

## 1. Overview
This redesign focuses on the intro/home experience to match modern LLMs (e.g., ChatGPT, Claude).

> **Parallel Execution Note:** This document is part of a three-pronged, coordinated parallel design effort. Decisions made here must synchronize with the [Global Design System Plan](global_design_system_plan.md) and the [Chat Scope Interface Redesign Plan](chat_scope_interface_redesign.md).

## 2. Intro/Home Page Redesign (Modern LLM Style)
The app's entry point will be redesigned to mirror the focused, intent-driven interfaces of modern LLMs.

### Layout Strategy
*   **Collapsible Left Menu (Hybrid Sidebar):** A standard side navigation panel that balances the "chat-first" approach with necessary B2B operating system controls (similar to Gemini's "Gems" or Claude's "Projects").
    *   **Included Items:** Global navigation ("New Chat" / Home), Recent workspaces / Chat history, a **"Workspace Tools"** section (Custom Agents, Analytics, Marketplace, Files) for rapid state management, and bottom-pinned utility links (Settings, Access Control, Audit Logs, Workflows).
*   **Centered Main Workspace (Empty State):** A clean, distraction-free central layout featuring:
    *   A prominent welcome message.
    *   Suggested prompt chips or quick-action buttons (e.g., "Start a new project," "Analyze documents").
    *   A central, oversized search/input bar for immediate interaction.
    *   **RBAC Condition:** The Intro Page is the exclusive landing page for `Agency Admin` and `Agency Staff`. `Client Approver` and `Client Viewer` roles bypass this entirely and land directly on the Client Dashboard.
*   **Transition to Active State:** Upon input submission, the central bar animates to the bottom or top (depending on context), and the main area populates with the active session or results.

## 3. Accessibility Focus
*   **Search/Chat Components:** The central oversized search/input bar must utilize appropriate ARIA roles (e.g., `role="search"`) to announce updates to screen readers dynamically.
*   **Interactive Elements:** All buttons, dropdowns, and collapsible panels must have explicitly defined `aria-expanded`, `aria-controls`, and descriptive `aria-label` attributes where visible text is absent or insufficient.

## 4. Teams and Responsibilities
To ensure the vital success of this redesign, tasks are explicitly assigned to specific agent profiles from the `/agents` directory:

### 1. Design & UX Architecture
*   **Agent Assigned:** `design-ux-architect`
*   **Second Chair / Reviewer:** `product-manager` (Ensures the intent-driven empty states and quick-action buttons perfectly align with the target user journey and business goals).
*   **Tasks:** Defines layout strategies, navigation patterns, and user flows for the Intro Page. Drafts empty states, onboarding flows, and microcopy to ensure a premium modern LLM feel. Identifies and corrects any UX regressions (such as the accidental re-introduction of legacy sidebar menus).

### 2. Frontend Engineering
*   **Agent Assigned:** `engineering-frontend-developer`
*   **Second Chair / Reviewer:** `design-ux-architect` (Reviews the implementation of central search bar animations and layout shifts for smoothness, timing, and design fidelity).
*   **Tasks:** Implements the Intro Page layout. Builds reusable components (Sidebar, Collapsible Panels) adhering to the global design system. Handles the animation of the central search bar transitioning to the active workspace state. **Immediate Task:** Implement the "Hybrid Sidebar" by reinstating the "Workspace Tools" section (Agents, Analytics, Marketplace, Files) ensuring correct role-based visibility.

### 3. Quality Assurance
*   **Agent Assigned:** `testing-evidence-collector`
*   **Second Chair / Reviewer:** `design-inclusive-visuals-specialist` (Verifies ARIA roles, screen reader announcements, and strict keyboard focus management for the action-first interface).
*   **Tasks:** Verifies responsive behavior of the Intro Page and tests drawer interactions, ARIA role announcements, screen reader compatibility, and focus traps.

## 5. Global User Flow Impact
Implementing an LLM-style Intro Page fundamentally alters the application's entry flow:
*   **Immediate Action Over Exploration:** The default dashboard is replaced by an action-first prompt interface. Users bypass traditional navigation menus to declare their intent immediately, compressing the funnel from "login to action."
*   **Contextual Initialization & Disambiguation:** The transition from the empty state to the active state signifies workspace instantiation. The flow dynamically loads the necessary context based on the user's initial prompt. **Disambiguation UI State:** If the backend intent parser cannot confidently determine the user's goal, the UI must gracefully display a disambiguation state offering clarifying quick-action chips before attempting to route to the Chat Scope.
*   **Conversational Core with Explicit Tools:** While project scoping and general tasks are driven through the central conversational funnel, essential B2B admin tools (like Custom Agents, Analytics, and Marketplace) are explicitly accessible via the "Workspace Tools" in the Hybrid Sidebar, eliminating the friction of conversational routing for complex state management.

## 6. Operational Procedures & Handoffs
To comply with global `.clinerules` and ensure a smooth transition from design to development, the following operational procedures are mandated for this phase.

### Git & Branching Strategy
*   **Epic Branch:** All work related to the Intro Page redesign must occur on a dedicated epic branch (e.g., `epic/ui-redesign-intro-page`). 
*   **Sequencing Dependency:** This branch must ONLY be created by branching off the merged staging branch of the `epic/ui-redesign-global-system` to prevent layout merge conflicts.
*   **No Main Commits:** Direct commits to `main` are strictly prohibited. Development must occur on branches and merge via Pull Request.

### Design to Development Handoff Protocol
*   The `design-ux-architect` must finalize all wireframes, responsive layouts, and state transitions (e.g., empty state to active state) before development begins.
*   The handoff must include clear specifications for the central search bar animation and layout shifts.

### QA Gate & Final Sign-off
*   Before merging, the `testing-evidence-collector` must provide a formal sign-off report focusing specifically on the new entry flow, animation performance, and screen reader announcements (`aria-live`, `role="search"`).

| Role | Agent | Sign-off Status | Date | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Design Architect** | `design-ux-architect` | [ ] Pending | | Wireframes & transitions finalized |
| **Frontend Lead** | `engineering-frontend-developer` | [ ] Pending | | Code implementation & animations complete |
| **QA / Evidence Collector** | `testing-evidence-collector` | [ ] Pending | | Responsive flow & ARIA roles verified |
| **Product Manager** | `product-manager` | [ ] Pending | | Epic goals met, ready for merge |