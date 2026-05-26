import asyncio
from central_runner import DAGOrchestrator, TerminalNodeError
from unittest.mock import patch
from server.services.llm_runner import llm_runner

async def test_cascading_failure():
    print("Testing cascading failure on single node crash...")
    dag = DAGOrchestrator()
    dag.add_node("n1", "agent1", "task1")
    dag.add_node("n2", "agent2", "task2", ["n1"])
    dag.add_node("n3", "agent3", "task3", ["n2"])
    dag.add_edge("n1", "n2")
    dag.add_edge("n2", "n3")

    # Mock n1 to fail permanently
    async def mock_generate_response(prompt, system_prompt=None):
        raise ValueError("Simulated permanent crash!")
        
    with patch.object(llm_runner, 'generate_response', new=mock_generate_response):
        result = await dag.execute_workflow(tenant_id="1")
        print("Workflow Result:", result["status"])
        for node_id, data in result["results"].items():
            print(f"Node {node_id}: {data['status']}")

if __name__ == "__main__":
    asyncio.run(test_cascading_failure())
