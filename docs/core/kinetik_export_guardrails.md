# AgencyOS Guardrails Export for Kinetik OS

This document contains the exact `OrchestratorIsolationMiddleware` and `TaskValidator` hardening logic implemented in AgencyOS to prevent agent drift and enforce HITL (Human-in-the-Loop) checkpoints. Provide this to the Roo Code instance in your Kinetik OS workspace so it can adapt and implement these rules there.

## 1. Orchestrator Isolation Middleware
**Location equivalent in AgencyOS:** `server/core/validation_middleware.py`

```python
from pydantic import BaseModel
from typing import Optional, Any
from abc import ABC, abstractmethod

class ValidationResult(BaseModel):
    is_valid: bool
    error_message: Optional[str] = None
    metadata: dict[str, Any] = {}

class ValidationMiddlewareBase(ABC):
    @abstractmethod
    def validate(self, request_data: Any) -> ValidationResult:
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
```

## 2. Validation Layer Hardening
**Location equivalent in AgencyOS:** `scripts/validation_layer.py`

```python
class TaskValidator:
    def pre_flight_check(self, task: str, agent_mode: str = None) -> str:
        # Prevent orchestrator from directly resolving coding tasks without delegation
        if agent_mode == "agents-orchestrator" and ("write" in task.lower() or "implement" in task.lower()):
            raise Exception("ROUTING FIRST MANDATE: Orchestrator cannot resolve implementation tasks directly.")
        print(f"Validation passed for task: {task} (mode: {agent_mode})")
        return "valid"
```

## 3. Implementation Instructions for Kinetik OS Agent
1. Create or update the middleware layer in Kinetik OS to intercept tool calls based on the `agent_mode`.
2. Integrate the `OrchestratorIsolationMiddleware` to block `write_to_file`, `edit`, and `execute_command` for the orchestrator.
3. Update the task parsing logic (similar to `TaskValidator`) to raise an exception if the orchestrator attempts implementation tasks without delegating.
4. Update `.clinerules` in Kinetik OS to mandate `ROUTING FIRST` and `Orchestrator Isolation`.
