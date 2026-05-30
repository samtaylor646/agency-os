import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
from server.services.orchestrator_service import TransientNodeError, TerminalNodeError
import sys
import os

try:
    from server.database import SessionLocal
except ImportError:
    SessionLocal = None

class ExecutionResult(BaseModel):
    """Represents the result of a task execution."""
    task_id: str
    success: bool
    output: Any
    error_details: Optional[str] = None
    execution_time_ms: int = 0
    context_keys: list = []

class ExecutionEngineBase(ABC):
    """Abstract base class for the core execution engine."""

    @abstractmethod
    async def start_task(self, task_id: str, context: Dict[str, Any]) -> bool:
        """Initialize and start a task execution."""
        pass

    @abstractmethod
    async def execute_step(self, task_id: str, step_data: Dict[str, Any]) -> ExecutionResult:
        """Execute a specific step or unit of work within a task."""
        pass

    @abstractmethod
    async def stop_task(self, task_id: str, reason: str = "User requested") -> bool:
        """Halt an ongoing task execution."""
        pass

class DefaultExecutionEngine(ExecutionEngineBase):
    async def start_task(self, task_id: str, context: Dict[str, Any]) -> bool:
        return True

    async def execute_step(self, task_id: str, step_data: Dict[str, Any]) -> ExecutionResult:
        task = step_data.get("task", "")
        context_data = step_data.get("context_data", {})
        tenant_id = step_data.get("tenant_id", "1")
        execution_type = step_data.get("execution_type", "llm")
        agent_name = step_data.get("agent_name", "default")
        
        # Semantic Context Injection (RAG)
        try:
            from server.services.semantic_search import search_documents
            if SessionLocal:
                db_session = SessionLocal()
                try:
                    rag_results = await search_documents(
                        db=db_session, 
                        workspace_id=int(tenant_id), 
                        query=task, 
                        top_k=3
                    )
                    
                    if rag_results:
                        rag_context = "\n\n---\n\n".join([r['text_content'] for r in rag_results])
                        context_data["Semantic_Knowledge"] = rag_context
                except Exception as e:
                    print(f"RAG semantic search error: {e}")
                finally:
                    db_session.close()
        except ImportError:
            pass

        try:
            from server.services.llm_runner import llm_runner
            
            # Build context prompt from dependencies
            context_str = "\n".join([f"{k}: {json.dumps(v)}" for k, v in context_data.items()])
            full_prompt = f"Task: {task}\nContext:\n{context_str}"
            
            error_msg = None
            status = "success"
            
            if execution_type == "sandbox":
                # Offload untrusted code to the secure execution sandbox
                try:
                    from server.services.sandbox import sandbox_env
                    code_to_run = task
                    try:
                        task_data = json.loads(task)
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
            
            return ExecutionResult(
                task_id=task_id,
                success=(status == "success"),
                output=response,
                error_details=error_msg,
                context_keys=list(context_data.keys())
            )
            
        except TransientNodeError as e:
            raise e
        except Exception as e:
            raise TerminalNodeError(f"Node execution failed permanently: {e}")

    async def stop_task(self, task_id: str, reason: str = "User requested") -> bool:
        return True
