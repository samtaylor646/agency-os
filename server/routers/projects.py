from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies, models

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["projects"],
    dependencies=[Depends(dependencies.get_current_user)]
)

@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: schemas.ProjectCreate,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    db_project = models.Project(
        **project.model_dump(),
        workspace_id=workspace.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("", response_model=List[schemas.ProjectOut])
async def get_projects(
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    projects = db.query(models.Project).filter(models.Project.workspace_id == workspace.id).all()
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectOut)
async def get_project(
    project_id: int,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.workspace_id == workspace.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=schemas.ProjectOut)
async def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.workspace_id == workspace.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
        
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.workspace_id == workspace.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    db.delete(project)
    db.commit()
    return None
