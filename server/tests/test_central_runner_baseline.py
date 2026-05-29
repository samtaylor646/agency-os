import pytest
import asyncio
from unittest.mock import patch, MagicMock
import json

from server.services.orchestrator_service import DAGOrchestrator, execute_node_with_retry, TransientNodeError, TerminalNodeError

@pytest.fixture
def mock_dependencies():
    with patch("server.services.orchestrator_service.SessionLocal", new=None), \
         patch("server.services.orchestrator_service.message_broker", new=None), \
         patch("server.services.orchestrator_service.AgentExecutionMetric", new=None), \
         patch("server.services.orchestrator_service.WorkflowExecution", new=None), \
         patch("server.services.llm_runner.llm_runner.generate_response", new_callable=MagicMock) as mock_llm:
        mock_llm.return_value = asyncio.Future()
        mock_llm.return_value.set_result("Mocked LLM Response")
        yield mock_llm

@pytest.mark.asyncio
async def test_dag_orchestrator_basic_workflow(mock_dependencies):
    orchestrator = DAGOrchestrator(workflow_name="test_basic_workflow")
    
    orchestrator.add_node("node1", "TestAgent", "Do task 1")
    orchestrator.add_node("node2", "TestAgent", "Do task 2")
    orchestrator.add_edge("node1", "node2")
    
    # Run workflow
    result = await orchestrator.execute_workflow(tenant_id="1")
    
    assert result["status"] == "COMPLETED"
    assert "node1" in result["results"]
    assert result["results"]["node1"]["status"] == "success"
    assert "node2" in result["results"]
    assert result["results"]["node2"]["status"] == "success"


@pytest.mark.asyncio
async def test_codesandbox_routing():
    with patch("server.services.orchestrator_service.SessionLocal", new=None), \
         patch("server.services.orchestrator_service.message_broker", new=None), \
         patch("server.services.sandbox.sandbox_env.execute_script", new_callable=MagicMock) as mock_sandbox:
         
        mock_sandbox.return_value = {"stdout": "hello world", "stderr": "", "exit_code": 0}
        
        task_data = json.dumps({"code": "print('hello world')"})
        
        result = await execute_node_with_retry(
            node_id="sandbox_node",
            agent_name="CodeSandbox",
            task=task_data,
            context_data={},
            tenant_id="1"
        )
        
        assert result.status == "success"
        assert "hello world" in result.result["output"]
        mock_sandbox.assert_called_once_with("print('hello world')")

@pytest.mark.asyncio
async def test_dag_cycle_detection():
    orchestrator = DAGOrchestrator(workflow_name="test_cycle_workflow")
    orchestrator.add_node("node1", "TestAgent", "Do task 1")
    orchestrator.add_node("node2", "TestAgent", "Do task 2")
    orchestrator.add_edge("node1", "node2")
    orchestrator.add_edge("node2", "node1")
    
    result = await orchestrator.execute_workflow(tenant_id="1")
    assert result["status"] == "FAILED"
    assert "Cycle detected" in result["error"]
