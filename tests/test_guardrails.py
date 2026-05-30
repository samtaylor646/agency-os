import pytest
from server.core.validation_middleware import OrchestratorIsolationMiddleware, ValidationResult

def test_orchestrator_isolation_middleware_rejects_file_writes():
    middleware = OrchestratorIsolationMiddleware()
    tool_call = {"name": "write_to_file"}
    agent_mode = "agents-orchestrator"
    
    result = middleware.validate(tool_call, agent_mode)
    
    assert result.is_valid == False
    assert "DomainViolationError" in result.error_message
    assert "write_to_file" in result.error_message

def test_orchestrator_isolation_middleware_allows_delegation():
    middleware = OrchestratorIsolationMiddleware()
    tool_call = {"name": "new_task"}
    agent_mode = "agents-orchestrator"
    
    result = middleware.validate(tool_call, agent_mode)
    
    assert result.is_valid == True
    assert result.error_message is None

def test_specialized_agent_allowed_file_writes():
    middleware = OrchestratorIsolationMiddleware()
    tool_call = {"name": "write_to_file"}
    agent_mode = "backend-architect"
    
    result = middleware.validate(tool_call, agent_mode)
    
    assert result.is_valid == True
    assert result.error_message is None
