import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from server.main import app
from server.dependencies import get_current_user

# Mock dependency
async def override_get_current_user():
    return {"id": 1, "username": "testuser"}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@patch('server.routers.chat.llm_runner.parse_intent', new_callable=AsyncMock)
@patch('server.routers.chat.llm_runner.generate_response', new_callable=AsyncMock)
def test_chat_scope_success(mock_generate, mock_parse):
    mock_parse.return_value = {
        "name": "Test Project",
        "description": "Testing the chat router",
        "tech_stack": ["FastAPI", "React"],
        "raw_message": "test message"
    }
    mock_generate.return_value = "Mocked chat response"

    response = client.post("/api/v1/chat/scope", json={"message": "test message"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["chat_response"] == "Mocked chat response"
    assert data["extraction"]["name"] == "Test Project"
    assert data["extraction"]["description"] == "Testing the chat router"

@patch('server.routers.chat.llm_runner.parse_intent', new_callable=AsyncMock)
def test_chat_scope_error(mock_parse):
    mock_parse.side_effect = Exception("LLM Error")

    response = client.post("/api/v1/chat/scope", json={"message": "test message"})
    
    assert response.status_code == 500
    assert "LLM Error" in response.json()["detail"]
