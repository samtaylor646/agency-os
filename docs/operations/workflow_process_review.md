# AgencyOS End-to-End Workflow & Task Resolution Protocol

## 1. Executive Summary
This document formalizes the complete agent execution lifecycle for the AgencyOS project, from initial task receipt to final handoff. It specifically highlights how the newly instituted **End of Task Sequence** integrates into the broader development pipeline to mitigate context loss, ensure quality control, and maintain pristine version control. To prevent ambiguity, all roles listed herein map strictly to the exact agent slugs defined in the system configurations and `/agents` directory.

## 2. The Full Agent Lifecycle Workflow
Every task, sprint, or epic managed by AgencyOS agents must strictly follow this five-phase lifecycle:

### Phase 1: Task Initiation & Routing
* **Intent Evaluation:** The **Agents Orchestrator (`agents-orchestrator`)** evaluates the user's request.
* **Specialist Assignment:** The **Agents Orchestrator (`agents-orchestrator`)** routes the task to the appropriate domain-specific agent (e.g., `backend-architect`, `product-manager`, `evidence-collector`) using the `switch_mode` tool.

### Phase 2: Guardrails & Environment Initialization
* **Validation:** The newly assigned specialist agent invokes `validation_layer.py` to ensure alignment with `settings.md`.
* **Branch Isolation:** If starting a new Epic or Feature, the agent must create and checkout a new Git branch to keep the `main` branch protected.

### Phase 3: Execution & Continuous Harvesting
* **Implementation:** The assigned agent executes the required code, design, or documentation updates.
* **Informal Human Spot-Checks:** Continuous human involvement begins here. The agent accommodates ad-hoc UI/UX or code spot-checks from the human operator during active build cycles.
* **Marketplace Seeding:** If a repeatable workflow or new agent role is discovered during execution, the agent proactively harvests and documents it in the `agents/` directory for the future AgencyOS Marketplace.

### Phase 4: The QA Gate
* **Automated & Manual Testing:** Code must be proven to work via documented automated tests.
* **Formal UAT Preparation (Instructions):** The responsible agent or the **Evidence Collector (`evidence-collector`)** MUST generate concise, step-by-step **Human Testing Instructions**. These must be simple, direct, and written so that *anyone* can easily execute the User Acceptance Testing (UAT).
* **Evidence Collection:** The **Evidence Collector (`evidence-collector`)** validates the automated tests and compiles the human testing instructions into a formal sign-off document before the task can proceed.

### Phase 5: The End of Task Mandate (Finalization)
*This is the mandatory concluding sequence triggered only after passing the QA Gate.*

1. **Handoff Documentation & Memory Updates**
   * Agents update `.roo/memory/changelog.md` and `.roo/memory/active_context.md`.
   * Newly generated documentation is correctly routed to `docs/core`, `docs/technical`, `docs/operations`, or `docs/qa`.
2. **Human-In-The-Loop (HITL) Verification (Formal UAT Starts & Ends)**
   * **Testing Starts:** The agent explicitly halts execution and presents the human operator with the **step-by-step Human Testing Instructions** generated in Phase 4. The human physically executes the test script against the system.
   * **Testing Ends:** The human operator provides explicit approval (or rejection) of the completed work. A successful approval definitively concludes the Human QA testing phase.
3. **Git Commit & Remote Push**
   * Following explicit human approval, the agent formally encapsulates all changes via a `git commit` on the isolated branch.
   * The commit is pushed to the remote repository (`git push`) to securely synchronize the completed task.

---

## 3. Deep Dive: Synthesized Team Feedback on Phase 5 (End of Task Mandate)

### 3.1 Product Manager (`product-manager`)
* **Feedback:** The Phase 5 sequence perfectly aligns with the requirement for strict feature traceability. By updating memory and documentation *before* the final push and requiring HITL, we ensure the product roadmap and active context remain perfectly synced with the physical codebase. 
* **Resolution:** Approved. This process guarantees that no feature is marked "done" without its corresponding operational and strategic footprint being fully realized.

### 3.2 Git Workflow Master (`git-workflow-master`)
* **Feedback:** Stressed the necessity of branch isolation and remote syncing. The `main` branch must remain pristine. Forcing a remote push at the very end of Phase 5 ensures no local work is lost and that feature branches contain the full narrative of the task before a Pull Request is opened.
* **Resolution:** Approved. The protocol mandates creating epic-specific branches in Phase 2, and encapsulating/pushing remotely at the end of Phase 5, reinforcing asynchronous collaboration safety.

### 3.3 Evidence Collector (`evidence-collector`)
* **Feedback:** QA mandates that the HITL step is useless without verifiable proof and actionable user steps. A human cannot accurately approve a phase gate without seeing the outcomes of Phase 4 and having a clear script to test the UI/backend.
* **Resolution:** Approved. The sequence mandates that Phase 4 yields explicit, concise **Human Testing Instructions**, ensuring the human operator has exactly what they need to effectively clear the Phase 5 HITL gate.

## 4. Conclusion
The comprehensive five-phase workflow, terminating with the **Docs/Memory -> HITL -> Git Master** sequence, is officially ratified as the Standard Operating Procedure (SOP) for AgencyOS. It must be explicitly tracked by agents using their internal TODO lists for every task.