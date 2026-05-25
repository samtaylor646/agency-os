# MASTER PROMPT: CORE PIVOT GUARDRAILS

**ATTENTION ALL AGENTS, DEVELOPERS, AND ORCHESTRATORS:**
This document serves as the absolute strategic guardrail for the AgencyOS project. You MUST adhere to these rules without exception. Any deviation is considered a failure of the current task.

## 🚫 ZERO ENTERPRISE DRIFT POLICY
**DO NOT** build, suggest, or plan ANY enterprise features until the Core Loop is proven in the backend/terminal.
This prohibition includes, but is not limited to:
- User Interfaces (UI) / Frontend Applications (React, Vite, Tailwind)
- Role-Based Access Control (RBAC)
- Complex User Management, Authentication, or Multi-tenancy
- Analytics Dashboards
- Billing / Subscriptions
- Marketplaces

## 🎯 THE ONE AND ONLY GOAL: THE CORE LOOP
Our sole focus is achieving a functional, CLI/API-driven Core Loop. The project is NOT ready for a frontend until this backend loop executes flawlessly.

**The Core Loop consists strictly of:**
1. **Project Creation & Ingestion:** Ingesting a user request/objective via API, CLI, or by uploading unstructured documents (PRDs, briefs).
2. **AI Scoping:** The LLM dynamically interpreting the request (and uploaded docs), breaking it down into an execution graph, and mapping it to specialized agents (including dynamically loaded custom agents via `agency-agents` format).
3. **Agent Execution:** Orchestrating the necessary agents to execute the scoped tasks and compile the final output.

## 🛠️ OPERATIONAL MANDATES
1. **Function over Form:** All implementations must favor backend execution, API endpoints, or CLI interfaces.
2. **Cut the Fat:** If a task asks you to update UI components, **STOP**. Politely refuse the task citing this Master Prompt and pivot the focus to backend API/LLM integration.
3. **Prove the Value First:** The product's value is agentic execution, not a pretty wrapper. We must prove the LLM can accurately orchestrate agents before we build the GUI wrapper.

**By reading this, you are bound to these constraints. Drift will not be tolerated.**