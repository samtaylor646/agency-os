from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, status, Request
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, dependencies
from ..services import document_parser, analysis_agent, semantic_search
import os
import uuid
import shutil

router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/documents",
    tags=["documents"],
)

UPLOAD_DIR = "uploads/"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB Payload size limit
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_document_pipeline(doc_id: str, storage_path: str, file_type: str, workspace_id: int):
    from ..database import SessionLocal
    from ..embeddings import get_embedding_provider
    db = SessionLocal()
    try:
        doc = db.query(models.IngestedDocument).filter(models.IngestedDocument.id == doc_id).first()
        if not doc:
            return
        doc.status = "analyzing"
        db.commit()
        
        extracted_text = document_parser.extract_text(storage_path, file_type)
        
        # Semantic Memory Spec Task 1 & 2: Chunking & Embeddings
        chunks = document_parser.chunk_text(extracted_text, chunk_size=500, overlap=50)
        
        provider = get_embedding_provider()
        
        # Create a parent Document record for RAG
        rag_doc = models.Document(
            title=doc.filename,
            content=extracted_text,
            type=file_type,
            # chat_id or other fields could go here if needed
        )
        db.add(rag_doc)
        db.commit()
        db.refresh(rag_doc)

        if chunks:
            # Batch process embeddings for all chunks
            embeddings = await provider.get_embeddings(chunks)
            
            # Save chunks to DB
            for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_record = models.DocumentChunk(
                    document_id=rag_doc.id,
                    workspace_id=workspace_id,
                    chunk_index=idx,
                    text_content=chunk_text,
                    embedding=embedding
                )
                db.add(chunk_record)
            
            db.commit()
        
        # The legacy pipeline generation if needed (leaving intact for now)
        try:
            pipeline_data = await analysis_agent.generate_pipeline(extracted_text, workspace_id)
        except Exception as e:
            print(f"Legacy analysis pipeline error: {e}")
            
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


@router.post("/ingest", response_model=dict, dependencies=[Depends(dependencies.rate_limit_ingestion)])
async def ingest_document(
    workspace_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.verify_workspace_access)
):
    # Enforce payload size limit
    if request.headers.get('content-length'):
        content_length = int(request.headers.get('content-length'))
        if content_length > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Payload Too Large. Max file size is 5MB.")

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


@router.get("/search")
async def search_workspace_documents(
    workspace_id: int,
    query: str,
    top_k: int = 5,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.verify_workspace_access)
):
    """
    Retrieves semantically similar document chunks for a given query.
    Enforces RBAC explicit read/write access to the workspace.
    """
    results = await semantic_search.search_documents(db, workspace_id, query, top_k)
    return {"results": results}

@router.get("/ingest/status/{job_id}")
def get_ingest_status(
    workspace_id: int,
    job_id: str,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.verify_workspace_access)
):
    doc = db.query(models.IngestedDocument).filter(
        models.IngestedDocument.id == job_id,
        models.IngestedDocument.workspace_id == workspace_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return {"job_id": doc.id, "status": doc.status}
