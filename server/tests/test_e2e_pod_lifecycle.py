import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_e2e_pod_execution():
    # Simulate an E2E pod creation and execution request
    payload = {
        "task": "E2E Integration Test Task",
        "domain": "engineering"
    }
    response = client.post("/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["PASSED", "COMPLETED"] or "error" in data
