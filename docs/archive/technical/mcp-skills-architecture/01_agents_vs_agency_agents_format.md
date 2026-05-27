# Session 1: Evaluating agency-agents vs agents.md

**Status:** Research / Future Enhancement
**Topic:** Format of AgencyOS agents, PRPM integration, and Few-Shot Prompting.

## Overview
A cross-functional panel convened to discuss the structural format of AgencyOS agents, specifically comparing the current `agency-agents` format against the emerging `agents.md` standard and PRPM (`prpm.dev`).

## Panel Responses

### 🧑‍🔬 Product Trend Researcher
The `agency-agents` format (YAML frontmatter + Markdown system prompts) was a fantastic pioneering effort. However, the industry is rapidly consolidating around the `agents.md` standard. Ignoring package managers like PRPM (the `npm` for AI agents) means we have to build our entire marketplace supply from scratch, whereas adopting the standard allows us to tap into an ecosystem of 7,000+ packages.

### 🏗️ Backend Architect
If we adopt the `agents.md` philosophy, we shift to a more resilient, schema-less design. The backend simply reads the file and prepends it to the context window. We can still support frontmatter for AgencyOS-specific UI flourishes, but we shouldn't *require* it. 

### 👔 Product Manager
Requiring creators to learn a bespoke "AgencyOS Agent Format" introduces immense friction. Natively supporting the standard `agents.md` format allows users to seamlessly pull community agents into their workspace. 

### 👨‍💻 Senior Developer
Our current `agency-agents` templates (e.g., `macos-spatial-metal-engineer.md`) are top-tier because they use **Few-Shot Prompting**—including actual code blocks and architectural patterns directly in the prompt. The beauty of the `agents.md` standard is that it natively supports this because it is plain text. We keep all of these rich, code-heavy examples while maintaining a vendor-agnostic architecture.

### 🪃 Agents Orchestrator (Synthesis)
**The Hybrid Recommendation:**
1. **The Core Format:** Continue using Markdown files as the universal source of truth for agent personas.
2. **Progressive Enhancement:** Allow YAML frontmatter to power UI features.
3. **Frictionless Fallback:** If an agent file lacks frontmatter, automatically assign default properties and execute the prompt.
