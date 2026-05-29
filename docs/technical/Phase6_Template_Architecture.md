# Phase 6: Template Architecture & API Selector

## 1. Overview
This document outlines the architectural specifications for Phase 6: Template Library & API Selector. It details the database schema changes for Templates, the Provider Routing Layer for multiple LLMs, and the Workflow State Rollback mechanisms.

## 2. Database Schema: Templates
To store full DAG configurations, agents, and prompts as reusable templates, we will introduce a robust schema.

### 2.1. `Template` Model
```python
class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True) # Null if system template
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    dag_configuration = Column(JSON, nullable=False) # Serialized DAG matrix, node definitions, and routing
    agent_definitions = Column(JSON, nullable=False) # Embedded custom agents/prompts
    required_api_capabilities = Column(JSON, default=list) # e.g., ["vision", "tools"]
    complexity_rating = Column(Integer, default=1)
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Key Considerations:**
- The `dag_configuration` will store a JSON representation of the `central_runner` matrix.
- `agent_definitions` allows the template to encapsulate specific prompts without relying on external DB rows that could be mutated, ensuring idempotency.
- The UI will list templates where `is_system == True` alongside user-created templates (`workspace_id == current_workspace`).

## 3. Provider Routing Layer (API Selector)
We need a dynamic routing layer to support OpenAI, Anthropic, and Gemini.

### 3.1. `llm_runner.py` Architecture
The `llm_runner.py` will act as a unified interface (facade) leveraging a Strategy pattern.

```python
class LLMProviderStrategy(ABC):
    @abstractmethod
    async def generate_response(self, messages, credentials, model, **kwargs):
        pass

class OpenAIStrategy(LLMProviderStrategy): ...
class AnthropicStrategy(LLMProviderStrategy): ...
class GeminiStrategy(LLMProviderStrategy): ...

class LLMRunner:
    def __init__(self):
        self.strategies = {
            "openai": OpenAIStrategy(),
            "anthropic": AnthropicStrategy(),
            "gemini": GeminiStrategy()
        }

    async def execute(self, provider: str, messages: list, credentials: dict, model: str, **kwargs):
        strategy = self.strategies.get(provider.lower())
        if not strategy:
            raise ValueError(f"Unsupported provider: {provider}")
        
        try:
            return await strategy.generate_response(messages, credentials, model, **kwargs)
        except Exception as e:
            # Implement Fallback logic here if configured
            return await self.handle_fallback(...)
```

### 3.2. `api_server.py` Updates
- `api_server.py` routes handling Agent Execution and Template Instantiation must dynamically pull `LLM_PROVIDER` and `LLM_MODEL` from the agent configuration or workspace defaults.
- The `CredentialsManager` (frontend) maps to the `Credential` table, which will map providers (`openai`, `anthropic`, `google`) to encrypted keys. `api_server.py` decrypts these just-in-time and passes them to `llm_runner.py`.

## 4. Workflow State Rollbacks
Rollbacks allow users to revert a pipeline execution to a previously completed node, clearing downstream context and restarting.

### 4.1. `state_manager.py` Updates
The `StateManager` must support a `rollback_to_node(pipeline_id, target_node_id)` operation.

- **Mechanism:**
  1. Retrieve the execution graph (DAG).
  2. Identify all nodes downstream of `target_node_id`.
  3. Purge or mark as "rolled_back" the outputs/context of all downstream nodes from the state matrix.
  4. Reset the state of `target_node_id` and downstream nodes to `PENDING` (or re-queue the target node).
  5. Emit a websocket event `ROLLBACK_COMPLETED` with the updated state matrix.

### 4.2. `central_runner.py` Integration
When a rollback is requested:
1. `central_runner.py` pauses current execution loops (if active).
2. It delegates to `StateManager.rollback_to_node()`.
3. It rebuilds its in-memory queue based on the newly reset state matrix.
4. Execution resumes starting from `target_node_id`.

```python
# Pseudo-code in central_runner.py
async def handle_rollback_request(self, pipeline_id: str, node_id: str):
    await self.pause_pipeline(pipeline_id)
    new_state = await self.state_manager.rollback_to_node(pipeline_id, node_id)
    await self.rebuild_execution_queue(new_state)
    await self.resume_pipeline(pipeline_id)
```

## 5. Summary
These architectural changes ensure robust template serialization, a flexible and extensible LLM provider strategy, and resilient state management with human-in-the-loop rollback capabilities.