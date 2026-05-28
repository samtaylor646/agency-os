from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, dependencies
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/marketplace", tags=["marketplace"])

class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    template_type: str
    content: Dict[str, Any]
    version: str = "1.0.0"

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
    db: Session = Depends(get_db)
):
    query = db.query(models.Template)
    if template_type:
        query = query.filter(models.Template.template_type == template_type)
    return query.all()

@router.get("/templates/{template_id}", response_model=TemplateOut)
def get_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.post("/templates", response_model=TemplateOut)
def create_template(
    template_in: TemplateCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    template = models.Template(**template_in.dict())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

@router.post("/templates/{id}/clone", response_model=TemplateOut)
def clone_template(
    id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    template = db.query(models.Template).filter(models.Template.id == id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    new_template = models.Template(
        name=f"Fork of {template.name}",
        description=template.description,
        template_type=template.template_type,
        content=template.content,
        version=template.version
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@router.delete("/templates/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    template = db.query(models.Template).filter(models.Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(template)
    db.commit()
    return {"status": "deleted"}
