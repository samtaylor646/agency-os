# Agency OS: Product Overview

## The Vision
Agency OS has established a robust enterprise foundation (RBAC, Multi-Tenancy, Audit Logging). The strategic vision focuses on delivering the **Core Engine**: an AI Orchestration and Conversational Project Creation workflow. We are transforming Agency OS from a management framework into an active, intelligent partner that seamlessly translates user intent into executed projects via a conversational interface and autonomous agents.

## Core Value Proposition
"From Conversation to Creation." Agency OS empowers users to simply talk to the system about what they want to build, and the system intelligently scopes, plans, and executes the project by orchestrating specialized AI agents.

## Key Features (The Core Engine)

1. **Conversational Onboarding & Project Creation:**
   - Chat-centric interface as the primary entry point for new projects.
   - Natural language processing to understand user goals, constraints, and requirements.
   - Dynamic prompt generation to extract necessary details from the user.

2. **AI Scoping & Requirements Generation:**
   - Automated generation of Product Requirements Documents (PRDs), engineering specs, and task breakdowns based on the conversational input.
   - Iterative refinement loop: the AI proposes a scope, and the user refines it via chat.

3. **Intelligent Agent Orchestration (The Nexus Pipeline):**
   - Dynamic selection of appropriate specialized agents from the registry based on project requirements (Guided by [Nexus Strategy](../../agents/strategy/nexus-strategy.md)).
   - Support for user-defined **Custom Specialized Agents**, interoperable via the standard `agency-agents` format, allowing domain-specific tasks (e.g., WordPress/Salesforce). Users can create these agents via a comprehensive multi-step UI wizard.
   - Automated handoffs and coordination between agents (e.g., Product Manager agent hands off to UI Designer agent, then to Frontend Developer agent).

4. **Document-Driven Task Ingestion:**
   - Seamlessly convert existing documentation into action.
   - Upload PRDs, briefs, or meeting notes to have the Orchestrator extract requirements and automatically seed the project's execution pipeline.

5. **Transparent Execution & Monitoring:**
   - Real-time visibility into agent activities and task progress.
   - Interactive feedback loops allowing users to intervene, approve, or redirect agents during execution.

## The Foundation (Already Built)
- **Multi-Tenancy & Workspaces:** Secure isolation of projects and resources.
- **Role-Based Access Control (RBAC):** Granular permissions for team members and agents.
- **API Key Management:** Full lifecycle management (generation, secure display, and revocation) of API keys.
- **Audit Logging:** Comprehensive tracking of all actions for compliance and security.

## Target Audience
- Founders and Entrepreneurs looking to rapidly prototype and build MVPs.
- Product Managers and Agencies needing to scale their delivery capacity.
- Developers seeking an intelligent assistant to handle boilerplate, planning, and specialized tasks.