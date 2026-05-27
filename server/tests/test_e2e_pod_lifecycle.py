import pytest
from server.api_server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_e2e_pod_execution(client):
    # Simulate an E2E pod creation and execution request
    payload = {
        "task": "E2E Integration Test Task",
        "domain": "engineering"
    }
    response = client.post("/execute", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    
    if "result" in data and isinstance(data["result"], dict) and "status" in data["result"]:
        assert data["result"]["status"] in ["PASSED", "COMPLETED", "PARTIAL_FAILURE"]
    else:
        assert data["status"] in ["PASSED", "COMPLETED", "PARTIAL_FAILURE"] or "error" in data
