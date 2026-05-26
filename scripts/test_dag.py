import asyncio
from central_runner import DAGOrchestrator

async def run_test():
    print("Initializing DAG Orchestrator...")
    dag = DAGOrchestrator(workflow_name="test_epic_a")
    
    # Add nodes
    dag.add_node("node1", "product-manager", "Analyze requirements")
    dag.add_node("node2", "backend-architect", "Design architecture", required_inputs=["node1"])
    dag.add_edge("node1", "node2")
    
    print("Executing Workflow...")
    result = await dag.execute_workflow(tenant_id="1")
    print(f"Result: {result}")
    print(f"State: {dag.state}")

if __name__ == "__main__":
    asyncio.run(run_test())
