# 🚨 Runbook: Autonomous Blast Radius Containment

> **Mode**: NEXUS-Micro | **Duration**: Minutes to hours | **Agents**: 2-4

---

## Scenario
An autonomous multi-agent Pod or DAG workflow has entered a failure mode characterized by high velocity, rapid API consumption, unexpected systemic mutation, or hallucination loops. The blast radius must be contained immediately to prevent resource exhaustion, data corruption, or external API penalties.

## Detection Trigger
- Rapid sequence of LLM API failures or quota exhaustion alerts.
- DAG orchestration loops detected (e.g., node recursion limits hit).
- User reports of "rogue" agent behavior within a workspace.

## Containment Sequence (Kill Switch)

### Step 1: Engage Kill Switch (0-2 minutes)
```
Incident Response Commander:
1. Identify the offending Tenant ID (or determine if a Global kill is necessary).
2. Execute the Kill Switch via API:
   POST /kill-switch/activate { "tenant_id": "[ID]" }
3. Verify DAG halts:
   GET /kill-switch/status?tenant_id=[ID]
4. Check DAG execution states for `KILLED_BY_SWITCH` status.
```

### Step 2: Triage & Audit (2-15 minutes)
```
Evidence Collector:
1. Export the halted `WorkflowExecution` context.
2. Identify the specific node/agent that initiated the runaway behavior.
3. Quantify the blast radius (Tokens consumed, external APIs called, database records mutated).

Backend Architect:
1. Review the generated prompts and the inputs that led to the hallucination.
2. Inspect the Semantic Memory vector for poisoning or recursive context insertion.
```

### Step 3: Remediation & Reset (15-60 minutes)
```
Incident Response Commander:
1. Deactivate the Kill Switch once the root cause is mitigated:
   POST /kill-switch/deactivate { "tenant_id": "[ID]" }
2. If data was mutated, restore from the last known good state or reverse the specific transactions.
3. Reset the tenant's Pod state.

Developer Agent:
1. Implement guardrails (e.g., strict token limits, schema enforcement patches).
2. Update system prompts to prevent the edge-case.
```

### Step 4: Post-Mortem
1. Analyze the context logs leading to the runaway condition.
2. Implement preventative rate limits in `TaskValidator` or the Message Broker.
3. Publish findings to `docs/operations/`.
