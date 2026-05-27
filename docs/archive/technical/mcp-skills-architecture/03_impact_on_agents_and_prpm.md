# Session 3: Impact on /agents and PRPM

**Status:** Research / Future Enhancement
**Topic:** How implementing Skills via MCP affects the existing `/agents` directory and enhances community-driven `agents.md` files.

## Overview
The panel detailed the practical workflow changes that occur when bringing MCP skills into the AgencyOS ecosystem.

## Panel Responses

### 🪃 Agents Orchestrator
Adding Skills turns text-generating "chatbots" into autonomous digital workers. An agent goes from advising on code to actually writing, compiling, and pushing it.

### 🏗️ Backend Architect
We do not have to rewrite the text of our existing Markdown files. We simply add a mapping layer in the frontmatter declaring necessary tools:
```yaml
name: macOS Spatial/Metal Engineer
required_mcp_skills:
  - filesystem_access
  - terminal_execute
```
When AgencyOS loads this agent, it reads that array and plugs the agent into those specific MCP servers. 

### 👔 Product Manager
When users download standard `agents.md` files from PRPM, those files are usually *just* text prompts. By having a robust Skills architecture, AgencyOS can prompt the user to equip these open-source personas with enterprise-grade capabilities (like AWS access or Git integration). The `agents.md` standard provides the *mind*, but AgencyOS provides the *body*.

### 👨‍💻 Senior Developer
**Concrete Example:** The `finance-tax-strategist.md`. Currently, it only gives general advice. If equipped with an `internet_search` skill and an `excel_reader` skill via MCP, it can parse actual user financial data from a `.xlsx` file and search for real-time 2026 tax codes, generating a customized, highly-actionable strategy.
