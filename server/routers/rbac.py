from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, dependencies
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
