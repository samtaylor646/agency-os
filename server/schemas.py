from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from .models import RoleEnum

class WorkspaceBase(BaseModel):
    name: str
    settings_json: Optional[Dict[str, Any]] = {}

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceOut(WorkspaceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    tenant_id: Optional[int]

    class Config:
        from_attributes = True

class WorkspaceInvite(BaseModel):
    email: EmailStr
    role: RoleEnum = RoleEnum.CLIENT_READ_ONLY

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    tenant_ids: List[int] = []
