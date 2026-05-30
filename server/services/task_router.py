from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class RouteDestination(BaseModel):
    """Represents the target destination for a routed task."""
    agent_id: str
    queue_name: str
    priority: int = 0
    execution_type: str = "llm"  # "llm" or "sandbox"

class TaskRouterBase(ABC):
    """Abstract base class for task routing."""

    @abstractmethod
    async def evaluate_task(self, task_definition: Dict[str, Any]) -> RouteDestination:
        """Determine the optimal destination for a given task."""
        pass

    @abstractmethod
    async def route_task(self, task_definition: Dict[str, Any], destination: RouteDestination) -> bool:
        """Dispatch the task to the specified destination."""
        pass

class DefaultTaskRouter(TaskRouterBase):
    """Concrete implementation of task router."""
    
    async def evaluate_task(self, task_definition: Dict[str, Any]) -> RouteDestination:
        agent_name = task_definition.get("agent_name", "default")
        
        execution_type = "sandbox" if agent_name == "CodeSandbox" else "llm"
        
        return RouteDestination(
            agent_id=agent_name,
            queue_name="default_queue",
            priority=1,
            execution_type=execution_type
        )
        
    async def route_task(self, task_definition: Dict[str, Any], destination: RouteDestination) -> bool:
        # Currently, routing is handled dynamically in execution_engine.
        # This method could be used to push to a task queue like Celery or Redis.
        return True
