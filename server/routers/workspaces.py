from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import get_db
from ..dependencies import get_current_user, get_tenant_context, require_role

router = APIRouter(
    prefix="/api/v1/workspaces",
    tags=["workspaces"]
)

@router.post("", response_model=schemas.WorkspaceOut, status_code=status.HTTP_201_CREATED)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(get_db), user_data: tuple = Depends(get_current_user)):
    user, token_data = user_data
    
    # Check if user has permission to create workspaces (e.g. Agency Admin or Super Admin)
    # Using simple role check for demonstration.
    if token_data.role not in [models.RoleEnum.SUPER_ADMIN.value, models.RoleEnum.AGENCY_ADMIN.value]:
        raise HTTPException(status_code=403, detail="Not authorized to create workspaces")
        
    db_workspace = models.Workspace(name=workspace.name, settings_json=workspace.settings_json)
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    
    # Automatically add the creator as Agency Admin for this new workspace
    db_member = models.WorkspaceMember(
        workspace_id=db_workspace.id,
        user_id=user.id,
        role=models.RoleEnum.AGENCY_ADMIN.value
    )
    db.add(db_member)
    db.commit()
    
    return db_workspace

@router.get("", response_model=List[schemas.WorkspaceOut])
def list_workspaces(db: Session = Depends(get_db), user_data: tuple = Depends(get_current_user)):
    user, token_data = user_data
    
    if token_data.role == models.RoleEnum.SUPER_ADMIN.value:
        workspaces = db.query(models.Workspace).all()
        return workspaces
        
    # List only workspaces the user has access to
    memberships = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id).all()
    workspace_ids = [m.workspace_id for m in memberships]
    
    workspaces = db.query(models.Workspace).filter(models.Workspace.id.in_(workspace_ids)).all()
    return workspaces

@router.post("/{workspace_id}/invites", status_code=status.HTTP_200_OK)
def invite_user(
    workspace_id: int, 
    invite: schemas.WorkspaceInvite, 
    db: Session = Depends(get_db), 
    tenant_id: int = Depends(get_tenant_context)
):
    # The tenant_context dependency already ensures the user has access to X-Tenant-ID
    # We must also ensure X-Tenant-ID matches the URL path for security (No IDOR)
    if workspace_id != tenant_id:
        raise HTTPException(status_code=403, detail="Workspace ID mismatch with Tenant Context")
        
    # Here we would typically generate an invitation token and send an email
    # For MVP, we simulate sending the invite.
    # Check if user already exists
    invited_user = db.query(models.User).filter(models.User.email == invite.email).first()
    
    if invited_user:
        # Check if already a member
        existing_member = db.query(models.WorkspaceMember).filter(
            models.WorkspaceMember.workspace_id == workspace_id,
            models.WorkspaceMember.user_id == invited_user.id
        ).first()
        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member of this workspace")
            
        # Add them immediately for MVP simplification
        new_member = models.WorkspaceMember(
            workspace_id=workspace_id,
            user_id=invited_user.id,
            role=invite.role.value
        )
        db.add(new_member)
        db.commit()
        return {"msg": f"User {invite.email} added to workspace directly."}
    else:
        # User doesn't exist. We would send an email with a signup link.
        return {"msg": f"Invitation email sent to {invite.email} for role {invite.role.value}."}
