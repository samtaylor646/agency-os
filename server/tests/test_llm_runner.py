import pytest
from server.services.llm_runner import LLMRunner

@pytest.mark.asyncio
async def test_generate_response():
    runner = LLMRunner()
    prompt = "Hello, what is the meaning of life?"
    response = await runner.generate_response(prompt)
    assert "Mock response" in response
    assert prompt[:50] in response

@pytest.mark.asyncio
async def test_generate_document():
    runner = LLMRunner()
    context = {"name": "Test App", "description": "A test app", "tech_stack": ["React", "Python"]}
    
    prd = await runner.generate_document("prd", context)
    assert "# PRD: Test App" in prd
    
    arch = await runner.generate_document("architecture", context)
    assert "# Architecture Spec: Test App" in arch
    assert "React, Python" in arch
    
    tasks = await runner.generate_document("tasks", context)
    assert "# Task List: Test App" in tasks

@pytest.mark.asyncio
async def test_parse_intent():
    runner = LLMRunner()
    
    # Test 1: Simple message
    msg1 = "I want to build a cool app"
    res1 = await runner.parse_intent(msg1)
    assert res1["name"] == "Cool App"
    assert res1["description"] == msg1
    assert "Unknown" in res1["tech_stack"]
    
    # Test 2: Message with web
    msg2 = "A new web project"
    res2 = await runner.parse_intent(msg2)
    assert res2["name"] == "Web Project"
    assert "React" in res2["tech_stack"]

@pytest.mark.asyncio
async def test_refine_document():
    runner = LLMRunner()
    current = "My old doc"
    feedback = "Add a new section"
    
    result = await runner.refine_document("prd", current, feedback)
    
    assert "My old doc" in result["content"]
    assert "Add a new section" in result["content"]
    assert "prd" in result["chat_response"]

@pytest.mark.asyncio
async def test_ingest_document():
    runner = LLMRunner()
    file_content = b"Some PRD text here"
    filename = "spec_doc.txt"
    
    result = await runner.ingest_document(file_content, filename)
    
    assert result["name"] == "Spec Doc"
    assert "spec_doc.txt" in result["description"]
    assert result["tech_stack"] == ["Unknown", "Auto-detected"]

