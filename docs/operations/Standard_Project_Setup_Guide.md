# Standard Project Setup Guide

This guide establishes the highly-optimized baseline for initiating new projects within the AgencyOS ecosystem. It synthesizes learnings from the AgencyOS build and evaluates standalone engine capabilities to create a robust, reliable, and frictionless environment for AI-assisted engineering.

---

## 1. Container Environment Setup (`.devcontainer`)

To eliminate "works on my machine" friction and ensure AI agents operate within a stable, predictable baseline, all new projects MUST utilize a standardized DevContainer architecture.

### Core Configuration Requirements

* **Consistent Baseline:** Use a robust, predictable base image (e.g., standard Debian/Ubuntu with necessary Python/Node runtimes pre-installed).
* **AI Extension Pre-Installation:** The `devcontainer.json` must automatically install essential VSCode extensions, explicitly including the Roo Code extension (`rooveterinaryinc.roo-cline`). This ensures the AI environment is instantly available upon container spin-up.
* **Volume Mounts for AI Persistence:** 
  It is critical to mount the host's global storage into the container to prevent context loss across container rebuilds.
  ```json
  "mounts": [
    "source=${localEnv:HOME}/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline,target=/root/.vscode-server/data/Machine/globalStorage/rooveterinaryinc.roo-cline,type=bind,consistency=cached"
  ]
  ```
  *(Path adjustments may be required based on OS, but the pattern of mounting global state must be maintained).*

### Production Container Security

* **Unprivileged Execution:** Production containerization (e.g., `deployment/server.Dockerfile`) is configured to run as an unprivileged non-root user. This is a critical security measure to minimize potential attack surfaces and prevent container breakout vulnerabilities.

---

## 2. Core Config: `.roomodes` and `.clinerules`

The "rules of engagement" must be structurally enforced via project-local configuration files. These files act as the "AgencyOS Brain", immediately instantiating the required governance model.

### `.roomodes` (Role-Based Access Control)
* **Purpose:** Defines the specialized personas (e.g., `agents-orchestrator`, `frontend-developer`, `evidence-collector`) and strictly bounds their file-access capabilities.
* **The Orchestrator Isolation Mandate:** The `agents-orchestrator` mode MUST be strictly forbidden from executing file modifications or writing code. Its permitted tools are strictly limited to planning, task breakdown, `switch_mode`, and `new_task`. It exists to *delegate*, not to execute.

### `.clinerules` (Operational Mandates)
* **Purpose:** Acts as the constitutional law for the project.
* **The Rule Classification System:** To prevent the AI from indiscriminately halting progress for minor infractions, all rules must be classified:
  * **Terminal Rules:** System crash or security breach risk. Immediate halt. (e.g., executing unchecked code).
  * **Severe Rules:** Major architectural deviation. Halts current task, requires immediate correction before proceeding. (e.g., writing backend logic in frontend files).
  * **Standard Rules:** General best practices. Corrected during the next natural review cycle. (e.g., missing documentation).
  * **Advisory Rules:** Suggestions for optimization. Logged but does not interrupt flow.
* **Key Directives to Include:**
  * **Routing First Mandate:** The system must evaluate user intent and switch to the correct specialized agent mode before engaging.
  * **Documentation Routing Mandate:** Enforces strict categorization of documentation into `core/`, `technical/`, `operations/`, `qa/`, `research/`, and `archive/`.
  * **Epic Workflow & Handoff Protocol:** Enforces isolated git branching, comprehensive documentation updates, and formal commit/push handoffs for major features.
  * **Strict QA Gate:** No feature can merge to `main` without automated test proof and explicit sign-off from the QA agent.
  * **Human-in-the-Loop Validation:** Strategic pausing for human verification at critical phase gates.
  * **Persistent Memory Updates:** Mandatory updates to `.roo/memory/changelog.md` and `active_context.md` at major transitions.

---

## 3. AI Interaction Paradigm

A significant challenge in AI orchestration is the system's tendency to bypass heavy operational protocols in favor of conversational "helpful assistant" defaults. To counter this, the project setup adopts specific interaction patterns.

