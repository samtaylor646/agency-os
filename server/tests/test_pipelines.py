import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.main import app
from server.database import get_db, Base
from server.models import Pipeline, PipelineRun, Workspace

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pipelines.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    ws = Workspace(name="test_ws")
    db.add(ws)
    db.commit()
    
    p = Pipeline(name="test_pipeline", tenant_id=ws.id)
    db.add(p)
    db.commit()
    
    yield
    Base.metadata.drop_all(bind=engine)
    db.close()

def test_start_pipeline():
    response = client.post("/pipelines/1/run")
    assert response.status_code == 200
    data = response.json()
    assert data["pipeline_id"] == 1
    assert data["status"] == "RUNNING"

def test_pause_pipeline():
    response = client.post("/pipelines/runs/1/pause")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "WAITING_APPROVAL"

def test_approve_pipeline():
    response = client.post("/pipelines/runs/1/approve", json={"action": "approve"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNNING"

def test_reject_pipeline():
    client.post("/pipelines/runs/1/pause")
    response = client.post("/pipelines/runs/1/approve", json={"action": "reject"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "REJECTED"

def test_error_pipeline():
    response = client.post("/pipelines/runs/1/error?error_message=Something%20broke")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ERROR"
    assert data["error_message"] == "Something broke"

def test_chat_pipeline():
    response = client.post("/pipelines/runs/1/chat?role=user&content=hello")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
