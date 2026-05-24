from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, dependencies
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/marketplace", tags=["marketplace"])

class TemplateOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    template_type: str
    content: Dict[str, Any]
    version: str

    class Config:
        from_attributes = True

@router.get("/templates", response_model=List[TemplateOut])
def list_templates(
    template_type: Optional[str] = None,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    query = db.query(models.Template)
    if template_type:
        query = query.filter(models.Template.template_type == template_type)
    return query.all()

@router.get("/templates/{template_id}", response_model=TemplateOut)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template
