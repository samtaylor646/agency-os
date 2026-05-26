import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.main import app
from server.database import Base, get_db
from server.dependencies import get_api_or_user_tenant_context
from server.models import Workspace
import os
import io

from sqlalchemy.pool import StaticPool

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_tenant_context():
    return 1 # return a mock workspace id

@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_api_or_user_tenant_context] = override_get_tenant_context
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

@pytest.fixture()
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Create test workspace
    workspace = Workspace(id=1, name="Test Workspace")
    db.add(workspace)
    db.commit()
    yield
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_ingest_document(setup_db):
    # Mock text file upload
    file_content = b"This is a test document."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.post(
        "/api/v1/workspaces/1/documents/ingest",
        files=files,
        headers={"X-Tenant-ID": "1"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"
    
    job_id = data["job_id"]
    
    # Check status endpoint
    status_resp = client.get(
        f"/api/v1/workspaces/1/documents/ingest/status/{job_id}",
        headers={"X-Tenant-ID": "1"}
    )
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["job_id"] == job_id
    assert status_data["status"] in ["pending", "analyzing", "completed"] # depending on async execution speed

def test_ingest_document_invalid_type(setup_db):
    file_content = b"Fake exe"
    files = {"file": ("test.exe", io.BytesIO(file_content), "application/x-msdownload")}
    
    response = client.post(
        "/api/v1/workspaces/1/documents/ingest",
        files=files,
        headers={"X-Tenant-ID": "1"}
    )
    
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_ingest_document_tenant_mismatch(setup_db):
    file_content = b"This is a test document."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.post(
        "/api/v1/workspaces/2/documents/ingest", # requesting workspace 2 but tenant is 1
        files=files,
        headers={"X-Tenant-ID": "1"} # Note: Context override returns 1
    )
    
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]
