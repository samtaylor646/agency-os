import pytest
from fastapi.testclient import TestClient
from server.main import app
import json

client = TestClient(app)

def test_safe_code_execution():
    code = "print('Hello QA')"
    response = client.post(
        "/api/v1/sandbox/execute",
        headers={"X-Tenant-ID": "1"},
        json={"code": code}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Hello QA" in data["stdout"]
    assert data["exit_code"] == 0

def test_network_isolation():
    code = "import urllib.request; urllib.request.urlopen('http://google.com', timeout=3)"
    response = client.post(
        "/api/v1/sandbox/execute",
        headers={"X-Tenant-ID": "1"},
        json={"code": code}
    )
    assert response.status_code == 200
    data = response.json()
    combined_output = data["stdout"] + data["stderr"]
    assert "Temporary failure in name resolution" in combined_output or "urlopen error" in combined_output or "Name or service not known" in combined_output

def test_empty_code():
    response = client.post(
        "/api/v1/sandbox/execute",
        headers={"X-Tenant-ID": "1"},
        json={"code": ""}
    )
    assert response.status_code == 400

