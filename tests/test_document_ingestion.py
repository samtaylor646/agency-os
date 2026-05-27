import pytest
from fastapi.testclient import TestClient
from server.main import app
import json

client = TestClient(app)

def test_document_ingestion_endpoint():
    # We must be authenticated for /api/v1/chat endpoint which has user deps.
    # Actually wait, /api/v1/chat requires get_current_workspace, get_db, which we can mock or just create a user.
    # Since we lack the DB state in the test environment, we might get a 401/403. Let's see.
    pass
