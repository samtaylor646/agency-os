import pytest
from server.services.llm_runner import LLMRunner, OpenAIStrategy, AnthropicStrategy, MockStrategy

@pytest.mark.asyncio
async def test_llm_runner_mock():
    runner = LLMRunner()
    res = await runner.generate_response("hello")
    assert "Mock response" in res
