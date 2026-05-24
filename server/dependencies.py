from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .auth import decode_access_token
from .models import User, RoleEnum
from .schemas import TokenData
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    
    # Super Admin bypasses tenant isolation checks if needed, but normally still uses X-Tenant-ID context
    if token_data.role == RoleEnum.SUPER_ADMIN.value:
        return x_tenant_id
        
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is missing")
        
    if x_tenant_id not in token_data.tenant_ids:
        raise HTTPException(status_code=403, detail="You do not have access to this workspace")
        
    # Store tenant_id in request state for downstream use
    request.state.tenant_id = x_tenant_id
    return x_tenant_id
