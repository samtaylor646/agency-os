# Session 2: Skills, MCP, and Future-Proofing

**Status:** Research / Future Enhancement
**Topic:** How to handle agent capabilities (skills) without bloating the application, and standardizing via Model Context Protocol (MCP).

## Overview
The panel discussed the distinction between an agent's persona and its capabilities, and how to future-proof AgencyOS against the rapidly changing LLM landscape.

## Panel Responses

### 🧑‍🔬 Product Trend Researcher
`agents.md` and `skills.md` serve fundamentally different purposes:
*   **`agents.md` defines *WHO* the AI is:** It contains the persona, the rules, and the system prompt. It is the "Brain".
*   **Skills define *WHAT* the AI can do:** These are functional tools (e.g., database queries, web search). They are the "Hands".

### 🏗️ Backend Architect
To prevent application bloat, we must rigidly separate the *Prompt* from the *Tools*.
Instead of adopting proprietary `skills.md` formats, we will use the open **Model Context Protocol (MCP)**. MCP acts like a universal USB port for AI capabilities. We build an MCP server once, and any LLM (Claude, GPT, Gemini) can use its tools without custom integration code.

### 👔 Product Manager
We will not chase every new file extension. By supporting open protocols (Markdown for Agents, MCP for Skills), AgencyOS remains lightweight, maintainable, and completely insulated from the "LLM wars" happening between Google, OpenAI, and Anthropic.

### 🪃 Agents Orchestrator (Synthesis)
1. **For Agents:** Treat `.md` (Markdown) as the universal source of truth.
2. **For Skills/Tools:** Use the Model Context Protocol (MCP) to dynamically attach tools to the LLM session.
3. **For Multi-LLM:** Rely on the internal router to pick the best model for the job, feeding it the same standard Markdown and MCP tools.
