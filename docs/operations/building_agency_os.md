# Continuing Development on AgencyOS

This document outlines the workflow and specialized agents required to continue building and extending the AgencyOS framework itself.

## Selected Roo Modes (.roomodes)

We have configured a specific set of custom modes in `.roomodes` to facilitate a structured multi-agent development pipeline (NEXUS) specifically for improving this repository.

### 1. Agents Orchestrator (`agents-orchestrator`)
**Role:** Pipeline Controller & Manager
**Usage:** Start here for any major feature addition. The orchestrator will break down the task, define the quality gates, and dictate the order of operations for the other agents.

### 2. UX Architect (`ux-architect`)
**Role:** Interface & Flow Designer
**Usage:** Switch to this mode when designing new dashboard views in `/client` or structuring new agent configuration formats in `/agents`. They ensure consistency and usability.

### 3. Senior Developer (`senior-developer`)
**Role:** Premium Implementation Specialist
**Usage:** Switch to this mode to write the actual code (e.g., React/Vite components in `/client` or Python backend logic in `/server`). They follow the architectural specs and implement the features.

### 4. Evidence Collector (`evidence-collector`)
**Role:** Quality Assurance & Verifier
**Usage:** Once the Senior Developer finishes a task, switch to this mode to run tests, build scripts, and verify the implementation objectively. They are the gatekeeper before a feature is considered "done."

## Development Dev/QA Loop

When building new features for AgencyOS, adhere to the standard NEXUS Dev/QA loop:

1. **Planning:** Orchestrator defines the scope and handoff to the Architect.
2. **Design:** UX Architect outlines the interface and data flow.
3. **Build:** Senior Developer implements the code based on the design.
4. **Verify:** Evidence Collector runs the tests (e.g., `npm run build` in `/client`).
5. **Harden:** If verification fails, the task returns to the Developer. If it passes, the Orchestrator marks the phase complete.