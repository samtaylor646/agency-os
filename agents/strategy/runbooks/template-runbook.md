# 📋 Runbook: [Scenario Name]

> **Mode**: [e.g., NEXUS-Sprint, NEXUS-Micro] | **Duration**: [e.g., 2-4 weeks] | **Agents**: [e.g., 5-10]

---

## Scenario

[Brief, 2-3 sentence description of the specific business or technical goal this runbook aims to achieve. State the required speed vs. quality constraints.]

## Agent Roster

*Identify the required agents from the `/agents` directory and define their exact roles for this scenario.*

### Core Team
| Agent | Role / Responsibility |
|-------|-----------------------|
| Agents Orchestrator | Pipeline controller & Handoff manager |
| [Agent Name] | [Specific task ownership] |
| [Agent Name] | [Specific task ownership] |

### Support / QA Team
| Agent | Role / Responsibility |
|-------|-----------------------|
| Evidence Collector | Primary QA and verification |
| [Agent Name] | [Specific task ownership] |

## Execution Plan

*Define the step-by-step or week-by-week pipeline. Clearly articulate inputs, processes, and outputs for each step.*

### Phase 1: [Phase Name] (Timeframe)

```text
Step 1: [Action Name]
├── [Agent Name] → [Specific atomic task]
│   ├── Input: [What they need to start]
│   └── Output: [Exact deliverable required]
└── [Agent Name] → [Specific atomic task]

Step 2: [Action Name]
├── [Agent Name] → [Specific atomic task]
└── Quality Gate: [What must be approved before Phase 2]
```

### Phase 2: [Phase Name] (Timeframe)

```text
Sprint 1:
├── Agents Orchestrator → Dev↔QA loop management
├── [Agent Name] → [Task]
├── [Agent Name] → [Task]
└── Evidence Collector → QA every task using PASS/FAIL templates
```

## Handoff & QA Protocols

*Specify the exact coordination mechanisms needed for this runbook.*

- **Developer -> QA:** Must use Standard Handoff Template.
- **QA Verifications:** Must use NEXUS QA Verdict PASS/FAIL template.
- **Max Retries:** 3 attempts. Upon 3rd failure, generate Escalation Report.

## Success Criteria (KPIs)

*How do we know this runbook executed successfully?*

| Metric | Target | Verification Method | Owner |
|--------|--------|---------------------|-------|
| [Metric Name] | [Target Value] | [How to measure] | [Agent] |
| [Metric Name] | [Target Value] | [How to measure] | [Agent] |

## Key Decisions & Human-in-the-Loop Gates

| Decision Point | When it happens | Who Decides (Agent or Human) |
|----------------|-----------------|------------------------------|
| [Decision] | [Phase/Step] | [Decision Maker] |

## Common Pitfalls & Mitigations

| Pitfall | Mitigation Strategy | Enforcing Agent |
|---------|---------------------|-----------------|
| [Risk 1] | [How to prevent it] | [Agent Name] |
| [Risk 2] | [How to prevent it] | [Agent Name] |
