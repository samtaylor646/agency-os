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
    name = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    settings_json = Column(JSON, default={})
    encrypted_dek = Column(String, nullable=True)

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
    provider = Column(String, nullable=False)
    encrypted_key = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    workspace = relationship("Workspace", back_populates="credentials")


class WorkspaceAPIKey(Base):
    __tablename__ = "workspace_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    prefix = Column(String, nullable=False) # e.g. ak_1234
    hashed_key = Column(String, nullable=False) # store hashed full key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Integer, default=1) # 1 for active, 0 for revoked

    workspace = relationship("Workspace", back_populates="api_keys")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
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
    role = Column(String, default=RoleEnum.CLIENT_READ_ONLY.value)
    
    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="memberships")


# Example of other core entities with tenant_id for Logical Isolation
class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tenant_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
