# NEXUS Pipeline Architecture

This document details the architectural design for the NEXUS Pipeline (Epic 2: Core Multi-Agent Orchestration). The NEXUS Pipeline acts as the central orchestration engine for routing tasks, managing context, and parsing agent definitions within AgencyOS.

## 1. Multi-Tenant Context Inheritance (`X-Tenant-ID`)

Building on the security foundations of Epic 1, the NEXUS Pipeline must rigorously isolate operations per tenant.

### Architecture
- **Context Extraction:** The FastAPI dependency injection layer extracts the `X-Tenant-ID` header from incoming HTTP requests.
- **Context Propagation:** We will utilize Python's `contextvars` to store the tenant context at the request boundary. This ensures that the tenant ID is automatically accessible to any asynchronous function executing within that request's thread/task, eliminating the need to pass `tenant_id` explicitly through every function signature.
- **Orchestrator Inheritance:** When `orchestrator_service.py` initializes an `AgentRunner` or creates a DAG task, it attaches the tenant context. 
- **Validation Layer Checks:** Before any task is routed to an agent, `validation_layer.py` retrieves the `X-Tenant-ID` from `contextvars` and ensures the requested resources (files, database rows, integrations) belong to the active tenant.

## 2. Markdown Parser for Agent Templates

Agents are defined declaratively in the `agents/` directory using Markdown (`.md`) files. The NEXUS pipeline requires a parser to dynamically convert these Markdown files into executable Agent personas.

### Implementation Strategy
- **Parser Library:** We will implement a custom parsing utility utilizing `python-frontmatter` (to handle YAML frontmatter for metadata) and Python's standard `re` (regex) or a library like `markdown-it-py` to parse sections based on headings.
- **Structure Mapping:**
  - **Frontmatter:** Contains configuration like `name`, `role`, `domain`, and `version`.
  - **Headings:** Specific level-2 (`##`) headings will be mapped to core agent components:
    - `## System Prompt` -> Maps to the core system instructions.
    - `## Capabilities` -> Maps to allowed tool bindings.
    - `## Guardrails` -> Maps to specific behavioral constraints passed to the validation layer.
- **Caching:** Parsing files on every request is inefficient. The orchestrator will parse these templates at startup or upon detecting file changes, caching the parsed representations in memory.

## 3. Directed Acyclic Graph (DAG) for Task Routing

Complex workflows require coordinated efforts from multiple specialized agents. To accomplish this, NEXUS uses a Directed Acyclic Graph (DAG) to map out task execution paths.

### Structure
- **Nodes (Vertices):** Represent a specific task unit assigned to a specific agent (e.g., Node A: User Journey Mapping by `product-manager`).
- **Edges (Directed Links):** Represent dependencies and data flow. A directed edge from Node A to Node B means Node B cannot start until Node A is complete, and Node B receives Node A's output as context.

### Implementation Strategy
- **DAG Engine:** We will implement a lightweight DAG manager leveraging `task_router.py` and `orchestrator_service.py` under the `server/services` module. NetworkX can be considered if graph complexity grows, but a custom dictionary-based adjacency list is sufficient for MVP.
- **Execution Flow:**
  1. **Planning Phase:** The `Agents Orchestrator` (the planner) receives a prompt and generates a workflow manifest defining the necessary nodes and edges.
  2. **Topological Sort:** The DAG engine performs a topological sort to establish a valid execution sequence.
  3. **Parallel Execution:** Nodes that share no dependencies (independent parallel branches) are executed concurrently using Python's `asyncio.gather`.
  4. **State Management:** As nodes complete, their outputs are appended to an `ExecutionState` object, which is passed down to dependent nodes, maintaining continuous context.

## Summary

The NEXUS pipeline relies on robust async context management for security (`X-Tenant-ID`), leverages a flexible Markdown parsing system for agent definitions, and utilizes a structured DAG to coordinate multi-agent workflows efficiently.
