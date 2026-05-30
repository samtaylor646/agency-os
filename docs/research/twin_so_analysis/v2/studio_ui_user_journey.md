# Studio UI User Journey: "Build vs. Run" Paradigm

## 1. Executive Summary
This document outlines the User Experience (UX) and user journey for the AgencyOS V2 Studio UI, heavily informed by the Twin.so "Build vs. Run" research. The journey is designed to support rapid, cost-effective agent development while ensuring strict separation between testing (Sandbox) and production (Run) environments.

## 2. Target User Persona
*   **Primary User:** Prompt Engineers, Solution Architects, and Developers.
*   **Goal:** To iteratively build, test, and refine multi-agent pods or single specialized agents without incurring high LLM API costs or risking production data.

## 3. The User Journey Map

### Phase 1: Entry & Configuration (The "Build" Canvas)
*   **Action:** The user enters the "Studio" interface from the AgencyOS dashboard.
*   **UI Experience:** A clean, split-pane layout. The left pane contains the Agent Configuration (System Prompts, Tools, Context), and the right pane is the Sandbox Chat interface.
*   **Key Interaction:** The user defines the agent's role, adds necessary tools, and types out the initial system prompt. The UI clearly indicates that the current state is **"BUILD MODE"** (perhaps through a distinct banner or toggle state).
*   **Behind the Scenes:** The system prepares the ephemeral execution context and network-isolated microVMs for tool testing.

### Phase 2: Iterative Testing (The Sandbox Validation)
*   **Action:** The user types a test query into the Sandbox Chat pane.
*   **UI Experience:** The chat interface responds rapidly. Cost-saving mechanisms are transparently communicated to the user. A small indicator shows "Simulated on gpt-4o-mini" (Automatic Model Degradation) and "Cache Hit" (Semantic Caching) to reassure the user that testing costs are minimized.
*   **Key Interaction:** The user interacts with the agent, testing edge cases and tool invocations. Tools that would normally access production data (like DB writes) display a "Mock Executed" badge.
*   **Behind the Scenes:** LLM routing proxy downgrades premium models. Secret manager blocks production API keys.

### Phase 3: Debugging & Refinement
*   **Action:** The user notices a flaw in the agent's reasoning or tool usage.
*   **UI Experience:** The Sandbox provides a "Trace View" overlay, showing the exact reasoning steps, token usage limits hit (Hard Token Caps), and intermediate tool payloads. 
*   **Key Interaction:** The user modifies the prompt on the left pane. Upon modification, the right pane offers a one-click "Replay Test" button, leveraging the semantic cache for unchanged parts of the conversation.

### Phase 4: Promotion to Production (The "Run" Transition)
*   **Action:** The user is satisfied with the agent's performance in the Sandbox and clicks the "Promote to Production" button.
*   **UI Experience:** A modal appears, summarizing the changes and requesting a version tag. It warns the user that this action will upgrade the underlying model to the premium version (e.g., reverting to `gpt-4o`) and enable full API/data access.
*   **Key Interaction:** The user confirms the deployment. The UI shifts from "BUILD MODE" to "RUN MODE" for that specific agent.
*   **Behind the Scenes:** The system creates an immutable snapshot of the agent configuration, tags it, and deploys it to the dedicated worker queues for live execution.

## 4. Key UX Principles Adopted
*   **Cost Transparency:** Visually reassuring the user that the Sandbox is a safe, cheap place to fail.
*   **Clear State Indication:** Absolute visual clarity between Ephemeral Build state and Persistent Run state.
*   **Rapid Iteration Loops:** Minimizing the friction between editing a prompt and testing the result (Replay Test, Caching).
*   **Safe Failure:** Preventing Sandbox actions from accidentally bleeding into production storage or external APIs.