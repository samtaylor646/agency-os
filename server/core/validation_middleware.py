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

class TaskValidationMiddleware(ValidationMiddlewareBase):
    """Middleware for validating tasks during node execution."""

    def validate(self, task: str, tenant_id: str) -> ValidationResult:
        if TaskValidator and set_tenant_context:
            try:
                set_tenant_context(tenant_id)
                validator = TaskValidator()
                validator.pre_flight_check(task)
                return ValidationResult(is_valid=True)
            except Exception as e:
                return ValidationResult(is_valid=False, error_message=str(e))
        # If validator isn't available, pass silently (or handle as needed)
        return ValidationResult(is_valid=True)
