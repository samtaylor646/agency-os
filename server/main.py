import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from .middleware_audit import AuditMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from . import models, schemas, auth, dependencies
from .database import engine, get_db
from .routers import workspaces, credentials, api_keys, webhooks, rbac, analytics, marketplace, audit, chat, documents, custom_agents, pipelines
from .context import set_tenant_id, get_tenant_id
from scripts.central_runner import DAGOrchestrator

# For development MVP, create tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgencyOS API")

import re

DEBUG_VALIDATION = os.getenv("DEBUG_VALIDATION", "false").lower() == "true"

def redact_pii(text: str) -> str:
    if not isinstance(text, str):
        return text
    # Redact Emails
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', text)
    # Redact Phone Numbers
    text = re.sub(r'\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[REDACTED_PHONE]', text)
    # Redact SSN (US)
    text = re.sub(r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b', '[REDACTED_SSN]', text)
    # Redact Credit Cards (basic)
    text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[REDACTED_CC]', text)
    # Password / Secrets in JSON
    text = re.sub(r'(?i)("password"|"secret"|"key"|"token"|"api_key")\s*:\s*"[^"]+"', r'\1: "[REDACTED]"', text)
    # Redact Bearer Tokens
    text = re.sub(r'Bearer\s+[A-Za-z0-9\-\._~+/]+=*', 'Bearer [REDACTED_TOKEN]', text)
    # Redact OpenAI / standard sk- keys
    text = re.sub(r'\bsk-[a-zA-Z0-9_-]{20,}\b', '[REDACTED_API_KEY]', text)
    return text

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors_str = redact_pii(str(exc.errors()))
    
    if DEBUG_VALIDATION:
        try:
            body = await request.body()
            body_str = body.decode('utf-8')
            redacted_body = redact_pii(body_str)
            logger.error(f"Validation Error: {errors_str}")
            logger.error(f"Redacted Body: {redacted_body}")
        except Exception:
            logger.error(f"Validation Error: {errors_str}")
    else:
        logger.error(f"Validation Error: {errors_str}")
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error"},
    )

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
                    role = payload.get("role")
                    # Verify requested tenant_id is in allowed_tenants
                    if tenant_id and role != "super_admin":
                        allowed_ints = [int(t) for t in allowed_tenants if str(t).isdigit()]
                        if int(tenant_id) not in allowed_ints and str(tenant_id) not in [str(t) for t in allowed_tenants]:
                            return JSONResponse(
                                status_code=status.HTTP_403_FORBIDDEN,
                                content={"detail": f"Forbidden: Tenant access denied. requested: {tenant_id}, allowed: {allowed_tenants}"}
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
app.include_router(audit.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(custom_agents.router)
app.include_router(pipelines.router)

@app.get('/')
def read_root():
    return {'status': 'AgencyOS Server Online'}

@app.post("/api/v1/token", response_model=schemas.Token)
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

@app.post("/api/v1/workflows/run")
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

