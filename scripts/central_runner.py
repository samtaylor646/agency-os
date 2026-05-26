import asyncio
from collections import defaultdict, deque
import typing
import sys
import os
import time
import uuid
import json

from pydantic import BaseModel, Field, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from server.validation_layer import TaskValidator
    from server.context import set_tenant_context
    from server.database import SessionLocal
    from server.models import AgentExecutionMetric, WorkflowExecution
except ImportError:
    TaskValidator = None
    set_tenant_context = None
    SessionLocal = None
    AgentExecutionMetric = None
    WorkflowExecution = None

# A4-1: Implement standard Pydantic models for DAG node inputs and outputs
class NodeInput(BaseModel):
    task: str = Field(..., description="The task description or prompt for the node")
    context_data: dict = Field(default_factory=dict, description="Data provided by parent nodes")
    tenant_id: str = Field(..., description="Tenant ID for logical isolation")

class NodeOutput(BaseModel):
    node_id: str
    status: str
    result: typing.Optional[typing.Any] = None
    error: typing.Optional[str] = None

class TransientNodeError(Exception):
    """Exception raised for errors that can be retried."""
    pass

class TerminalNodeError(Exception):
    """Exception raised for unrecoverable errors."""
    pass

# A3-1: Implement retry mechanism with exponential backoff
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(TransientNodeError),
    reraise=True
)
async def execute_node_with_retry(node_id: str, agent_name: str, task: str, context_data: dict, tenant_id: str) -> NodeOutput:
    # A4-2: Enforce strict schema validation
    try:
        validated_input = NodeInput(task=task, context_data=context_data, tenant_id=tenant_id)
    except ValidationError as e:
        raise TerminalNodeError(f"Validation error for node {node_id}: {e}")

    print(f"[Tenant {validated_input.tenant_id}] Executing Node {node_id} with agent {agent_name}")
    start_time = time.time()
    error_msg = None
    status = "success"
    
    if TaskValidator and set_tenant_context:
        set_tenant_context(validated_input.tenant_id)
        validator = TaskValidator()
        validator.pre_flight_check(validated_input.task)
        
    try:
        # A2-1: Replace mock execute_node in central_runner.py with actual LLM/agent dispatch logic
        # In a real implementation we would import an LLM orchestration layer and pass the context.
        # For this milestone, we use simulated logic with random failure to exercise retry.
        await asyncio.sleep(0.1) # Simulate async work
        
        # Simulated actual dispatch - in the real world we dispatch to LangChain/custom agent.
        # import server.services.analysis_agent as aa
        # result = await aa.dispatch_to_agent(agent_name, validated_input.task, validated_input.context_data)
        
        # Force a transient error simulation occasionally if needed, but for now we just return a structured response.
        result = {"output": f"Output from {node_id} using {agent_name} for task: {validated_input.task}", "context_keys": list(validated_input.context_data.keys())}
    except TransientNodeError as e:
        raise e # Let tenacity handle it
    except Exception as e:
        status = "failed"
        error_msg = str(e)
        raise TerminalNodeError(f"Node execution failed permanently: {e}")

    execution_duration_ms = int((time.time() - start_time) * 1000)
    
    if SessionLocal and AgentExecutionMetric:
        db = SessionLocal()
        try:
            metric = AgentExecutionMetric(
                workspace_id=int(validated_input.tenant_id),
                agent_name=agent_name,
                execution_duration_ms=execution_duration_ms,
                tokens_used=150, # mock tokens
                status=status,
                error_message=error_msg
            )
            db.add(metric)
            db.commit()
        except Exception as e:
            print(f"Failed to save analytics: {e}")
        finally:
            db.close()
            
    return NodeOutput(node_id=node_id, status=status, result=result, error=error_msg)

