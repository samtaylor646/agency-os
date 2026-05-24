from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from .. import models, dependencies

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])

class AuditLogOut(BaseModel):
    id: int
    user_id: Optional[int]
    workspace_id: int
    action: str
    resource: str
    details: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("", response_model=List[AuditLogOut])
def get_audit_logs(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    logs = db.query(models.AuditLog).filter(
        models.AuditLog.workspace_id == tenant_id
    ).order_by(models.AuditLog.created_at.desc()).offset(offset).limit(limit).all()
    return logs
