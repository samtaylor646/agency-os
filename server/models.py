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

    members = relationship("WorkspaceMember", back_populates="workspace")


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
