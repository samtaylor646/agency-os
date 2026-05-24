import asyncio
from collections import defaultdict, deque
import typing
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from server.validation_layer import TaskValidator
    from server.context import set_tenant_context
    from server.database import SessionLocal
    from server.models import AgentExecutionMetric
except ImportError:
    TaskValidator = None
    set_tenant_context = None
    SessionLocal = None
    AgentExecutionMetric = None

# Mock execution function for nodes
async def execute_node(node_id: str, agent_name: str, task: str, context_data: dict, tenant_id: str):
    print(f"[Tenant {tenant_id}] Executing Node {node_id} with agent {agent_name}")
    start_time = time.time()
    error_msg = None
    status = "success"
    
    if TaskValidator and set_tenant_context:
        set_tenant_context(tenant_id)
        validator = TaskValidator()
        validator.pre_flight_check(task)
        
    try:
        await asyncio.sleep(0.1) # Simulate async work
        result = f"Output from {node_id} using {agent_name} for task: {task}"
    except Exception as e:
        status = "failed"
        error_msg = str(e)
        result = None

    execution_duration_ms = int((time.time() - start_time) * 1000)
    
    if SessionLocal and AgentExecutionMetric:
        db = SessionLocal()
        try:
            metric = AgentExecutionMetric(
                workspace_id=int(tenant_id),
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
            
    if status == "failed":
        raise RuntimeError(error_msg)
        
    return result

class DAGOrchestrator:
    def __init__(self):
        self.nodes = {}  # node_id -> {"agent_name": str, "task": str, "required_inputs": list}
        self.edges = defaultdict(list)  # node_id -> list of dependent node_ids
        self.incoming_edges = defaultdict(list)  # node_id -> list of parent node_ids
        self.in_degree = defaultdict(int)
    
    def add_node(self, node_id: str, agent_name: str, task: str, required_inputs: typing.List[str] = None):
        self.nodes[node_id] = {"agent_name": agent_name, "task": task, "required_inputs": required_inputs or []}
        if node_id not in self.in_degree:
            self.in_degree[node_id] = 0

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node].append(to_node)
        self.incoming_edges[to_node].append(from_node)
        self.in_degree[to_node] += 1
        
        # Ensure from_node is in in_degree even if it has 0 dependencies
        if from_node not in self.in_degree:
            self.in_degree[from_node] = 0

    def get_topological_sort(self) -> list:
        """Return lists of nodes grouped by execution level."""
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
            raise ValueError("Cycle detected in DAG. Cannot execute workflows with circular dependencies.")
            
        return levels

    async def execute_workflow(self, tenant_id: str):
        try:
            levels = self.get_topological_sort()
        except ValueError as e:
            return {"error": str(e)}

        results = {}
        for level in levels:
            tasks = []
            for node_id in level:
                node_info = self.nodes[node_id]
                
                context_data = {}
                for parent_node in self.incoming_edges.get(node_id, []):
                    if parent_node in results:
                        context_data[parent_node] = results[parent_node]
                
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
                    execute_node(
                        node_id=node_id,
                        agent_name=node_info["agent_name"],
                        task=node_info["task"],
                        context_data=context_data,
                        tenant_id=tenant_id
                    )
                )
            
            level_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for node_id, result in zip(level, level_results):
                if isinstance(result, Exception):
                    return {"error": f"Node {node_id} failed: {result}"}
                results[node_id] = result
                
        return results
