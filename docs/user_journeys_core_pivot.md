# User Journeys: Conversational Project Creation

This document outlines the primary user journeys focusing on the new conversational entry point and AI orchestration pipeline.

## Journey 1: The "Napkin Pitch" to Executable Plan

**Persona:** Startup Founder with an idea but lacking detailed technical specs.

1. **Entry:** User logs into Agency OS and clicks the prominent "Create New Project" button, which opens a chat interface.
2. **The Pitch:** User types, "I want to build a simple web app where users can upload recipes and generate grocery lists."
3. **Discovery Conversation:**
   - The Orchestrator AI responds, "Great idea! To help me scope this, will users need to create accounts? And do you have a preference for the tech stack?"
   - User answers: "Yes, basic email login. Let's use React and Node.js."
4. **Automated Scoping:** The AI processes the conversation and generates a draft PRD, Technical Spec, and Initial Task List.
5. **Review & Approval:** The AI presents the generated documents in a split-view (Chat on left, Docs on right). The user reviews and says, "Looks good, but let's add a feature to share recipes via a link."
6. **Refinement:** The AI instantly updates the PRD and Task List. User clicks "Approve Plan."

## Journey 2: Orchestration and Execution

**Persona:** Product Manager executing an approved plan.

1. **Agent Assignment:** Upon plan approval, the Orchestrator AI automatically selects the necessary agents (e.g., `frontend-developer`, `backend-architect`, `ux-designer`).
2. **Kickoff:** The Orchestrator initiates the Nexus Pipeline. The UX Designer agent begins drafting wireframe descriptions or component structures.
3. **Handoff:** Once UX is approved (auto-approved based on confidence or user-approved), the Frontend Developer agent starts writing React code.
4. **Execution Visibility:** The user watches a "Project Dashboard" where agents are visualized as active nodes. They can see logs of what the Frontend Developer agent is currently coding.
5. **Intervention (Optional):** The user notices the agent chose a blue color scheme and types in the project chat, "Make the primary theme green instead." The Orchestrator intercepts this, updates the context, and instructs the active agent to pivot.
6. **Delivery:** Agents complete their tasks, run tests (via QA agents), and present the final build for user review.

## Journey 3: Micro-Tasking via Chat

**Persona:** Developer needing a quick asset or script.

1. **Entry:** User opens the universal command chat (Cmd+K or persistent chat bar).
2. **Command:** "Write a Python script to parse these specific CSVs in my current workspace and output a JSON summary."
3. **Execution:** The Orchestrator bypasses the heavy project scoping, instantly assigns a `python-developer` agent, runs the script in the secure sandbox, and returns the JSON file to the workspace.