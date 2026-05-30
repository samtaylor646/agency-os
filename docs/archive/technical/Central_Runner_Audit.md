# Central Runner Audit Report

**File path:** `scripts/central_runner.py`
**Purpose:** Serves as the monolithic orchestration engine for the AgencyOS backend, handling Directed Acyclic Graph (DAG) construction, state management, dependency resolution, task execution, and agent/tool dispatching.

---

## 1. External Dependencies

### Standard Libraries
* `asyncio`, `collections`, `typing`, `sys`, `os`, `time`, `uuid`, `json`

### Third-Party Libraries
* `pydantic` (`BaseModel`, `Field`, `ValidationError`) - For input/output schema validation.
* `tenacity` (`retry`, `stop_after_attempt`, `wait_exponential`, `retry_if_exception_type`) - For handling exponential backoffs on transient failures.

### Internal System Modules
* `scripts.validation_layer`: Imports `TaskValidator` for pre-flight task checking.
* `server.context`: Imports `set_tenant_id` for multi-tenant context management.
* `server.database`: Imports `SessionLocal` for direct database session manipulation.
* `server.models`: Imports DB models (`AgentExecutionMetric`, `WorkflowExecution`).
* `server.schemas`: Imports data transfer schemas (`DAGNodeInput`, `DAGNodeOutput`).
* `server.services.message_broker`: Real-time pub/sub notifications for pipeline state changes.
* `server.services.semantic_search`: Inline dependency for context injection (RAG).
* `server.services.llm_runner`: Inline dependency for triggering the LLM generation.
* `server.services.sandbox`: Inline dependency for dispatching python code to a secure sandbox.
* `server.services.kill_switch`: Inline dependency to evaluate if the global execution switch was tripped.

---

## 2. Classes

### `TransientNodeError(Exception)`
* **Responsibility:** Custom exception to trigger the `tenacity` retry decorator. Signals that a failure is temporary (e.g., network timeout) and the task can be safely retried.

### `TerminalNodeError(Exception)`
* **Responsibility:** Custom exception indicating unrecoverable errors (e.g., strict schema validation failure, sandbox code crash). Aborts the node execution permanently.

### `DAGOrchestrator`
* **Responsibility:** The core engine of the workflow pipeline. Constructs the workflow graph, resolves dependencies, and manages state persistence and human-in-the-loop pauses.
* **Key Properties:**
    * `workflow_id`, `workflow_name`
    * `nodes`, `edges`, `incoming_edges`, `in_degree` (Graph structure variables)
    * `state`: A dictionary mapping node IDs to their current `DAGNodeOutput`.
* **Methods:**
    * `add_node(...)`: Registers a node, its assigned agent, task, required inputs, and approval flags.
    * `add_edge(...)`: Builds the directional dependencies between nodes.
    * `get_topological_sort()`: Determines execution order. Uses a queue-based topological sort to group nodes into parallel-executable "levels." Detects cyclic dependencies.
    * `load_state()`: Hydrates the workflow state from the database (`WorkflowExecution` model).
    * `_save_state(tenant_id, status)`: Persists the workflow's current completion status and node results to the database.
    * `execute_workflow(tenant_id)`: The main orchestration loop. 
        * Validates the graph for cycles.
        * Retrieves prior state to enable pipeline resumption.
        * Checks the `kill_switch` per level to halt processing immediately if necessary.
        * Filters out skipped, paused, or already completed nodes.
        * Gathers required inputs from parent node outputs for validation.
        * Executes the level of nodes concurrently via `asyncio.gather`.
        * Handles pipeline suspension for `PAUSED_AWAITING_APPROVAL` and `PAUSED_ERROR_ESCALATION` states.
        * Emits real-time state transitions through the `message_broker`.

---

## 3. Functions

### `execute_node_with_retry(node_id, agent_name, task, context_data, tenant_id)`
* **Responsibility:** Executes an individual agent task within a DAG node. Wrapped by a `@retry` decorator for transient faults. 
* **Execution Flow:**
    1. **Schema Validation:** Validates the input payload using `DAGNodeInput`.
    2. **Event Dispatch:** Emits a `node_start` event to the message broker.
    3. **Pre-flight Validation:** Checks the task against the `TaskValidator`.
    4. **Context Injection (RAG):** Connects to the database to retrieve semantic context (`semantic_search.search_documents`) matching the task, injecting it into `context_data`.
    5. **Dispatching:**
        * **If `agent_name == "CodeSandbox"`:** Extracts code and executes it securely using `sandbox_env`. 
        * **Otherwise:** Generates a response via the `llm_runner`.
    6. **Analytics Logging:** Persists duration, execution metrics, and mocked token usage to `AgentExecutionMetric`.
    7. **Completion Dispatch:** Emits `node_complete` or `node_failed` events via the message broker.
    8. **Return:** Formats and returns a `DAGNodeOutput`.

---

## 4. Assessment & Refactoring Insights (Tech Debt)

1. **Monolithic Design:** This single file orchestrates the workflow, queries databases, interfaces with LLMs, runs RAG, and manages websockets/brokers. It violates the Single Responsibility Principle (SRP).
2. **Inline Imports:** Services like `semantic_search`, `llm_runner`, `sandbox_env`, and `kill_switch` are imported locally inside functions, likely to avoid circular dependencies. This is a strong indicator of tight coupling and poor modularization.
3. **Database Contention:** Direct manipulation of `SessionLocal()` instances inside node execution (`AgentExecutionMetric`, `search_documents`) and orchestrator loops (`_save_state`) binds the orchestration logic directly to the database layer.
4. **Hardcoded Sandboxing Logic:** The `if agent_name == "CodeSandbox"` check inside the generic execution function means that adding new tools or execution environments requires editing the core runner logic.
