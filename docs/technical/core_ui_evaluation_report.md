# Core vs. Technical Redesign Evaluation Report

**Date:** 2026-05-25
**Evaluators:** Product Manager, UX Architect, Business Strategist

## 1. Objective
To evaluate recent UX/UI redesign plans (specifically the `intro_page_redesign_plan.md` "Unified Entry Point" paradigm) against the foundational `/core` documentation (`PRD.md` and `User_Journeys.md`), weighing the pros and cons of proposed deviations, and ensuring all user journeys remain supported.

## 2. Core Documentation Baseline
The `/core` documentation defines Agency OS as a conversational, multi-agent orchestration platform. 
Crucially, **Journey 5** in `User_Journeys.md` states: *"User navigates to the Agent Registry and clicks 'Create Custom Agent'."* 
The `PRD.md` (Req 5.1) also explicitly requires a UI to define custom agents.

## 3. The Deviation: The "Pure Chat" UI
The initial `intro_page_redesign_plan.md` proposed stripping all feature-specific navigation (Agents, Analytics, Files) from the sidebar in favor of a "Unified Entry Point" (a central chat prompt). 

### Pros of "Pure Chat":
*   Mimics the hyper-streamlined experience of ChatGPT or early Claude.
*   Forces users to adopt the conversational interface.
*   Reduces cognitive load upon initial login.

### Cons of "Pure Chat" (The Conflict):
*   **Breaks Core Journeys:** It breaks Journey 5 (Custom Agent Creation) by removing explicit navigation to the Agent Registry.
*   **Friction for Admins:** It introduces massive friction for B2B state management. Asking a chat interface to "Show me the analytics" or "Take me to the custom agent wizard" is an anti-pattern for tasks that require explicit data visualization and form entry.
*   **Deviates from B2B OS Purpose:** Agency OS is an operating system, not just an LLM chatbot. It requires explicit tool management.

## 4. The Resolution: The "Hybrid Sidebar"
The UX team recently corrected this deviation by instituting the **Hybrid Sidebar** (reinstating the "Workspace Tools" section for Agents, Analytics, Marketplace, and Files).

### Evaluation of the Hybrid Approach:
*   **Pros:** Perfectly aligns with the `PRD.md` requirements for explicitly managing custom agents (Req 5.1). Restores functionality for Journey 5. Mirrors the successful UI of Gemini ("Gems") which balances chat with tool management.
*   **Cons:** Slightly more initial UI elements than a pure blank slate.
*   **Verdict:** The Hybrid Sidebar is the **correct strategic choice**. It adheres strictly to the `/core` requirements while still elevating the conversational interface as the primary engine for project creation.

## 5. Required Actions
1. Update `docs/core/User_Journeys.md` to ensure terminology reflects the new "Hybrid Sidebar" (e.g., updating Journey 5 to "User clicks 'Agents' in the Workspace Tools sidebar...").
2. Validate that the "Workspace Tools" section restricts visibility correctly based on RBAC (e.g., Client Approvers should not see the Agent Registry). This ensures we satisfy the core access control requirements.

## 6. Conclusion
The initial design iteration swung too far towards a consumer LLM experience. By evaluating against the `/core` documents, we identified the gap (broken admin workflows) and course-corrected to the Hybrid Sidebar. We are now fully aligned with the core vision.