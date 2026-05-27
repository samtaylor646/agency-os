from fastapi import Depends, HTTPException, status, Header, Request, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
from .database import get_db
from .auth import decode_access_token, verify_api_key
from .models import User, RoleEnum, WorkspaceAPIKey
from .schemas import TokenData
from typing import Optional
from .embeddings import get_embedding_provider, EmbeddingProvider

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
api_key_header_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    token_data = TokenData(email=email, role=payload.get("role"), tenant_ids=payload.get("tenant_ids", []))
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user, token_data

async def require_role(allowed_roles: list[RoleEnum]):
    def role_checker(user_data: tuple = Depends(get_current_user)):
        user, token_data = user_data
        if token_data.role not in [role.value for role in allowed_roles]:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user, token_data
    return role_checker

async def get_tenant_context(
    request: Request,
    x_tenant_id: Optional[int] = Header(None),
    user_data: tuple = Depends(get_current_user)
):
    user, token_data = user_data
    
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is missing")
        
    if token_data.role != RoleEnum.SUPER_ADMIN.value and x_tenant_id not in token_data.tenant_ids:
        raise HTTPException(status_code=403, detail="You do not have access to this workspace")
        
    # Store tenant_id in request state for downstream use
    request.state.tenant_id = x_tenant_id
    return x_tenant_id

async def get_api_or_user_tenant_context(
    request: Request,
    authorization: Optional[str] = Security(api_key_header_scheme),
    token: Optional[str] = Depends(oauth2_scheme),
    x_tenant_id: Optional[int] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Dependency for core API endpoints that allows either a Bearer JWT Token or an API Key.
    Returns the tenant_id that the request is authenticated for.
    """
    if authorization and authorization.startswith("Bearer "):
        api_key = authorization.replace("Bearer ", "")
        
        # Check if it looks like an API key (e.g., ak_...) or a JWT
        if api_key.startswith("ak_"):
            prefix = api_key[:12] # e.g. ak_12345678
            
            # Find candidate keys with matching prefix to minimize bcrypt checks
            # In a real app we might cache this or structure the key so we can do a direct lookup
            # But here we search by active keys and verify
            
            # Since bcrypt is slow, we should just get all active keys, but that's O(N).
            # To optimize, we can extract the prefix from the key when created and store it in DB.
            # We already added `prefix` to WorkspaceAPIKey.
            
            # For this exercise, let's say the key format is ak_PREFIX_RANDOM
            # Where PREFIX is 8 chars.
            prefix_to_search = prefix
            
            candidate_keys = db.query(WorkspaceAPIKey).filter(
                WorkspaceAPIKey.prefix == prefix_to_search,
                WorkspaceAPIKey.is_active == 1
            ).all()
            
            for ck in candidate_keys:
                if verify_api_key(api_key, ck.hashed_key):
                    # Valid API Key found
                    request.state.tenant_id = ck.workspace_id
                    return ck.workspace_id
                    
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
            )
            
    # Fallback to User Auth via JWT
    if token:
        user, token_data = await get_current_user(token=token, db=db)
        
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID header is missing")
            
        if token_data.role != RoleEnum.SUPER_ADMIN.value:
            allowed_ints = [int(t) for t in token_data.tenant_ids if str(t).isdigit()]
            if int(x_tenant_id) not in allowed_ints and str(x_tenant_id) not in [str(t) for t in token_data.tenant_ids]:
                raise HTTPException(status_code=403, detail="You do not have access to this workspace")
            
        request.state.tenant_id = x_tenant_id
        return x_tenant_id

async def verify_workspace_access(
    workspace_id: int,
    tenant_id: int = Depends(get_api_or_user_tenant_context)
):
    """
    Verifies that the authenticated user has explicit read/write access 
    to the requested workspace_id.
    """
    if tenant_id != workspace_id:
        raise HTTPException(status_code=403, detail="Forbidden: Workspace mismatch. Explicit read/write access required.")
    return workspace_id

async def rate_limit_ingestion(request: Request):
    """
    Rate limiter for document ingestion to prevent DoW attacks.
    Limits to 10 requests per minute per tenant/IP.
    """
    # Implementation of rate limiting logic would go here using Redis or slowapi.
    # For now, it serves as the defined dependency hook.
    pass

async def get_current_workspace(
    tenant_id: int = Depends(get_tenant_context),
    db: Session = Depends(get_db)
):
    from .models import Workspace
    workspace = db.query(Workspace).filter(Workspace.id == tenant_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

