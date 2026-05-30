
## Future Integrations & Architecture
*   **PRPM & `agents.md` Standard Integration:** Transition the agent ingestion engine to natively support the `agents.md` standard for cross-LLM compatibility. Implement a hybrid parsing strategy that uses YAML frontmatter for UI enhancement if present, but gracefully falls back to raw text execution for standard files. Evaluate PRPM (`prpm.dev`) as a backend package manager to populate the AgencyOS Marketplace with community agents. (See `docs/technical/agent_format_prpm_evaluation.md` for full analysis).

### Agent Upscaler & MCP Architecture (Phase 6 Completed / Scale)
*   **Comprehensive Architecture Hub:** A full, 7-part multi-disciplinary review covering Engineering, UX, Business Strategy, Security, and Legal compliance for adopting `agents.md`, PRPM integration, Model Context Protocol (MCP) skills, and the Automated Upscaler Pipeline. 
*   **Documentation Location:** See `docs/technical/mcp-skills-architecture/` for the complete roadmap, implementation plan, and business viability reports.

### Documentation Safeguards & Guardrails
*   **Documentation Safeguard Implementation:** Implement the proposed documentation safeguard plan (as drafted in `docs/operations/documentation_safeguard_plan.md`) into the core system guardrails. This involves integrating `.clinerules` checks or validation layers that strictly prevent incorrect file creation outside the routing mandate. **[REQUIRES HITL REVIEW]** A Human-in-the-Loop review is required to finalize the rules before implementation.

### Automated Validation Layer Enhancements
*   **Marketplace EULA Update (Legal & Compliance):** Explicitly state that automated validation checks do not constitute an IP warranty. Update Terms of Service/EULA documents accordingly to protect ecosystem liability.
*   **Kill Switch Integration (Incident Response):** Integrate `validation_layer.py` with the runtime Kill Switch (`server/services/kill_switch.py`) to automatically trip the kill switch and isolate agents if validation fails repeatedly.
