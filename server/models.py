from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    SUPER_ADMIN = "Super Admin"
    AGENCY_ADMIN = "Agency Admin"
    CLIENT_APPROVER = "Client Approver"
    CLIENT_READ_ONLY = "Client Read-Only"

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    settings_json = Column(JSON, default={})
    encrypted_dek = Column(String(255), nullable=True)

    members = relationship("WorkspaceMember", back_populates="workspace")
    credentials = relationship("Credential", back_populates="workspace")
    api_keys = relationship("WorkspaceAPIKey", back_populates="workspace")


class CredentialProvider(str, enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    # add others as needed

class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    provider = Column(String(255), nullable=False)
    encrypted_key = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    workspace = relationship("Workspace", back_populates="credentials")


class WorkspaceAPIKey(Base):
    __tablename__ = "workspace_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String(255), nullable=False)
    prefix = Column(String(255), nullable=False) # e.g. ak_1234
    hashed_key = Column(String(255), nullable=False) # store hashed full key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Integer, default=1) # 1 for active, 0 for revoked

    workspace = relationship("Workspace", back_populates="api_keys")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # The specification mentions Users should include a tenant_id. 
    # For a multi-tenant system where users can belong to multiple workspaces, 
    # we typically use a junction table (WorkspaceMember). 
    # We include tenant_id here to represent the default or primary workspace if needed, 
    # but the authorized `tenant_ids` will be derived from WorkspaceMember.
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)

    memberships = relationship("WorkspaceMember", back_populates="user")


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(255), default=RoleEnum.CLIENT_READ_ONLY.value)
    
    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="memberships")


class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    description = Column(String(255), nullable=True)


class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)


class WorkspaceMemberRole(Base):
    __tablename__ = "workspace_member_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_member_id = Column(Integer, ForeignKey("workspace_members.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(255), nullable=False)
    resource_type = Column(String(255), nullable=True)
    resource_id = Column(String(255), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgentExecutionMetric(Base):
    __tablename__ = "agent_execution_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    agent_name = Column(String(255), nullable=False)
    execution_duration_ms = Column(Integer, nullable=False)
    tokens_used = Column(Integer, nullable=False, default=0)
    status = Column(String(255), nullable=False)
    error_message = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    template_type = Column(String(255), nullable=False) # e.g. "agent", "workflow"
    content = Column(JSON, nullable=False)
    version = Column(String(255), nullable=False, default="1.0.0")
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class IngestedDocument(Base):
    __tablename__ = "ingested_documents"
    id = Column(String(255), primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    storage_path = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True, nullable=True) # or pipeline_run_id
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CustomAgent(Base):
    __tablename__ = "custom_agents"
    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    filepath = Column(String(255), unique=True, nullable=False)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Example of other core entities with tenant_id for Logical Isolation
class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=False)
    status = Column(String(50), default="RUNNING") # RUNNING, WAITING_APPROVAL, ERROR, COMPLETED, REJECTED
    state = Column(JSON, default={})
    error_message = Column(String(255), nullable=True)

class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(String(255), primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    workflow_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="PENDING") # PENDING, RUNNING, PAUSED, COMPLETED, FAILED, PARTIAL_FAILURE
    state_data = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PipelineMessage(Base):
    __tablename__ = "pipeline_messages"
    id = Column(Integer, primary_key=True, index=True)
    pipeline_run_id = Column(Integer, ForeignKey("pipeline_runs.id"), nullable=False)
    role = Column(String(50), nullable=False) # user, agent, system
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
