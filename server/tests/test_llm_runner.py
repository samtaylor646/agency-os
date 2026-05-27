import pytest
import sys
from unittest.mock import MagicMock
import os

# Mock the external libraries before importing the runner
sys.modules['openai'] = MagicMock()
sys.modules['anthropic'] = MagicMock()

from server.services.llm_runner import LLMRunner, OpenAIProvider, AnthropicProvider, MockProvider

@pytest.mark.asyncio
async def test_providers_initialization():
    os.environ["OPENAI_API_KEY"] = "sk-test"
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
    
    runner = LLMRunner(provider="openai")
    assert isinstance(runner.provider, OpenAIProvider)
    
    runner2 = LLMRunner(provider="anthropic")
    assert isinstance(runner2.provider, AnthropicProvider)
    
    runner3 = LLMRunner(provider="mock")
    assert isinstance(runner3.provider, MockProvider)

@pytest.mark.asyncio
async def test_mock_fallback():
    runner = LLMRunner(provider="mock")
    
    response = await runner.generate_response("Test prompt")
    assert "Mock response" in response
    assert "Test prompt" in response
    
    doc = await runner.generate_document("prd", {"name": "Test"})
    assert "Mock response" in doc
    
    parsed = await runner.parse_intent("I want an app")
    assert parsed["name"] == "Parsed Project"
    
    refined = await runner.refine_document("prd", "old doc", "feedback")
    assert "Mock response" in refined["content"]
    assert "updated the prd based on your feedback" in refined["chat_response"]
