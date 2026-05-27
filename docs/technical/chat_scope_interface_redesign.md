# Chat Scope Interface Redesign Plan

## 1. Overview
This document outlines the redesign for the `ChatScopeInterface` (Project Scope page), aiming to resolve existing layout issues and implement the new active-chat patterns.

> **Parallel Execution Note:** This document is part of a three-pronged, coordinated parallel design effort. Decisions made here must synchronize with the [Global Design System Plan](global_design_system_plan.md) and the [Intro Page Redesign Plan](intro_page_redesign_plan.md).

## 2. ChatScopeInterface (Project Scope Page) Fixes & Updates
The `ChatScopeInterface` will be refactored to align with the new global design system and resolve existing layout issues.

### Current Issues to Fix
*   Hardcoded 50/50 split on desktop creates awkward spacing on varied screen sizes.
*   Cluttered presentation of extracted project details.
*   Inconsistent styling compared to the new Atlassian-inspired direction.

### Proposed Architecture
*   **Main Chat Area:** Follows the LLM active state model. The chat history occupies the main scrollable area with a streamlined input area pinned to the bottom. Message bubbles will adopt the new enterprise aesthetic.
    *   **RBAC Condition (Client Approver):** The chat input is restricted to feedback and approval confirmations.
    *   **RBAC Condition (Client Viewer):** The chat input box is completely disabled/hidden to enforce read-only monitoring.
*   **Contextual Details Panel (Right):** The extracted project details (Project Name, Description, Tech Stack, Draft PRD) will be moved to a collapsible right-hand drawer or sidebar. This allows users to focus purely on the chat when needed and pull up details on demand.
*   **Responsive Behavior:** On smaller screens, both the left navigation and the right details panel will retreat behind hamburger menus or slide-over panels.

## 3. Accessibility focus
*   **Keyboard Navigation & Focus Management:**
    *   **Slide-out Menus & Drawers:** When a side navigation panel or contextual details drawer is opened, focus must automatically shift into the drawer, be trapped within the drawer while it is open, and return to the trigger element when closed. The `Esc` key must reliably close any open overlay, modal, or drawer.
*   **ARIA Roles & Semantic HTML:**
    *   **Search/Chat Components:** The central oversized search/input bar and chat interfaces must utilize appropriate ARIA roles (e.g., `role="search"`, `role="log"`).
    *   **Streaming Announcements:** For dynamic LLM chat message generation, the interface must use a debounced `aria-live="polite"` region to announce incoming text chunks gracefully, ensuring screen readers are updated without being overwhelmed by rapid token streaming.
    *   **Interactive Elements:** All buttons, dropdowns, and collapsible panels must have explicitly defined `aria-expanded`, `aria-controls`, and descriptive `aria-label` attributes where visible text is absent or insufficient (such as icon-only buttons in the side navigation).

## 4. Teams and Responsibilities
To ensure the vital success of this redesign, tasks are explicitly assigned to specific agent profiles from the `/agents` directory:

### 1. Design & UX Architecture
*   **Agent Assigned:** `design-ux-architect`
*   **Second Chair / Reviewer:** `product-manager` (Confirms that the three-pane architecture surfaces the essential PRD and Tech Stack data efficiently for user workflows).
*   **Tasks:** Defines layout strategies, navigation patterns, and user flows for the ChatScope interface. Designs the collapsible right-hand contextual drawer and unified chat bubbles.

### 2. Frontend Engineering
*   **Agent Assigned:** `engineering-frontend-developer`
*   **Second Chair / Reviewer:** `design-ux-architect` (Validates the responsive behavior and visual consistency of the collapsible details panel and chat bubbles across all breakpoints).
*   **Tasks:** Refactors the hardcoded 50/50 split into the new multi-pane architecture. Implements the collapsible details panel, dynamic chat history area, and responsive slide-over functionality for mobile.

### 3. Quality Assurance
*   **Agent Assigned:** `testing-evidence-collector`
*   **Second Chair / Reviewer:** `design-inclusive-visuals-specialist` (Specifically reviews focus trapping within the side-drawers and the semantic ARIA labeling for the dynamic chat log).
*   **Tasks:** Verifies responsive behavior of the ChatScope interface across breakpoints. Tests drawer interactions, ARIA role announcements, chat input accessibility, and strict focus trapping for side panels.

## 5. Global User Flow Impact
The ChatScope Interface redesign consolidates the operational workflow into a focused, singular view:
*   **Workspace Convergence:** By moving project details to a right-hand collapsible drawer, users no longer need to switch tabs or split their screen uncomfortably to reference contextual data (like PRDs) while actively engaging with the agent.
*   **Seamless Transitions:** Following the Intro Page prompt, users fluidly land in this interface with their context already loaded. The journey shifts from "navigate to data view -> navigate to chat view" into a unified "chat with data on demand" paradigm.
*   **Scalable Interaction Model:** This three-pane architecture (Hybrid Left Nav, Main Chat, Right Details) sets a standard layout pattern that can be reused across other modules (e.g., custom agent creator, marketplace), standardizing the user journey globally while still providing explicit Workspace Tool access in the left navigation.

## 6. Operational Procedures & Handoffs
To comply with global `.clinerules` and ensure a smooth transition from design to development, the following operational procedures are mandated for this phase.

### Git & Branching Strategy
*   **Epic Branch:** All work related to the Chat Scope interface redesign must occur on a dedicated epic branch (e.g., `epic/ui-redesign-chat-scope`). 
*   **Sequencing Dependency:** This branch must ONLY be created by branching off the merged staging branch of the `epic/ui-redesign-global-system` to prevent layout merge conflicts.
*   **No Main Commits:** Direct commits to `main` are strictly prohibited. Development must occur on branches and merge via Pull Request.

### Design to Development Handoff Protocol
*   The `design-ux-architect` must finalize all structural layouts for the three-pane architecture, including precise behaviors for the right-hand collapsible drawer across all breakpoints.
*   A formal review of the layout logic must occur with the `engineering-frontend-developer` prior to implementation.

### QA Gate & Final Sign-off
*   Before merging, the `testing-evidence-collector` must provide a formal sign-off report.
*   The sign-off must explicitly verify focus trapping within the right-hand drawer, slide-over panel behavior on mobile devices, and that the chat input remains fully accessible.

| Role | Agent | Sign-off Status | Date | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Design Architect** | `design-ux-architect` | [ ] Pending | | Three-pane layouts & responsive behavior finalized |
| **Frontend Lead** | `engineering-frontend-developer` | [ ] Pending | | Code implementation complete |
| **QA / Evidence Collector** | `testing-evidence-collector` | [ ] Pending | | Focus traps & mobile interactions verified |
| **Product Manager** | `product-manager` | [ ] Pending | | Epic goals met, ready for merge |