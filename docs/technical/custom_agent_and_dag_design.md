# Custom Agent Creator Wizard & Task Queue DAG Logic Design

## 1. Custom Agent Creator Wizard

### 1.1 UI Flow (`client/src/CustomAgentCreator.jsx`)
A multi-step wizard component:
1.  **Step 1: Identity:** Name, Role, Goal, Backstory.
2.  **Step 2: Configuration:** Select Base Model (e.g., GPT-4, Claude), Domain (e.g., specialized, marketing, finance).
3.  **Step 3: Capabilities & Guardrails:** Select Tools (from available system tools like `bash`, `file_read`, etc.), define specific instructions and guardrails.
4.  **Step 4: Review & Generate:** Displays a preview of the generated YAML frontmatter and Markdown content. User clicks "Create Agent".

### 1.2 Data Models (`server/models.py`)
Enhance the existing `CustomAgent` model (defined in `custom_agents_and_ingestion_architecture.md`) if needed.
```python
class CustomAgent(Base):
    __tablename__ = "custom_agents"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    domain = Column(String, nullable=False, default="specialized")
    filepath = Column(String, unique=True, nullable=False) # Path in /agents/{domain}/
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 1.3 API Endpoints (`server/routers/agents.py` or similar)
- `POST /api/v1/agents`:
    - **Request:** JSON payload with `name`, `role`, `goal`, `backstory`, `domain`, `capabilities`, `tools`, `instructions`.
    - **Logic:**
        1. Validates inputs.
        2. Generates Markdown string with YAML frontmatter.
        3. Saves file to `/agents/{domain}/{sanitized_name}.md`.
        4. Saves metadata to `custom_agents` table.
    - **Response:** Agent ID, filepath, success status.

## 2. Task Queue Translation DAG Logic

### 2.1 Concept
Translate the outputs from the Document Ingestion Pipeline (the Epics and Tasks) into an executable Directed Acyclic Graph (DAG) for the NEXUS Pipeline (`central_runner.py`).

### 2.2 Data Models (`server/models.py`)
Ensure tasks have dependency tracking.
```python
class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=generate_uuid)
    epic_id = Column(String, ForeignKey("epics.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    assigned_agent = Column(String) # E.g., 'product-manager'
    status = Column(String, default="pending") # pending, running, completed, failed
    dependencies = Column(JSON) # List of task IDs that must complete before this one
    output = Column(Text) # Store results for dependent tasks
```

### 2.3 DAG Engine (`scripts/orchestrator/dag_manager.py`)
- **Initialization:** Reads tasks for an Epic. Constructs a graph using a dictionary adjacency list.
- **Topological Sort:**
    ```python
    def get_execution_order(tasks: list[Task]) -> list[list[Task]]:
        # Returns a list of 'stages'. Tasks in the same stage can run in parallel.
        # Implements standard Kahn's algorithm or DFS topological sort.
        pass
    ```
- **Execution (`central_runner.py`):**
    1. Fetch `pending` tasks for the active Epic.
    2. Build DAG and determine executable tasks (those with no incomplete dependencies).
    3. Dispatch executable tasks to their `assigned_agent` via `asyncio.gather`.
    4. Upon completion, update task `status` to `completed`, save `output`, and trigger the next stage in the DAG.
    5. Pass `output` of completed dependencies into the context of downstream tasks.

### 2.4 State Management
- Use `ExecutionState` object (as mentioned in `nexus_pipeline_architecture.md`) to aggregate outputs.
- Database acts as the persistent state store. If the runner crashes, it can resume by querying `pending` tasks whose `dependencies` are all `completed`.