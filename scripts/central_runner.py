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
    from scripts.validation_layer import TaskValidator
except ImportError:
    TaskValidator = None

try:
    from server.context import set_tenant_id as set_tenant_context
    from server.database import SessionLocal
    from server.models import AgentExecutionMetric, WorkflowExecution
    from server.schemas import DAGNodeInput, DAGNodeOutput
    from server.services.message_broker import message_broker
except ImportError as e:
    print(f"Warning: Could not import server dependencies: {e}")
    set_tenant_context = None
    SessionLocal = None
    AgentExecutionMetric = None
    WorkflowExecution = None
    DAGNodeInput = None
    DAGNodeOutput = None
    message_broker = None

# A4-1: Implement standard Pydantic models for DAG node inputs and outputs
# Models imported from server.schemas: DAGNodeInput, DAGNodeOutput

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
async def execute_node_with_retry(node_id: str, agent_name: str, task: str, context_data: dict, tenant_id: str) -> DAGNodeOutput:
    # A4-2: Enforce strict schema validation
    try:
        validated_input = DAGNodeInput(task=task, context_data=context_data, tenant_id=tenant_id)
    except ValidationError as e:
        raise TerminalNodeError(f"Validation error for node {node_id}: {e}")

    print(f"[Tenant {validated_input.tenant_id}] Executing Node {node_id} with agent {agent_name}")
    start_time = time.time()
    error_msg = None
    status = "success"
    
    if message_broker:
        await message_broker.publish(str(validated_input.tenant_id), {
            "type": "node_start",
            "node_id": node_id,
            "agent_name": agent_name
        })
        
    if TaskValidator and set_tenant_context:
        set_tenant_context(validated_input.tenant_id)
        validator = TaskValidator()
        validator.pre_flight_check(validated_input.task)
        
    # Semantic Context Injection (RAG)
    try:
        from server.services.semantic_search import search_documents
        if SessionLocal:
            db_session = SessionLocal()
            try:
                rag_results = await search_documents(
                    db=db_session, 
                    workspace_id=int(validated_input.tenant_id), 
                    query=validated_input.task, 
                    top_k=3
                )
                
                if rag_results:
                    rag_context = "\n\n---\n\n".join([r['text_content'] for r in rag_results])
                    validated_input.context_data["Semantic_Knowledge"] = rag_context
            except Exception as e:
                print(f"RAG semantic search error: {e}")
            finally:
                db_session.close()
    except ImportError:
        pass

    try:
        # A2-1: Replace mock execute_node in central_runner.py with actual LLM/agent dispatch logic
        # Import LLM orchestration layer and pass the context.
        from server.services.llm_runner import llm_runner
        
        # Build context prompt from dependencies
        context_str = "\n".join([f"{k}: {json.dumps(v)}" for k, v in validated_input.context_data.items()])
        full_prompt = f"Task: {validated_input.task}\nContext:\n{context_str}"
        
        if agent_name == "CodeSandbox":
            # Offload untrusted code to the secure execution sandbox
            try:
                from server.services.sandbox import sandbox_env
                code_to_run = validated_input.task # Assume task contains the code directly or as part of JSON
                # Check if task is JSON that contains 'code'
                try:
                    task_data = json.loads(validated_input.task)
                    if isinstance(task_data, dict) and 'code' in task_data:
                        code_to_run = task_data['code']
                except json.JSONDecodeError:
                    pass
                    
                sandbox_result = sandbox_env.execute_script(code_to_run)
                response = f"Sandbox Output:\nStdout: {sandbox_result['stdout']}\nStderr: {sandbox_result['stderr']}\nExit Code: {sandbox_result['exit_code']}"
                if sandbox_result['exit_code'] != 0:
                    status = "failed"
                    error_msg = f"Sandbox execution failed with exit code {sandbox_result['exit_code']}"
            except Exception as sb_err:
                raise TerminalNodeError(f"Sandbox execution failed: {sb_err}")
        else:
            # Dispatch to LLM runner
            try:
                response = await llm_runner.generate_response(
                    prompt=full_prompt, 
                    system_prompt=f"You are acting as the specialized agent: {agent_name}."
                )
            except (TimeoutError, ConnectionError) as net_err:
                raise TransientNodeError(f"Network error during LLM generation: {net_err}")
        
        result = {"output": response, "context_keys": list(validated_input.context_data.keys())}
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
            
    if message_broker:
        if status == "success":
            await message_broker.publish(str(validated_input.tenant_id), {
                "type": "node_complete",
                "node_id": node_id,
                "result": result
            })
        else:
            await message_broker.publish(str(validated_input.tenant_id), {
                "type": "node_failed",
                "node_id": node_id,
                "error": error_msg
            })
            
    return DAGNodeOutput(node_id=node_id, status=status, result=result, error=error_msg)

