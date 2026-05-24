import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from .middleware_audit import AuditMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, auth, dependencies
from .database import engine, get_db
from .routers import workspaces, credentials, api_keys, webhooks, rbac, analytics, marketplace
from .context import set_tenant_id, get_tenant_id
from scripts.central_runner import DAGOrchestrator

# For development MVP, create tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgencyOS API")

# Add CORS Middleware
app.add_middleware(AuditMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def secure_tenant_and_headers_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    if tenant_id:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = auth.decode_access_token(token)
                if payload:
                    allowed_tenants = payload.get("tenant_ids", [])
                    # Verify requested tenant_id is in allowed_tenants
                    if int(tenant_id) not in allowed_tenants:
                        return JSONResponse(
                            status_code=status.HTTP_403_FORBIDDEN,
                            content={"detail": "Forbidden: Tenant access denied"}
                        )
            except Exception:
                # If token is invalid or parsing fails, let the normal auth flow handle it or reject
                pass
        
        set_tenant_id(tenant_id)
        
    response = await call_next(request)
    
    # Add Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

app.include_router(workspaces.router)
app.include_router(credentials.router)
app.include_router(api_keys.router)
app.include_router(webhooks.router)
app.include_router(rbac.router)
app.include_router(analytics.router)
app.include_router(marketplace.router)

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
async def run_workflow(
    request: schemas.WorkflowRunRequest,
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    # Set the tenant context for any thread-local usages just in case
    set_tenant_id(str(tenant_id))
        
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

