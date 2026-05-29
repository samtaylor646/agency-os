# KPIs & Success Metrics

## Overview
This document defines the Key Performance Indicators (KPIs) and success metrics for Agency OS. These metrics are designed to measure the effectiveness of the Conversational Core Engine, the Nexus Pipeline orchestration, custom agent adoption, and the overall platform's impact on reducing project initiation friction and execution time. By tracking these KPIs, we ensure the platform delivers on its promise of moving users "From Conversation to Creation" seamlessly.

## Objectives
1. **Reduce Friction:** Minimize the time and effort required to go from project ideation to execution.
2. **Increase Automation:** Maximize the percentage of project scoping and execution handled autonomously by agents.
3. **Enhance Quality & Reliability:** Ensure generated documents and code meet high-quality standards and pass quality assurance gates.
4. **Drive Platform Adoption:** Increase user engagement with custom agents, document ingestion, and the conversational interface.
5. **Ensure Security & Compliance:** Maintain enterprise-grade security and auditing standards throughout the orchestration process.

## Core Metrics

### 1. Acquisition & Onboarding
- **Sign-up to Active Beta Conversion Rate:** Percentage of users who transition from the waitlist/sign-up to actively running their first project pipeline.
- **Time to First Project Execution:** The average time (in hours/days) it takes for a new user to move from their initial chat interaction to triggering a live Nexus Pipeline.
- **Onboarding Drop-off Rate:** The percentage of users who abandon the project creation process during the conversational scoping phase.

### 2. Conversational Engine & Scoping (Planning Phase)
- **Time to First Spec (TTFS):** The average time elapsed from project initiation (the "Napkin Pitch") to a completed, user-approved Product Requirements Document (PRD). *Target: Decrease by 80% compared to traditional manual processes.*
- **Scoping Auto-Approval Rate:** Percentage of AI-generated documents (PRDs, Tech Specs, Task Lists) that are approved by users with minimal or no manual edits.
- **Document Ingestion Usage:** The ratio of projects started via document upload versus manual chat entry.

### 3. Orchestration & Execution (Nexus Pipeline)
- **Agent Orchestration Success Rate:** The percentage of generated task lists successfully executed by `central_runner.py` without requiring manual developer intervention.
- **Average Agents Utilized Per Project:** The mean number of unique specialized agents assigned to execute a standard project pipeline.
- **Mid-Execution Intervention Rate:** The frequency at which users must pause the pipeline to correct agent behavior or adjust requirements via chat. (A lower rate indicates better initial scoping and agent autonomy).
- **Quality Gate Pass Rate:** The percentage of code and deliverables that pass automated QA checks (Evidence Collector) on the first attempt before merging.

### 4. Custom Agents & Extensibility
- **Custom Agent Creation Rate:** The number of new custom agents created per active user/workspace via the Wizard UI.
- **Custom Agent Assignment Rate:** The percentage of tasks within the Nexus Pipeline that are actively assigned to user-defined custom agents versus default system agents.
- **Marketplace Readiness Score:** Volume of successfully proven multi-agent workflows and custom agents documented for future Marketplace seeding.

### 5. Enterprise & Infrastructure (Security/Performance)
- **Pipeline Uptime:** The percentage of time the Nexus Pipeline and `central_runner.py` operate without systemic failure or downtime.
- **Audit Log Coverage:** 100% adherence to tracking all human-in-the-loop approvals, agent executions, and access control changes.
- **API Key Utilization:** Volume of secure API calls routed through the platform's credential manager.

## Tracking & Reporting
- **Real-Time Dashboards:** Key metrics (Execution Visibility, Agent Utilization) will be integrated directly into the `AnalyticsDashboard.jsx` within the Agency OS frontend.
- **Monthly Business Reviews (MBR):** Product management and engineering leads will review these KPIs monthly to identify bottlenecks in the Nexus Pipeline or conversational engine.
- **User Feedback Loops:** Continuous monitoring of qualitative user feedback gathered via the chat interface and formalized UAT processes to provide context behind the quantitative metrics.