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
    encrypted_dek: Optional[str] = None

    class Config:
        from_attributes = True

class CredentialBase(BaseModel):
    provider: str

class CredentialCreate(CredentialBase):
    key: str

class CredentialUpdate(BaseModel):
    key: str

class CredentialOut(CredentialBase):
    id: int
    tenant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    masked_key: str

    class Config:
        from_attributes = True

class APIKeyCreate(BaseModel):
    name: str
    expires_in_days: Optional[int] = None

class APIKeyOut(BaseModel):
    id: int
    name: str
    prefix: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: int

    class Config:
        from_attributes = True

class APIKeyCreateOut(APIKeyOut):
    key: str # The full plain-text key (only shown once)

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

class WorkflowNode(BaseModel):
    node_id: str
    agent_name: str
    task: str
    required_inputs: Optional[List[str]] = []

class WorkflowEdge(BaseModel):
    from_node: str
    to_node: str

class WorkflowRunRequest(BaseModel):
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]

class WebhookPayload(BaseModel):
    event_type: str
    data: Dict[str, Any]
    timestamp: Optional[datetime] = None
