import asyncio
import time
from unittest.mock import patch
from central_runner import DAGOrchestrator, execute_node_with_retry, TransientNodeError, TerminalNodeError
from server.services.llm_runner import llm_runner

async def test_retry_success():
    print("Testing retry success after 2 failures...")
    
    attempts = 0
    original_generate = llm_runner.generate_response
    
    async def mock_generate_response(*args, **kwargs):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            print(f"  Attempt {attempts}: Simulating transient failure...")
            raise TransientNodeError("Simulated network timeout")
        print(f"  Attempt {attempts}: Success!")
        return await original_generate(*args, **kwargs)
    
    with patch.object(llm_runner, 'generate_response', new=mock_generate_response):
        start = time.time()
        result = await execute_node_with_retry(
            node_id="test_node_1",
            agent_name="product-manager",
            task="Do something",
            context_data={},
            tenant_id="1"
        )
        end = time.time()
        print(f"Result: {result.status}")
        print(f"Took: {end - start:.2f} seconds")
        assert attempts == 3
        assert result.status == "success"
        print("Success test passed!\n")

async def test_retry_failure():
    print("Testing retry permanent failure after 3 transient failures...")
    
    attempts = 0
    
    async def mock_generate_response(*args, **kwargs):
        nonlocal attempts
        attempts += 1
        print(f"  Attempt {attempts}: Simulating transient failure...")
        raise TransientNodeError("Simulated network timeout")
    
    with patch.object(llm_runner, 'generate_response', new=mock_generate_response):
        try:
            await execute_node_with_retry(
                node_id="test_node_2",
                agent_name="product-manager",
                task="Do something else",
                context_data={},
                tenant_id="1"
            )
            assert False, "Should have raised TransientNodeError after all retries exhausted"
        except TransientNodeError:
            print(f"Caught expected TransientNodeError after {attempts} attempts.")
            assert attempts == 3
            print("Failure test passed!\n")

if __name__ == "__main__":
    asyncio.run(test_retry_success())
    asyncio.run(test_retry_failure())
