# Agent Format & Architecture Evaluation

**Date:** May 26, 2026
**Topic:** Evaluating `agency-agents` format, `agents.md` standard, PRPM integration, and MCP for Skills.

## Executive Summary
The `agency-agents` repository provided the initial structural inspiration for AgencyOS agents (Markdown with YAML frontmatter) and remains top-tier due to its use of "few-shot prompting" (embedded code examples). However, to maximize the AgencyOS marketplace velocity and future-proof the platform, a **Hybrid Approach** leveraging the `agents.md` standard for Prompts and the **Model Context Protocol (MCP)** for Skills is recommended.

---

## Expert Panel Review

### 🧑‍🔬 Product Trend Researcher: "Agents vs. Skills"
There is a critical distinction in the AI meta between Agents and Skills:
*   **`agents.md` defines *WHO* the AI is:** It contains the persona, the rules, and the system prompt. It is the "Brain".
*   **Skills define *WHAT* the AI can do:** These are functional tools (e.g., database queries, web search). They are the "Hands".

Markdown (`agents.md`) is practically immortal. It represents the lowest-common-denominator for defining the "Brain".

### 🏗️ Backend Architect: "Separation of Concerns & MCP"
To prevent application bloat, we must rigidly separate the *Prompt* from the *Tools*.
*   **The Prompt Layer (`agents.md`):** Passed as the `system` message to any LLM.
*   **The Skills Layer (MCP):** Instead of adopting proprietary `skills.md` formats, we will use the open **Model Context Protocol (MCP)**. MCP acts like a universal USB port for AI capabilities. We build an MCP server once, and any LLM (Claude, GPT, Gemini) can use its tools without custom integration code.
*   **Mapping:** The `.md` file's frontmatter declares *which* skills are required (e.g., `required_skills: [github_mcp]`). The orchestrator binds these dynamically at runtime, ensuring strict RBAC (Role-Based Access Control).

### 👨‍💻 Senior Developer: "The Power of Few-Shot Prompting"
A review of the existing `agency-agents` templates (e.g., `macos-spatial-metal-engineer.md`) reveals why they are so effective: they include actual code blocks and architectural patterns directly in the prompt. This technique, known as **Few-Shot Prompting**, drastically reduces hallucinations.
The beauty of the `agents.md` standard is that it natively supports this. Because it is plain text, we keep all of these rich, code-heavy examples while maintaining a vendor-agnostic architecture. We do not lose the quality of `agency-agents` by standardizing.

### 👔 Product Manager: "Staying Lean & Marketplace Velocity"
We will not chase every new file extension or proprietary vendor format. By supporting open protocols (Markdown for Agents, MCP for Skills), AgencyOS remains lightweight and insulated from "LLM wars." The `agency-agents` templates will serve as our high-quality seed data, while our architecture evolves to support PRPM and standard `agents.md` ingestion for massive marketplace scalability.

---

## The Hybrid Architecture Recommendation

1.  **The Core Format:** Continue using Markdown (`.md`) files as the universal source of truth for agent personas, retaining all few-shot code examples.
2.  **Progressive Enhancement:** Allow YAML frontmatter to power AgencyOS UI features (colors, avatars) and explicitly declare required MCP skills.
3.  **Frictionless Fallback:** If an agent file lacks frontmatter (like a standard `agents.md` pulled from PRPM), AgencyOS automatically assigns default properties and executes the prompt.
4.  **Skills via MCP:** Do not adopt custom `skills.md` schemas. Use the Model Context Protocol to dynamically attach tools to the LLM session based on the agent's declared requirements.
