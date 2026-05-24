from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, dependencies
from pydantic import BaseModel

router = APIRouter(prefix="/rbac", tags=["rbac"])

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