### The Recommended Paradigm: Explicit Prompting & Lazy Loading

Instead of passively hoping the AI reads a text rule to trigger a heavy setup (branch creation, scaffold generation), the system should utilize **Explicit Decision Gates** and **Progressive Execution**:

1. **Micro-Friction Decision Gates:** 
   When a user requests a new feature or team assembly, the Orchestrator should not immediately execute the heavy `Standard Kickoff Protocol`. Instead, it must utilize native tools (like `ask_followup_question`) to present explicit options:
   * `[Run Full Epic Handoff Protocol (Branching & Docs)]`
   * `[Quick Conversational Assistance]`
   * `[Generate Architecture Docs Only]`
   
2. **Progressive Execution:**
   Defer heavy lifting. The Orchestrator acknowledges the request, executes the immediate first step (e.g., switching to the primary specialist agent), and provides suggested follow-up actions. 

3. **Explicit Trigger Commands (Future Proofing):**
   Where possible, move toward explicit CLI-style commands (e.g., `/kickoff Epic_9`) to mechanically trigger procedural workflows, bypassing the LLM's conversational tendency entirely.

### Handling Autonomous Engine Capabilities
While tools like `AGENT-ZERO` emphasize an unconstrained, build-tools-on-the-fly approach, our setup relies on the structured registry of personas (`agency-agents`). The Orchestrator acts as the bridge—using strict personas for predictable domain expertise, but maintaining the flexibility to write dynamic validation scripts or sandboxed tools when predefined paths fall short.

---

## 4. Initialization Checklist

When starting a new project repository, ensure the following steps are completed:
1. [ ] Clone or copy the `agency-os-template` repository, which contains the fully hardened baseline (DevContainers, unprivileged Dockerfiles, and JIT rules).
2. [ ] Initialize the `.roo/memory/` directory with `active_context.md` and `changelog.md`.
3. [ ] **Enable Automated Validation Layer:** Ensure `.githooks/pre-commit` and `scripts/validate_agent_metadata.py` are executable to enforce SOC2 auditability and prevent malformed agent configurations.

---

## 5. AI Extension Tooling (Roo Code / Cline) Configuration

To maximize velocity while maintaining safety and operational control, the Roo Code extension must be configured specifically for containerized development.

### Auto-Approval Settings in a Containerized Environment

When operating strictly within an isolated DevContainer, the risk profile of AI actions is significantly reduced. This allows for more aggressive auto-approval settings to maintain high momentum during execution.

* **Safe Reads (Auto-Approve):**
  * `read_file`, `list_files`, `search_files`: MUST be fully auto-approved. These actions are non-destructive and essential for the AI to build context rapidly.
* **File Modifications (Contextual Approval):**
  * `edit`, `write_to_file`: Can be auto-approved if working within an easily rebuildable and source-controlled container environment. However, ensure strict `.roomodes` restrictions (e.g., file pattern constraints) are in place to prevent the AI from modifying core configuration or rules outside its purview.
* **Shell Commands (Require Approval or Sandboxed Auto-Approve):**
  * `execute_command`: General best practice is to **Require Approval** for shell execution to prevent unintended side effects (e.g., recursive deletions or runaway background processes).
  * *Exception for Full Isolation:* If the DevContainer is fully ephemeral, completely isolated from sensitive host mounts (other than the workspace and extension storage), and you are utilizing rigorous `git` commit handoffs, you may enable auto-approve for shell commands to achieve maximum velocity.

### Best Practices for `.rootasks` and `.roomodes`

* **`.rootasks` (Structured Task Execution):**
  * **Purpose:** Provides a persistent, markdown-based checklist of tasks for the Orchestrator and specialized agents to follow, ensuring complex, multi-step workflows are not lost in conversational context.
  * **Best Practice:** Maintain a modular `.rootasks` template in the project skeleton. When a new Epic or Sprint begins, the Orchestrator should dynamically update `.rootasks` with the specific, atomic steps required. Agents must systematically check off items (`[x]`) as they complete them.
  * **Task Archiving Protocol:** To prevent `.rootasks` from growing indefinitely and causing context bloat, implement a systematic archiving process. Once a major phase or epic is completed, the `.rootasks` file should be purged of completed tasks. These completed tasks must be moved to an archive file (e.g., `.roo/memory/task_archive.md`) before starting the next phase.
