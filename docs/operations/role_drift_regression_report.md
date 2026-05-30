# Role Drift Regression Report: Terminal Command Execution

## Overview
An investigation was conducted into why specialized agents (such as `engineering-technical-writer` and `engineering-devops-engineer`) are inappropriately falling back to the default `Code` mode to execute terminal commands, rather than executing them within their own designated modes.

## Findings

### 1. Missing Tool Group Assignments in `.roomodes`
The `.roomodes` file defines the specific tool groups available to each custom mode. 
- The `engineering-technical-writer` mode (and several others like `design-visual-storyteller`, `support-legal-compliance-checker`) is strictly limited to the `["read", "edit"]` groups.
- **Impact:** Because these agents literally lack the `"command"` tool group, they are physically incapable of executing terminal commands (e.g., git commands, build scripts, moving files). When a task requires a command, they are forced to request a mode switch, defaulting to the well-known `Code` mode.

### 2. Missing Explicit Execution Mandates in `.clinerules` & Templates
While the `engineering-devops-engineer` *does* possess the `"command"` group in `.roomodes`, it still occasionally drifts back to `Code` mode. 
- **Impact:** The `config/agent_base.yaml` template defines capabilities (`task_execution`, `data_analysis`) but does not explicitly grant or reinforce the authority for specialized agents to execute terminal operations within their own domain. 
- Furthermore, `.clinerules` lacks a strict directive forbidding specialized agents with command capabilities from deferring to `Code` mode. Agents often associate "terminal commands" and "implementation" inherently with the default `Code` mode due to standard AI behavioral baselines.

### 3. Orchestrator and Routing Ambiguity
The `ROUTING FIRST MANDATE` in `.clinerules` instructs agents to use the `switch_mode` tool to route tasks. If a task involves "coding" or "terminal commands," specialized agents may incorrectly interpret this as a trigger to route the task to the default `Code` or `Senior Developer` mode, rather than utilizing their own granted tools.

## Recommendations
1. **Update `.roomodes`:** Add the `"command"` group to `engineering-technical-writer` and other relevant specialized agents that require terminal access for operational tasks (like git operations or moving files).
2. **Update `.clinerules`:** Add an explicit mandate (e.g., "MODE RETENTION MANDATE") stating that if an agent possesses the `"command"` or `"edit"` tool group, they MUST execute those actions within their current mode and are forbidden from falling back to `Code` mode.
3. **Refine `config/agent_base.yaml`:** Explicitly map tool capabilities in the base template so specialized agents are systemically aware of their authority to execute terminal commands without delegating.