<!-- Agent: product-manager -->
# Research: System-Enforced Guardrails

## 1. The Problem: "Lost in the Middle" Attention Failures
Large Language Models (LLMs), regardless of underlying provider, process instructions across a vast context window. When given complex, multi-faceted tasks (like analyzing architecture, synthesizing code, and applying strict formatting constraints), the LLM's attention mechanism heavily weights the primary generative task. Secondary constraints, such as mandatory comment headers or strict rule compliance found deep within the `.clinerules` system prompt, are frequently missed. This is a technical limitation of AI attention, not a setup failure.

## 2. The Solution: Shifting from "Prompt-Based" to "System-Enforced"
To guarantee 100% compliance without relying on AI memory or attention, we must shift from relying on the prompt to enforcing rules mathematically at the execution layer. 

### Recommended Architecture
1. **Git Pre-Commit Hooks (The Ultimate Gatekeeper):**
   A lightweight `pre-commit` hook (Bash or Python) that scans all staged files. It ignores strict formats (JSON, YAML, lockfiles). If it detects a missing `Agent: [Mode]` header, it rejects the commit. This halts forward progress and forces the AI/Human to correct the oversight before it enters the repository.
   
2. **Automated Validation Layers:**
   A script (e.g., `scripts/validation_layer.py`) that acts as a post-generation checker. After an AI agent modifies a file, this script scans the workspace for missing headers or violated directory rules and returns an explicit error to the agent, forcing self-correction before the task is marked "complete".

## 3. Impact on AgencyOS & Ecosystem
Adopting this inside the AgencyOS platform provides exponential benefits, specifically for Epic 7 (MCP Skills) and Epic 9 (Marketplace):
- **Marketplace Quality Control:** When users upload custom `agents.md` assets to the PRPM marketplace, an automated guardrail enforces that the required headers, IP attributions, and YAML frontmatter exist before publication.
- **Blast Radius Containment:** Autonomous multi-agent Pods within AgencyOS can be forced through a "pre-save hook" that runs security checks before writing code to a user's workspace.
- **SOC2 Compliance:** It ensures an irrefutable, system-enforced audit log of *which* agent modified *which* file.

## 4. Implementation Strategy for Current Build
1. Write the Git `pre-commit` hook script in `.githooks/pre-commit`.
2. Configure git to use this local directory: `git config core.hooksPath .githooks`.
3. Update `docs/operations/Standard_Project_Setup_Guide.md` (or create it if missing) to include this as a mandatory setup step for all future environments and kinetik-os downstream builds.

## 5. Real-World Context: Strict Role Routing

**Common Question:** *"Why do you keep using the roo code standard roles?"*

**Contextual Explanation:** The AgencyOS architecture explicitly mandates a strict multi-agent workflow via `.clinerules` and `.roomodes` (the **Routing First Mandate**). Rather than relying on a single, general-purpose AI, tasks are broken down and routed to specialized domain experts (e.g., UX Architect, Backend Architect, Evidence Collector). This guarantees that context is preserved and code quality is maintained across different architectural domains. When a user queries this behavior, the system enforces a routing rule to switch to a purely conversational "Ask" mode, acting as a behavioral guardrail against unintended file modifications during general inquiries.