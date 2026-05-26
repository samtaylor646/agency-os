# Context Optimization Runbook

## Overview
This runbook defines the procedures for auditing and optimizing the workspace's context files, system prompts, and memory management structures.

## Phase 1: Context Audit
**Objective:** Assess the current state of core configuration and rule files.

**Target Files:**
* `.clinerules`
* `.roomodes`
* `config/settings.md` (and related templates)

**Action Items:**
1. Read target files.
2. Identify conflicts between different rule definitions.
3. Assess verbosity and unnecessary information that consumes context window.
4. Document findings in `docs/operations/context_audit_findings.md`.

## Phase 2: Refinement & Consolidation (Future)
**Objective:** Apply optimizations based on Phase 1 findings.

**Action Items:**
1. Draft updated, concise rule files.
2. Consolidate overlapping instructions.
3. Validate changes with the team.
