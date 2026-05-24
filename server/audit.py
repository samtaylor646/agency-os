from typing import Optional
from sqlalchemy.orm import Session
from . import models

def log_audit_event(
    db: Session,
    workspace_id: int,
    action: str,
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None
):
    audit_log = models.AuditLog(
        workspace_id=workspace_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log
