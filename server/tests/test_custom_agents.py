import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.main import app
from server.database import Base, get_db
from server import models
import uuid
import os
import shutil

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_custom_agents.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    workspace = models.Workspace(name="Test Workspace")
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    
    user = models.User(email="test@example.com", hashed_password="hashed_password", tenant_id=workspace.id)
    db.add(user)
    db.commit()
    
    yield
    
    db.close()
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_custom_agents.db"):
        os.remove("./test_custom_agents.db")
    if os.path.exists("agents/custom"):
        shutil.rmtree("agents/custom", ignore_errors=True)

def test_create_custom_agent():
    client = TestClient(app)
    
    # Needs auth token typically, assuming test uses a mock or we need to add one.
    # Actually, we can bypass auth for simple tests by overriding get_api_or_user_tenant_context.
    from server.dependencies import get_api_or_user_tenant_context
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 1
    
    payload = {
        "identity": {
            "name": "Wizard Agent",
            "role": "Test Role",
            "version": "1.0.0"
        },
        "system_rules": {
            "path": "config/settings.md",
            "enforcement_level": "Strict"
        },
        "capabilities": ["cap1", "cap2"],
        "constraints": ["const1", "const2"],
        "system_prompt": "You are a wizard."
    }
    
    response = client.post("/api/v1/custom_agents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Wizard Agent"
    assert data["role"] == "Test Role"
    assert "filepath" in data
    
    # Read the file
    filepath = data["filepath"]
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        content = f.read()
    
    assert "Wizard Agent" in content
    assert "Test Role" in content
    assert "cap1" in content
    assert "const1" in content
    assert "You are a wizard." in content
def test_tenant_isolation_get_agents():
    client = TestClient(app)
    
    # Create agents for Tenant 1 and Tenant 2
    from server.dependencies import get_api_or_user_tenant_context
    
    # Tenant 1 Context
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 1
    client.post("/api/v1/custom_agents", json={
        "identity": {"name": "Tenant 1 Agent", "role": "Role 1", "version": "1.0.0"},
        "system_rules": {"path": "config/settings.md", "enforcement_level": "Strict"},
        "capabilities": [], "constraints": [], "system_prompt": "Prompt 1"
    })
    
    # Tenant 2 Context
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 2
    client.post("/api/v1/custom_agents", json={
        "identity": {"name": "Tenant 2 Agent", "role": "Role 2", "version": "1.0.0"},
        "system_rules": {"path": "config/settings.md", "enforcement_level": "Strict"},
        "capabilities": [], "constraints": [], "system_prompt": "Prompt 2"
    })
    
    # Test Isolation
    
    # Request as Tenant 1
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 1
    res1 = client.get("/api/v1/custom_agents")
    assert res1.status_code == 200
    agents1 = res1.json()
    assert len(agents1) == 2 # 1 previous wizard agent + 1 this one
    names1 = [a["name"] for a in agents1]
    assert "Tenant 1 Agent" in names1
    assert "Tenant 2 Agent" not in names1
    
    # Request as Tenant 2
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 2
    res2 = client.get("/api/v1/custom_agents")
    assert res2.status_code == 200
    agents2 = res2.json()
    assert len(agents2) == 1
def test_update_custom_agent():
    client = TestClient(app)
    from server.dependencies import get_api_or_user_tenant_context
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 1
    
    # Create
    payload = {
        "identity": {"name": "Old Name", "role": "Old Role", "description": "Old desc", "color": "#000000", "emoji": "🤔", "vibe": "chill", "intro_paragraph": "Hi"},
        "system_rules": {"personality": "nice", "experience": "high", "memory": "good", "mission": "win", "rules": "none", "deliverables": "code", "communication": "direct", "learning": "fast", "success_metrics": "KPI"},
        "capabilities": [],
        "constraints": [],
        "system_prompt": "Old prompt"
    }
    create_res = client.post("/api/v1/custom_agents", json=payload)
    assert create_res.status_code == 201
    agent_id = create_res.json()["id"]
    
    # Update
    payload["identity"]["name"] = "New Name"
    payload["system_prompt"] = "New prompt"
    
    update_res = client.put(f"/api/v1/custom_agents/{agent_id}", json=payload)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "New Name"
    
    filepath = update_res.json()["filepath"]
    with open(filepath, "r") as f:
        content = f.read()
    assert "New Name" in content
    assert "New prompt" in content

def test_delete_custom_agent():
    client = TestClient(app)
    from server.dependencies import get_api_or_user_tenant_context
    app.dependency_overrides[get_api_or_user_tenant_context] = lambda: 1
    
    payload = {
        "identity": {"name": "Delete Me", "role": "Role", "description": "desc", "color": "#000", "emoji": "🤔", "vibe": "chill", "intro_paragraph": "Hi"},
        "system_rules": {"personality": "nice", "experience": "high", "memory": "good", "mission": "win", "rules": "none", "deliverables": "code", "communication": "direct", "learning": "fast", "success_metrics": "KPI"},
        "capabilities": [],
        "constraints": [],
        "system_prompt": "Prompt"
    }
    create_res = client.post("/api/v1/custom_agents", json=payload)
    assert create_res.status_code == 201
    agent_id = create_res.json()["id"]
    filepath = create_res.json()["filepath"]
    assert os.path.exists(filepath)
    
    delete_res = client.delete(f"/api/v1/custom_agents/{agent_id}")
    assert delete_res.status_code == 204
    
    get_res = client.get("/api/v1/custom_agents")
    agents = get_res.json()
    assert not any(a["id"] == agent_id for a in agents)
    
    assert not os.path.exists(filepath)