* **`.roomodes` (Customizing Agent Behavior):**
  * **Purpose:** Customizes the available modes and personas within the Roo Code extension, tailored to the specific project's needs.
  * **Best Practice:** Do not rely on default modes. Explicitly define specialized roles (e.g., `frontend-developer`, `database-architect`, `evidence-collector`) mapped to your team's structure.
  * **Just-In-Time (JIT) Dynamic Loading:** Bulk-loading `/agents` into `.roomodes` is strictly forbidden. The Orchestrator MUST dynamically inject a specific role into `.roomodes` only when needed for a specific task and clean it up ephemerally afterward.
  * **File Restrictions:** Utilize the file restriction capabilities within `.roomodes` heavily. For example, the `frontend-developer` mode should only be allowed to edit files matching `.*(js|jsx|ts|tsx|css|html)$`, preventing it from accidentally altering Python backend code or CI/CD pipelines.
* **Mandatory Agent File Headers:**
  * **Purpose:** Ensures accountability and traceablity of AI-generated code.
  * **Best Practice:** Every new file created or significantly modified by an agent must include a standardized header block at the top. This header must specify the creation date, the agent role responsible (e.g., `frontend-developer`), and a brief description of the file's purpose. This aids in auditing and understanding the provenance of the codebase.

---

## 6. QA Audit Findings & Sign-off

**Audit Date:** 2026-05-30
**Auditor:** Evidence Collector (QA)
**Status:** ✅ APPROVED WITH MINOR RECOMMENDATIONS

### Audit Summary
A comprehensive audit was performed comparing the draft `Standard_Project_Setup_Guide.md` against the retrospective learnings documented in `reusable_assets_and_learnings.md`. 

**Verified Strengths:**
1. **DevContainer Configuration:** The critical volume mounting of `globalStorage/rooveterinaryinc.roo-cline` for AI persistence across rebuilds is accurately captured.
2. **Auto-Approval Constraints:** The contextual approach to auto-approvals (differentiating between safe reads, contextual file writes, and restricted shell commands) provides a strong security posture.
3. **Orchestrator Isolation Mandate:** The rules explicitly forbidding the `agents-orchestrator` from executing file modifications are present and correctly align with resolving the "analysis paralysis" bottleneck.

**Minor Gaps & Recommended Tweaks:**
* **Intent Classification & Asynchronous Executions:** Section 3 (AI Interaction Paradigm) covers "Progressive Execution," but misses two key heuristic patterns outlined in the retrospective:
  1. *Intent Classification via Request Complexity:* Evaluating the length/complexity of prompts to determine whether to default to a simple conversational response or trigger the heavy Kickoff Protocol.
  2. *Asynchronous/Shadow Kickoff:* Triggering scaffolding in the background while maintaining immediate conversational velocity.
  *Recommendation:* Consider incorporating these heuristics into Section 3 as future UX optimizations.

**Sign-off:**
The guide successfully codifies the required constraints and isolation parameters. It is structurally sound and approved for immediate adoption across the AgencyOS ecosystem.

* **Roo Code Workspace Storage:**
  To maintain task history reliably both locally on the host machine and inside the Dev Container, the Custom Storage Path must be explicitly defined in both environments to avoid "unusable path" errors:
  1. **`.vscode/settings.json` (Local Host):** Set the `roo-cline.customStoragePath` to the **absolute path** of your host workspace (e.g., `"/Users/youruser/.../.roo-tasks"`).
  2. **`.devcontainer/devcontainer.json` (Container):** Use the `customizations.vscode.settings` block to override this with the absolute path *inside* the container (e.g., `"/workspaces/project-name/.roo-tasks"`).