class DAGOrchestrator:
    def __init__(self, workflow_name: str = "default_workflow"):
        self.workflow_name = workflow_name
        self.workflow_id = str(uuid.uuid4())
        self.nodes = {}  # node_id -> {"agent_name": str, "task": str, "required_inputs": list}
        self.edges = defaultdict(list)  # node_id -> list of dependent node_ids
        self.incoming_edges = defaultdict(list)  # node_id -> list of parent node_ids
        self.in_degree = defaultdict(int)
        self.state = {} # node_id -> DAGNodeOutput dict
    
    def add_node(self, node_id: str, agent_name: str, task: str, required_inputs: typing.List[str] = None, requires_human_approval: bool = False):
        self.nodes[node_id] = {"agent_name": agent_name, "task": task, "required_inputs": required_inputs or [], "requires_human_approval": requires_human_approval}
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

    def load_state(self):
        if not SessionLocal or not WorkflowExecution:
            return
            
        db = SessionLocal()
        try:
            exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.id == self.workflow_id).first()
            if exec_record and exec_record.execution_context:
                self.state = exec_record.execution_context
        except Exception as e:
            print(f"Failed to load workflow state: {e}")
        finally:
            db.close()

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

        self.load_state()
        self._save_state(tenant_id, "RUNNING")
        
        if message_broker and not self.state:
            await message_broker.publish(str(tenant_id), {
                "type": "workflow_start",
                "workflow_id": self.workflow_id,
                "workflow_name": self.workflow_name,
                "nodes": {k: {"agent_name": v["agent_name"], "task": v["task"]} for k, v in self.nodes.items()},
                "edges": dict(self.edges)
            })
            
        results = self.state.copy()
        has_failure = False
        
        try:
            from server.services.kill_switch import kill_switch
        except ImportError:
            kill_switch = None

        for level in levels:
            if kill_switch and kill_switch.is_active(tenant_id):
                final_status = "KILLED_BY_SWITCH"
                self._save_state(tenant_id, final_status)
                if message_broker:
                    await message_broker.publish(str(tenant_id), {
                        "type": "workflow_failed",
                        "workflow_id": self.workflow_id,
                        "error": "Workflow execution halted by LLM Kill Switch."
                    })
                return {"status": final_status, "results": results, "error": "Workflow execution halted by LLM Kill Switch."}

            tasks = []
            node_ids_in_tasks = []
            has_pause = False
            
            for node_id in level:
                node_status = self.state.get(node_id, {}).get("status")
                
                # If node is already successfully completed
                if node_status in ["success", "COMPLETED"]:
                    continue
                
                # If node is currently paused and awaiting intervention
                if node_status in ["PAUSED_AWAITING_APPROVAL", "PAUSED_ERROR_ESCALATION"]:
                    has_pause = True
                    continue
                
                # Check dependencies state
                skip_node = False
                for parent in self.incoming_edges.get(node_id, []):
                    parent_status = results.get(parent, {}).get("status")
                    if parent_status in ["failed", "skipped", "PAUSED_ERROR_ESCALATION", "PAUSED_AWAITING_APPROVAL"]:
                        skip_node = True
                        break
                        
                if skip_node:
                    results[node_id] = {"status": "skipped", "error": "Parent node failed, skipped, or paused"}
                    self.state[node_id] = results[node_id]
                    continue
                    
                node_info = self.nodes[node_id]
                
                context_data = {}
                for parent_node in self.incoming_edges.get(node_id, []):
                    parent_res = results.get(parent_node, {})
                    if "result" in parent_res:
                        context_data[parent_node] = parent_res["result"]
                
                if node_status == "INTERVENED":
                    intervened_context = self.state.get(node_id, {}).get("context_data", {})
                    if "HUMAN_INTERVENTION" in intervened_context:
                        context_data["HUMAN_INTERVENTION"] = intervened_context["HUMAN_INTERVENTION"]
                
                required_inputs = node_info.get("required_inputs", [])
                if required_inputs:
                    filtered_context = {}
                    for req in required_inputs:
                        for parent_res in context_data.values():
                            if isinstance(parent_res, dict) and req in parent_res:
                                filtered_context[req] = parent_res[req]
                    
                    missing_inputs = [req for req in required_inputs if req not in filtered_context]
                    if missing_inputs:
                        results[node_id] = {"status": "failed", "error": f"Schema validation failed. Missing required inputs: {missing_inputs}"}
                        self.state[node_id] = results[node_id]
                        has_failure = True
                        continue
                        
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
                node_ids_in_tasks.append(node_id)
            
            if tasks:
                level_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for node_id, result in zip(node_ids_in_tasks, level_results):
                    if isinstance(result, Exception):
                        # PAUSED_ERROR_ESCALATION
                        res_dict = {
                            "status": "PAUSED_ERROR_ESCALATION", 
                            "error": str(result),
                            "node_id": node_id
                        }
                        results[node_id] = res_dict
                        has_pause = True
                        
                        if message_broker:
                            asyncio.create_task(message_broker.publish(str(tenant_id), {
                                "type": "pipeline_paused",
                                "node_id": node_id,
                                "reason": "error_escalation",
                                "error": str(result)
                            }))
                            asyncio.create_task(message_broker.publish(str(tenant_id), {
                                "type": "error_escalation",
                                "node_id": node_id,
                                "error": str(result)
                            }))
                            
                    elif hasattr(result, 'dict'):
                        res_dict = result.dict()
                        if res_dict["status"] == "success" and self.nodes[node_id].get("requires_human_approval"):
                            res_dict["status"] = "PAUSED_AWAITING_APPROVAL"
                            has_pause = True
                            if message_broker:
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "pipeline_paused",
                                    "node_id": node_id,
                                    "reason": "awaiting_approval"
                                }))
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "awaiting_approval",
                                    "node_id": node_id,
                                    "result": res_dict.get("result")
                                }))
                        elif res_dict["status"] == "failed":
                            res_dict["status"] = "PAUSED_ERROR_ESCALATION"
                            has_pause = True
                            if message_broker:
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "pipeline_paused",
                                    "node_id": node_id,
                                    "reason": "error_escalation",
                                    "error": res_dict.get("error")
                                }))
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "error_escalation",
                                    "node_id": node_id,
                                    "error": res_dict.get("error")
                                }))
                        else:
                            if res_dict["status"] == "failed":
                                has_failure = True
                        
                        results[node_id] = res_dict
                        
                    self.state[node_id] = results[node_id]
                    
            if has_pause:
                self._save_state(tenant_id, "PAUSED")
                return {"status": "PAUSED", "results": results}
                
            self._save_state(tenant_id, "RUNNING")
                
        final_status = "PARTIAL_FAILURE" if has_failure else "COMPLETED"
        self._save_state(tenant_id, final_status)
        
        if message_broker:
            await message_broker.publish(str(tenant_id), {
                "type": "workflow_complete",
                "workflow_id": self.workflow_id,
                "status": final_status,
                "results": results
            })
            
        return {"status": final_status, "results": results}
