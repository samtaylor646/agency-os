# LLM Kill Switch Architecture

## 1. Overview
The LLM Kill Switch is a global and per-tenant halting mechanism designed to immediately stop autonomous DAG executions and N:N multi-agent Pods in AgencyOS (Epic 4.4.A). It serves as an emergency stop to contain "blast radiuses" if an autonomous agent or workflow behaves unexpectedly, consumes excess resources, or begins hallucinating rapidly.

## 2. Components

### 2.1. `KillSwitch` Service
Located at `server/services/kill_switch.py`. It provides a Redis-backed boolean flag system.
- `activate(tenant_id="GLOBAL")`: Sets a fast-access Redis key indicating the switch is active.
- `deactivate(tenant_id="GLOBAL")`: Removes the active flag.
- `is_active(tenant_id="GLOBAL")`: Quickly checks if the global or tenant-specific flag is present.

### 2.2. API Endpoints
Exposed in `server/api_server.py`:
- `POST /kill-switch/activate`
- `POST /kill-switch/deactivate`
- `GET /kill-switch/status`

### 2.3. DAG Orchestrator Integration
The `DAGOrchestrator` in `scripts/central_runner.py` polls `kill_switch.is_active(tenant_id)` at the start of every topological level execution. 
- If activated, the workflow immediately halts.
- Status is updated to `KILLED_BY_SWITCH`.
- Prevents subsequent nodes from receiving execution commands.

## 3. Blast Radius Containment
- **Tenant Isolation**: The Kill Switch supports tenant-level granularity. A runaway DAG in Workspace A can be killed without affecting Workspace B.
- **Global Halting**: In a P0 scenario (e.g., API provider compromised, global DB saturation), the `GLOBAL` tenant ID stops all workflows system-wide.
- **Immediate State Preservation**: The DAG halts at the current level, saving the intermediate context to `WorkflowExecution` to allow post-incident analysis.
