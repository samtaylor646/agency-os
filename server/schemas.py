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

class DAGNodeInput(BaseModel):
    task: str
    context_data: Dict[str, Any] = {}
    tenant_id: str

class DAGNodeOutput(BaseModel):
    node_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None

class WebhookPayload(BaseModel):
    event_type: str
    data: Dict[str, Any]
    timestamp: Optional[datetime] = None

class ChatScopeRequest(BaseModel):
    message: str

class ProjectScopeExtraction(BaseModel):
    name: str
    description: str
    tech_stack: List[str]
    raw_message: str

class ChatScopeResponse(BaseModel):
    extraction: ProjectScopeExtraction
    chat_response: str

class DocumentOut(BaseModel):
    id: int
    chat_id: Optional[int]
    title: str
    content: str
    type: str
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentGenerateRequest(BaseModel):
    doc_type: str
    context: Dict[str, Any]

class DocumentGenerateResponse(BaseModel):
    content: str
    doc_type: str

class DocumentRefineRequest(BaseModel):
    doc_type: str
    current_content: str
    feedback: str

class DocumentRefineResponse(BaseModel):
    content: str
    doc_type: str
    chat_response: str

class AgentIdentity(BaseModel):
    name: str
    role: str
    version: str

class AgentSystemRules(BaseModel):
    path: str
    enforcement_level: str



class Identity(BaseModel):
    name: str
    role: str
    domain: str = "specialized"
    base_model: str = "gpt-4o"
    description: Optional[str] = ""
    color: Optional[str] = "blue"
    emoji: Optional[str] = "🤖"
    vibe: Optional[str] = ""
    intro_paragraph: Optional[str] = ""

class SystemRules(BaseModel):
    mission: Optional[str] = ""
    rules: Optional[str] = ""
    personality: Optional[str] = ""
    memory: Optional[str] = ""
    experience: Optional[str] = ""
    deliverables: Optional[str] = ""
    communication: Optional[str] = ""
    learning: Optional[str] = ""
    success_metrics: Optional[str] = ""
    advanced_capabilities: Optional[str] = ""
    instructions_reference: Optional[str] = ""

class CustomAgentCreate(BaseModel):
    identity: Identity
    system_rules: SystemRules
    capabilities: List[str] = []
    constraints: List[str] = []
    system_prompt: Optional[str] = ""

    class Config:
        extra = "forbid"


class CustomAgentOut(BaseModel):
    id: str
    name: str
    role: str
    filepath: str
    
    class Config:
        from_attributes = True
