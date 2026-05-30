from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from .. import schemas, models
from ..database import get_db
from ..dependencies import get_current_user, get_tenant_context, require_role, get_async_db

router = APIRouter(
    prefix="/api/v1/workspaces",
    tags=["workspaces"]
)

@router.post("", response_model=schemas.WorkspaceOut, status_code=status.HTTP_201_CREATED)
async def create_workspace(workspace: schemas.WorkspaceCreate, db: AsyncSession = Depends(get_async_db), user_data: tuple = Depends(get_current_user)):
    user, token_data = user_data
    
    # Check if user has permission to create workspaces (e.g. Agency Admin or Super Admin)
    # Using simple role check for demonstration.
    if token_data.role not in [models.RoleEnum.SUPER_ADMIN.value, models.RoleEnum.AGENCY_ADMIN.value]:
        raise HTTPException(status_code=403, detail="Not authorized to create workspaces")
        
    db_workspace = models.Workspace(name=workspace.name, settings_json=workspace.settings_json)
    db.add(db_workspace)
    await db.commit()
    await db.refresh(db_workspace)
    
    # Automatically add the creator as Agency Admin for this new workspace
    db_member = models.WorkspaceMember(
        workspace_id=db_workspace.id,
        user_id=user.id,
        role=models.RoleEnum.AGENCY_ADMIN.value
    )
    db.add(db_member)
    await db.commit()
    
    return db_workspace

@router.get("", response_model=List[schemas.WorkspaceOut])
async def list_workspaces(db: AsyncSession = Depends(get_async_db), user_data: tuple = Depends(get_current_user)):
    user, token_data = user_data
    
    if token_data.role == models.RoleEnum.SUPER_ADMIN.value:
        result = await db.execute(select(models.Workspace))
        return result.scalars().all()
        
    # List only workspaces the user has access to
    result = await db.execute(select(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id))
    memberships = result.scalars().all()
    workspace_ids = [m.workspace_id for m in memberships]
    
    result = await db.execute(select(models.Workspace).filter(models.Workspace.id.in_(workspace_ids)))
    return result.scalars().all()

@router.post("/{workspace_id}/invites", status_code=status.HTTP_200_OK)
async def invite_user(
    workspace_id: int, 
    invite: schemas.WorkspaceInvite, 
    db: AsyncSession = Depends(get_async_db), 
    tenant_id: int = Depends(get_tenant_context)
):
    # The tenant_context dependency already ensures the user has access to X-Tenant-ID
    # We must also ensure X-Tenant-ID matches the URL path for security (No IDOR)
    if workspace_id != tenant_id:
        raise HTTPException(status_code=403, detail="Workspace ID mismatch with Tenant Context")
        
    # Here we would typically generate an invitation token and send an email
    # For MVP, we simulate sending the invite.
    # Check if user already exists
    result = await db.execute(select(models.User).filter(models.User.email == invite.email))
    invited_user = result.scalars().first()
    
    if invited_user:
        # Check if already a member
        result = await db.execute(select(models.WorkspaceMember).filter(
            models.WorkspaceMember.workspace_id == workspace_id,
            models.WorkspaceMember.user_id == invited_user.id
        ))
        existing_member = result.scalars().first()
        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member of this workspace")
            
        # Add them immediately for MVP simplification
        new_member = models.WorkspaceMember(
            workspace_id=workspace_id,
            user_id=invited_user.id,
            role=invite.role.value
        )
        db.add(new_member)
        await db.commit()
        return {"msg": f"User {invite.email} added to workspace directly."}
    else:
        # User doesn't exist. We would send an email with a signup link.
        return {"msg": f"Invitation email sent to {invite.email} for role {invite.role.value}."}
