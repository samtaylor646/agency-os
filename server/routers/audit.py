from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from .. import models, dependencies

router = APIRouter(prefix="/api/v1/workspaces/audit-logs", tags=["audit"])

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
    writer.writerow(["id", "user_id", "workspace_id", "action", "resource", "details", "ip_address", "created_at"])
    
    for log in logs:
        writer.writerow([log.id, log.user_id, log.workspace_id, log.action, log.resource, log.details, log.ip_address, log.created_at])
        
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=audit_logs_export.csv"
    return response
