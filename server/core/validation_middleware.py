from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable, Optional
from pydantic import BaseModel

try:
    from scripts.validation_layer import TaskValidator
except ImportError:
    TaskValidator = None

try:
    from server.context import set_tenant_id as set_tenant_context
except ImportError:
    set_tenant_context = None

class ValidationResult(BaseModel):
    """Represents the outcome of a validation check."""
    is_valid: bool
    error_message: Optional[str] = None
    metadata: dict[str, Any] = {}

class ValidationMiddlewareBase(ABC):
    """Abstract base class for validation middleware."""

    @abstractmethod
    def validate(self, request_data: Any) -> ValidationResult:
        """Perform validation on the incoming request or task data."""
        pass

class DomainViolationError(Exception):
    """Raised when an agent attempts an action outside its domain."""
    pass

class OrchestratorIsolationMiddleware(ValidationMiddlewareBase):
    """Ensures agents-orchestrator mode cannot write code directly."""
    
    def validate(self, tool_call: dict, agent_mode: str) -> ValidationResult:
        if agent_mode == "agents-orchestrator":
            tool_name = tool_call.get("name")
            if tool_name in ["write_to_file", "edit", "execute_command"]:
                msg = f"DomainViolationError: Orchestrator is forbidden from using {tool_name}. Delegate to a specialized agent."
                return ValidationResult(is_valid=False, error_message=msg)
        return ValidationResult(is_valid=True)

class TaskValidationMiddleware(ValidationMiddlewareBase):
    """Middleware for validating tasks during node execution."""

    def validate(self, task: str, tenant_id: str, agent_mode: str = None) -> ValidationResult:
        if TaskValidator and set_tenant_context:
            try:
                set_tenant_context(tenant_id)
                validator = TaskValidator()
                validator.pre_flight_check(task, agent_mode)
                return ValidationResult(is_valid=True)
            except Exception as e:
                return ValidationResult(is_valid=False, error_message=str(e))
        # If validator isn't available, pass silently (or handle as needed)
        return ValidationResult(is_valid=True)
