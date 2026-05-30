import pytest
import asyncio
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_task_validator():
    with patch('server.services.orchestrator_service.TaskValidationMiddleware.validate') as mock_validate:
        mock_val = MagicMock()
        mock_val.is_valid = True
        mock_val.requires_human_approval = False
        mock_validate.return_value = mock_val
        yield mock_validate
from server.services.orchestrator_service import DAGOrchestrator, execute_node_with_retry, TransientNodeError, TerminalNodeError
from server.services.llm_runner import llm_runner

@pytest.mark.asyncio
async def test_dag_execution():
    dag = DAGOrchestrator(workflow_name="test_epic_a")
    dag.add_node("node1", "product-manager", "Analyze requirements")
    dag.add_node("node2", "backend-architect", "Design architecture", required_inputs=["node1"])
    dag.add_edge("node1", "node2")
    
    # Mock generation to avoid real LLM calls
    async def mock_generate(*args, **kwargs):
        return "mocked response"
        
    with patch.object(llm_runner, 'generate_response', new=mock_generate):
        result = await dag.execute_workflow(tenant_id="1")
        assert result["status"] == "PAUSED"
        assert dag.state == "PAUSED"

def test_dag_disconnected():
    dag = DAGOrchestrator()
    dag.add_node("n1", "agent1", "task1")
    dag.add_node("n2", "agent2", "task2")
    levels = dag.get_topological_sort()
    assert len(levels) > 0

def test_dag_cycle():
    dag = DAGOrchestrator()
    dag.add_node("n1", "agent1", "task1")
    dag.add_node("n2", "agent2", "task2", ["n1"])
    dag.add_node("n3", "agent3", "task3", ["n2"])
    dag.add_edge("n1", "n2")
    dag.add_edge("n2", "n3")
    dag.add_edge("n3", "n1") # cycle
    with pytest.raises(ValueError):
        dag.get_topological_sort()

@pytest.mark.asyncio
async def test_retry_success():
    attempts = 0
    original_generate = llm_runner.generate_response
    
    async def mock_generate_response(*args, **kwargs):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TransientNodeError("Simulated network timeout")
        return await original_generate(*args, **kwargs)
    
    with patch.object(llm_runner, 'generate_response', new=mock_generate_response):
        result = await execute_node_with_retry(
            node_id="test_node_1",
            agent_name="product-manager",
            task="Do something",
            context_data={},
            tenant_id="1"
        )
        assert attempts == 3
        assert result.status == "success"

@pytest.mark.asyncio
async def test_retry_failure():
    attempts = 0
    async def mock_generate_response(*args, **kwargs):
        nonlocal attempts
        attempts += 1
        raise TransientNodeError("Simulated network timeout")
    
    with patch.object(llm_runner, 'generate_response', new=mock_generate_response):
        with pytest.raises(TransientNodeError):
            await execute_node_with_retry(
                node_id="test_node_2",
                agent_name="product-manager",
                task="Do something else",
                context_data={},
                tenant_id="1"
            )
        assert attempts == 3

@pytest.mark.asyncio
async def test_cascading_failure():
    dag = DAGOrchestrator()
    dag.add_node("n1", "agent1", "task1")
    dag.add_node("n2", "agent2", "task2", ["n1"])
    dag.add_node("n3", "agent3", "task3", ["n2"])
    dag.add_edge("n1", "n2")
    dag.add_edge("n2", "n3")

    async def mock_generate_response(prompt, system_prompt=None):
        raise ValueError("Simulated permanent crash!")
        
    with patch.object(llm_runner, 'generate_response', new=mock_generate_response):
        result = await dag.execute_workflow(tenant_id="1")
        assert result["status"] == "PAUSED"
