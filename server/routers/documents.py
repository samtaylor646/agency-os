from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, dependencies
from ..services import document_parser, analysis_agent
import os
import uuid
import shutil

router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/documents",
    tags=["documents"],
)

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_document_pipeline(doc_id: str, storage_path: str, file_type: str, workspace_id: int):
    from ..database import SessionLocal
    db = SessionLocal()
    try:
        doc = db.query(models.IngestedDocument).filter(models.IngestedDocument.id == doc_id).first()
        if not doc:
            return
        doc.status = "analyzing"
        db.commit()
        
        extracted_text = document_parser.extract_text(storage_path, file_type)
        pipeline_data = await analysis_agent.generate_pipeline(extracted_text, workspace_id)
        
        # Save parsed pipeline to DB logic will go here
        
        doc.status = "completed"
        db.commit()
        
    except Exception as e:
        doc = db.query(models.IngestedDocument).filter(models.IngestedDocument.id == doc_id).first()
        if doc:
            doc.status = "failed"
            db.commit()
        print(f"Pipeline error: {e}")
    finally:
        db.close()


@router.post("/ingest", response_model=dict)
async def ingest_document(
    workspace_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    if tenant_id != workspace_id:
        raise HTTPException(status_code=403, detail="Forbidden: Workspace mismatch")
        
    allowed_types = ["application/pdf", "text/markdown", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    if file.content_type not in allowed_types and not file.filename.lower().endswith(('.pdf', '.md', '.txt', '.docx')):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    storage_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    
    with open(storage_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_type = "txt"
    if file.filename.lower().endswith('.pdf'): file_type = "pdf"
    elif file.filename.lower().endswith('.md'): file_type = "md"
    elif file.filename.lower().endswith('.docx'): file_type = "docx"

    doc = models.IngestedDocument(
        id=file_id,
        workspace_id=workspace_id,
        filename=file.filename,
        file_type=file_type,
        storage_path=storage_path,
        status="pending"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    background_tasks.add_task(
        process_document_pipeline, doc.id, storage_path, file_type, workspace_id
    )
    
    return {"message": "Document ingested successfully", "job_id": doc.id, "status": "pending"}


@router.get("/ingest/status/{job_id}")
def get_ingest_status(
    workspace_id: int,
    job_id: str,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    if tenant_id != workspace_id:
        raise HTTPException(status_code=403, detail="Forbidden: Workspace mismatch")
        
    doc = db.query(models.IngestedDocument).filter(
        models.IngestedDocument.id == job_id,
        models.IngestedDocument.workspace_id == workspace_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return {"job_id": doc.id, "status": doc.status}