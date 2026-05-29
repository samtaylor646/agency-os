# Sprint 4.3: Frontend & Marketplace Technical Specification

## 1. Overview
This specification focuses on the UI Implementation for Pods, Memory, and the Marketplace using React and Tailwind CSS. The goal of this sprint is to deliver a highly interactive, responsive, and visually cohesive frontend that enables users to engage with multi-agent pods, inspect semantic memory context, and browse available agents/pods within the AgencyOS marketplace.

## 2. Epic-4.3.A: Implement Multi-Agent Chat Interface (Pod View)
**Objective**: Build a cohesive chat interface that visualizes collaboration among multiple agents within a single thread.

**Key Components**:
*   `PodChatContainer`: The main wrapper for the multi-agent chat interface.
*   `AgentMessageBubble`: A visually distinct message component that indicates which agent is speaking (via avatar, color coding, or badge).
*   `PodThreadTimeline`: A visual indicator showing the execution pipeline and current active agent.
*   `ChatInputBar`: Input mechanism for user intervention or prompting.

**Backend Integration**:
*   Hooks into the `agent_sessions` backend endpoints to fetch historical session data and stream agent responses in real-time.
*   Parses session JSON to differentiate between system messages, user prompts, and individual specialized agent outputs.

## 3. Epic-4.3.B: Implement Memory Inspector Panel
**Objective**: Provide a side panel UI to expose semantic memory (RAG) retrieved context for transparency and debugging of agent executions.

**Key Components**:
*   `MemoryInspectorSidebar`: A collapsible right-hand side panel.
*   `ContextCard`: Displays individual pieces of retrieved context (documents, past interactions, tool outputs) with their metadata.
*   `RelevanceScoreBadge`: A visual indicator showing the similarity/relevance score of the context to the query.
*   `AgentExecutionSelector`: Allows the user to select which specific agent's execution memory is currently being inspected.

**Backend Integration**:
*   Fetches from memory inspection endpoints to populate the RAG context details for the selected execution context.

## 4. Epic-4.3.C: Build Foundational Marketplace UI Components
**Objective**: Create the building blocks for the AgencyOS marketplace to allow users to discover, evaluate, and install new agents and pods.

**Key Components**:
*   `MarketplaceGrid`: A responsive Tailwind CSS Grid layout container for marketplace items.
*   `EntityCard`: A reusable card component for both Agents and Pods, displaying title, description, creator, capabilities, and visual tags.
*   `EntityDetailModal`: A comprehensive modal providing deep-dive details, version history, required permissions, and an "Install/Enable" action.
*   `FilterSidebar`: A sidebar for filtering by domain categories (e.g., Marketing, Development, Strategy) and sorting preferences.

## 5. Sprint Execution / Todo Plan

### Epic-4.3.A (Pod View)
- [x] Scaffold `PodChatContainer` component and define routing.
- [x] Implement `AgentMessageBubble` with dynamic styling and avatars based on agent identity.
- [x] Integrate with `agent_sessions` endpoint to load and parse multi-agent thread data.
- [x] Build `PodThreadTimeline` to show execution status and agent handoffs.
- [x] Wire up real-time session streaming.

### Epic-4.3.B (Memory Inspector)
- [x] Scaffold `MemoryInspectorSidebar` layout and CSS transitions.
- [x] Build `ContextCard` and `RelevanceScoreBadge` UI components.
- [x] Implement state management to tie the inspector to the currently focused agent execution.
- [x] Implement API calls to fetch Semantic Memory/RAG data for the active view.

### Epic-4.3.C (Marketplace UI)
- [x] Create the primary `MarketplaceGrid` layout.
- [x] Implement the responsive `EntityCard` component using Tailwind.
- [x] Build the `FilterSidebar` component and integrate category filtering state.
- [x] Implement the `EntityDetailModal` with overview and permission tabs.
- [x] Finalize responsive design across mobile, tablet, and desktop viewports.