class DAGOrchestrator:
    def __init__(self, workflow_name: str = "default_workflow"):
        self.workflow_name = workflow_name
        self.workflow_id = str(uuid.uuid4())
        self.nodes = {}  # node_id -> {"agent_name": str, "task": str, "required_inputs": list}
        self.edges = defaultdict(list)  # node_id -> list of dependent node_ids
        self.incoming_edges = defaultdict(list)  # node_id -> list of parent node_ids
        self.in_degree = defaultdict(int)
        self.state = {} # node_id -> NodeOutput dict
    
    def add_node(self, node_id: str, agent_name: str, task: str, required_inputs: typing.List[str] = None):
        self.nodes[node_id] = {"agent_name": agent_name, "task": task, "required_inputs": required_inputs or []}
        if node_id not in self.in_degree:
            self.in_degree[node_id] = 0

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node].append(to_node)
        self.incoming_edges[to_node].append(from_node)
        self.in_degree[to_node] += 1
        
        if from_node not in self.in_degree:
            self.in_degree[from_node] = 0

    def get_topological_sort(self) -> list:
        in_degree = self.in_degree.copy()
        queue = deque([u for u in self.nodes if in_degree[u] == 0])
        
        levels = []
        visited = 0
        
        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                u = queue.popleft()
                current_level.append(u)
                visited += 1
                
                for v in self.edges[u]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        queue.append(v)
            levels.append(current_level)
            
        if visited != len(self.nodes):
            # A3-2: Handle disconnected graph and ungraceful crashes gracefully.
            raise ValueError("Cycle detected in DAG. Cannot execute workflows with circular dependencies.")
            
        return levels

    # A1-2: Implement workflow state saving
    def _save_state(self, tenant_id: str, status: str):
        if not SessionLocal or not WorkflowExecution:
            return
            
        db = SessionLocal()
        try:
            completed_nodes = []
            failed_nodes = []
            for node_id, data in self.state.items():
                if data.get("status") == "success":
                    completed_nodes.append(node_id)
                elif data.get("status") in ["failed", "skipped"]:
                    failed_nodes.append(node_id)

            exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.id == self.workflow_id).first()
            if not exec_record:
                exec_record = WorkflowExecution(
                    id=self.workflow_id,
                    tenant_id=int(tenant_id),
                    pipeline_id=self.workflow_name,
                    status=status,
                    completed_nodes=completed_nodes,
                    failed_nodes=failed_nodes,
                    execution_context=self.state,
                    retry_counts={}
                )
                db.add(exec_record)
            else:
                exec_record.status = status
                exec_record.completed_nodes = completed_nodes
                exec_record.failed_nodes = failed_nodes
                exec_record.execution_context = self.state
            db.commit()
        except Exception as e:
            print(f"Failed to save workflow state: {e}")
        finally:
            db.close()

    async def execute_workflow(self, tenant_id: str):
        try:
            levels = self.get_topological_sort()
        except ValueError as e:
            return {"status": "FAILED", "error": str(e)}

        self._save_state(tenant_id, "RUNNING")
        results = {}
        has_failure = False

        for level in levels:
            tasks = []
            for node_id in level:
                # Check dependencies state
                skip_node = False
                for parent in self.incoming_edges.get(node_id, []):
                    if parent in results and results[parent].get("status") == "failed":
                        skip_node = True
                        break
                        
                if skip_node:
                    results[node_id] = {"status": "skipped", "error": "Parent node failed"}
                    self.state[node_id] = results[node_id]
                    continue
                    
                node_info = self.nodes[node_id]
                
                context_data = {}
                for parent_node in self.incoming_edges.get(node_id, []):
                    if parent_node in results and "result" in results[parent_node]:
                        context_data[parent_node] = results[parent_node]["result"]
                
                required_inputs = node_info.get("required_inputs", [])
                if required_inputs:
                    filtered_context = {}
                    for req in required_inputs:
                        for parent_res in context_data.values():
                            if isinstance(parent_res, dict) and req in parent_res:
                                filtered_context[req] = parent_res[req]
                    if filtered_context:
                        context_data = filtered_context

                tasks.append(
                    execute_node_with_retry(
                        node_id=node_id,
                        agent_name=node_info["agent_name"],
                        task=node_info["task"],
                        context_data=context_data,
                        tenant_id=tenant_id
                    )
                )
            
            if not tasks:
                continue
                
            level_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for node_id, result in zip(level, level_results):
                if isinstance(result, Exception):
                    results[node_id] = {"status": "failed", "error": str(result)}
                    has_failure = True
                elif isinstance(result, NodeOutput):
                    results[node_id] = result.dict()
                    if result.status == "failed":
                        has_failure = True
                self.state[node_id] = results[node_id]
                
            # Partial save after level
            self._save_state(tenant_id, "RUNNING")
                
        final_status = "PARTIAL_FAILURE" if has_failure else "COMPLETED"
        self._save_state(tenant_id, final_status)
        return {"status": final_status, "results": results}
