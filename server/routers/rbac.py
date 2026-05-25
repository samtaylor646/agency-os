from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from ..database import get_db
from .. import models, schemas, dependencies, auth
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/rbac", tags=["rbac"])

class PermissionOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

class RoleOut(BaseModel):
    id: int
    name: str
    workspace_id: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class WorkspaceMemberOut(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: str
    email: str

    class Config:
        from_attributes = True

class UpdateMemberRole(BaseModel):
    role: str

@router.get("/permissions", response_model=List[PermissionOut])
def list_permissions(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    return db.query(models.Permission).all()

@router.get("/roles", response_model=List[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    return db.query(models.Role).filter((models.Role.workspace_id == tenant_id) | (models.Role.workspace_id == None)).all()

@router.post("/roles", response_model=RoleOut)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    new_role = models.Role(
        name=role_in.name,
        description=role_in.description,
        workspace_id=tenant_id
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.put("/roles/{role_id}", response_model=RoleOut)
def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    db_role = db.query(models.Role).filter(
        models.Role.id == role_id,
        models.Role.workspace_id == tenant_id
    ).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    if role_in.name is not None:
        db_role.name = role_in.name
    if role_in.description is not None:
        db_role.description = role_in.description
        
    db.commit()
    db.refresh(db_role)
    return db_role

@router.post("/invite", response_model=WorkspaceMemberOut)
def invite_user(
    invite_data: schemas.WorkspaceInvite,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    user = db.query(models.User).filter(models.User.email == invite_data.email).first()
    if not user:
        # Create dummy user if doesn't exist
        temp_password = str(uuid.uuid4())
        hashed_pw = auth.get_password_hash(temp_password)
        user = models.User(email=invite_data.email, hashed_password=hashed_pw, tenant_id=tenant_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        
    # Check if already member
    member = db.query(models.WorkspaceMember).filter(
        models.WorkspaceMember.workspace_id == tenant_id,
        models.WorkspaceMember.user_id == user.id
    ).first()
    
    if member:
        raise HTTPException(status_code=400, detail="User is already a member of this workspace")
        
    new_member = models.WorkspaceMember(
        workspace_id=tenant_id,
        user_id=user.id,
        role=invite_data.role.value
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return WorkspaceMemberOut(
        id=new_member.id,
        workspace_id=new_member.workspace_id,
        user_id=new_member.user_id,
        role=new_member.role,
        email=user.email
    )

@router.get("/members", response_model=List[WorkspaceMemberOut])
def list_members(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    members = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.workspace_id == tenant_id).all()
    out = []
    for m in members:
        out.append(WorkspaceMemberOut(
            id=m.id,
            workspace_id=m.workspace_id,
            user_id=m.user_id,
            role=m.role,
            email=m.user.email
        ))
    return out

@router.put("/members/{member_id}/role", response_model=WorkspaceMemberOut)
def update_member_role(
    member_id: int,
    role_update: UpdateMemberRole,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    member = db.query(models.WorkspaceMember).filter(
        models.WorkspaceMember.id == member_id,
        models.WorkspaceMember.workspace_id == tenant_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Workspace member not found")
        
    member.role = role_update.role
    db.commit()
    db.refresh(member)
    
    return WorkspaceMemberOut(
        id=member.id,
        workspace_id=member.workspace_id,
        user_id=member.user_id,
        role=member.role,
        email=member.user.email
    )
