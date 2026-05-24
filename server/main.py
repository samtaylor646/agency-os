import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, auth
from .database import engine, get_db
from .routers import workspaces
from .context import set_tenant_id, get_tenant_id
from scripts.central_runner import DAGOrchestrator

# For development MVP, create tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgencyOS API")

@app.middleware("http")
async def tenant_id_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    if tenant_id:
        set_tenant_id(tenant_id)
    response = await call_next(request)
    return response

app.include_router(workspaces.router)

@app.get('/')
def read_root():
    return {'status': 'AgencyOS Server Online'}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Get user's role and workspaces from memberships
    memberships = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id).all()
    tenant_ids = [m.workspace_id for m in memberships]
    
    # Simple role assignment for MVP: highest role across workspaces or default
    # A real system might encode a mapping of {workspace_id: role}
    roles = [m.role for m in memberships]
    primary_role = models.RoleEnum.SUPER_ADMIN.value if models.RoleEnum.SUPER_ADMIN.value in roles else \
                   (models.RoleEnum.AGENCY_ADMIN.value if models.RoleEnum.AGENCY_ADMIN.value in roles else \
                   models.RoleEnum.CLIENT_APPROVER.value)
                   
    # Super admins should probably be explicitly defined, but for MVP:
    if not roles and user.email == "admin@agencyos.com":
        primary_role = models.RoleEnum.SUPER_ADMIN.value
    elif not roles:
        primary_role = models.RoleEnum.CLIENT_READ_ONLY.value

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": primary_role, "tenant_ids": tenant_ids}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/workflows/run")
async def run_workflow(request: schemas.WorkflowRunRequest, current_user: schemas.UserOut = Depends(auth.get_current_user)):
    tenant_id = get_tenant_id()
    if not tenant_id:
        # Fallback to current user ID as tenant ID if not provided via middleware
        tenant_id = str(current_user.id)
        
    orchestrator = DAGOrchestrator()
    for node in request.nodes:
        orchestrator.add_node(
            node_id=node.node_id,
            agent_name=node.agent_name,
            task=node.task,
            required_inputs=node.required_inputs
        )
        
    for edge in request.edges:
        orchestrator.add_edge(from_node=edge.from_node, to_node=edge.to_node)
        
    results = await orchestrator.execute_workflow(tenant_id=str(tenant_id))
    if isinstance(results, dict) and "error" in results:
        raise HTTPException(status_code=400, detail=results["error"])
        
    return {"status": "success", "results": results}

