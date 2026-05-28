from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
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
    resource_type: Optional[str]
    resource_id: Optional[str]
    details: Optional[Dict[str, Any]]
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

from fastapi import Response
import csv
from io import StringIO

@router.get("/export")
def export_audit_logs(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    logs = db.query(models.AuditLog).filter(
        models.AuditLog.workspace_id == tenant_id
    ).order_by(models.AuditLog.created_at.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "user_id", "workspace_id", "action", "resource_type", "resource_id", "details", "created_at"])
    
    for log in logs:
        writer.writerow([log.id, log.user_id, log.workspace_id, log.action, log.resource_type, log.resource_id, log.details, log.created_at])
        
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=audit_logs_export.csv"
    return response
