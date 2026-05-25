# User Journeys: Conversational Project Creation & Orchestration

This document outlines the primary user journeys focusing on the new conversational entry point and AI orchestration pipeline (Nexus Pipeline), including custom agent creation via the wizard.

## Journey 1: The "Napkin Pitch" to Executable Plan

**Persona:** Startup Founder with an idea but lacking detailed technical specs.

1. **Entry:** User logs into Agency OS and clicks the prominent "Create New Project" button, which opens a chat interface.
2. **The Pitch:** User types, "I want to build a simple web app where users can upload recipes and generate grocery lists."
3. **Discovery Conversation:**
   - The Orchestrator AI responds, "Great idea! To help me scope this, will users need to create accounts? And do you have a preference for the tech stack?"
   - User answers: "Yes, basic email login. Let's use React and Node.js."
4. **Automated Scoping:** The AI processes the conversation and generates a draft PRD, Technical Spec, and Initial Task List.
5. **Review & Sharing:** The AI presents the generated documents in a split-view (Chat on left, Docs on right). The user can export, share via link, or email the docs directly from the interface to ensure external stakeholders stay in the loop. For internal users, the system triggers an alert in their notification center or message inbox requesting their review.
6. **Refinement & Approval:** A user reviews the docs and says, "Looks good, but let's add a feature to share recipes via a link." The AI instantly updates the PRD and Task List. Once all parties are satisfied, the authorized user clicks "Approve Plan."

## Journey 2: Orchestration and Execution (The Nexus Pipeline)

**Persona:** Product Manager executing an approved plan.

1. **Agent Assignment:** Upon plan approval, the Orchestrator AI automatically selects the necessary agents (e.g., `frontend-developer`, `backend-architect`, `ux-designer`).
2. **Kickoff:** The Orchestrator initiates the Nexus Pipeline (per [Nexus Strategy](../../agents/strategy/nexus-strategy.md)). The UX Designer agent begins drafting wireframe descriptions or component structures.
3. **Handoff:** Once UX is complete, it triggers the same notification and approval flow (internal alerts, external sharing). Once approved (or auto-approved based on confidence), the Frontend Developer agent starts writing React code.
4. **Execution Visibility:** The user watches a "Project Dashboard" where agents are visualized as active nodes. They can see logs of what the Frontend Developer agent is currently coding.
5. **Intervention (Optional):** The user notices the agent chose a blue color scheme and types in the project chat, "Make the primary theme green instead." The Orchestrator intercepts this, updates the context, and instructs the active agent to pivot.
6. **Delivery & Final Approval:** Agents complete their tasks and run tests (via QA agents). The final build is presented for user review, utilizing the same robust sharing and notification systems for final stakeholder sign-off.

## Journey 3: Micro-Tasking via Chat

**Persona:** Developer needing a quick asset or script.

1. **Entry:** User opens the universal command chat (Cmd+K or persistent chat bar).
2. **Command:** "Write a Python script to parse these specific CSVs in my current workspace and output a JSON summary."
3. **Clarification (Optional):** If the request is ambiguous, the Orchestrator quickly prompts for parameters: "Which specific folder are the CSVs located in, and what data fields should the JSON contain?"
4. **Script Generation & Approval:** The Orchestrator bypasses heavy project scoping, instantly assigns a `python-developer` agent, and generates the script. The proposed script is presented to the user for review and approval before execution.
5. **Execution:** Once the user approves the script, the Orchestrator runs the script in the secure sandbox and returns the JSON file to the workspace.
6. **Review & Iteration:** The user reviews the output and replies in the chat, "Looks close, but please include the 'date' column in the JSON." The agent instantly refines the script, requests approval again if necessary, re-runs it, and updates the final output.

## Journey 4: Document-Driven Ingestion

**Persona:** Product Manager with existing documentation from another tool.

1. **Entry:** User clicks "Create Project via Document Upload" and drops a 5-page PDF PRD into the workspace.
2. **Analysis:** The Orchestrator AI ("Analysis Agent") reads the document, extracting the core features, constraints, and user stories.
3. **Pipeline Generation:** Instead of a lengthy chat, the AI immediately outputs a structured Task Pipeline and assigns specialized agents to the generated epics.
4. **Review & Execute:** The user reviews the mapped pipeline, makes minor adjustments, and clicks "Execute" to begin the Nexus Pipeline.

## Journey 5: Custom Agent Creation Wizard

**Persona:** Agency Owner needing a niche expert not available in the default roster.

1. **Entry:** User navigates to the Agent Registry and clicks "Create Custom Agent". This launches the Multi-Step Wizard.
2. **Step 1 - Identity:** User enters Name ("HubSpot CRM Expert"), Role, and Version.
3. **Step 2 - Rules & Constraints:** User defines the system rules path and specific behavioral constraints.
4. **Step 3 - Capabilities:** User defines a markdown list of what the agent is capable of doing.
5. **Step 4 - System Prompt:** User provides the detailed operational prompt and reviews the overall configuration before submitting.
6. **Export/Save:** The backend parses this into the standard `agency-agents` schema (YAML frontmatter + markdown) and saves it.
7. **Utilization:** The user creates a new task "Configure HubSpot pipelines" and the Orchestrator successfully assigns it to the newly created custom agent.