from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies, models
from ..services.llm_runner import llm_runner

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
    dependencies=[Depends(dependencies.get_current_user)]
)

@router.post("", response_model=schemas.ChatOut, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat: schemas.ChatCreate,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    db_chat = models.Chat(
        **chat.model_dump(),
        workspace_id=workspace.id
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.get("", response_model=List[schemas.ChatOut])
async def get_chats(
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    chats = db.query(models.Chat).filter(models.Chat.workspace_id == workspace.id).all()
    return chats

@router.get("/{chat_id}", response_model=schemas.ChatWithMessagesOut)
async def get_chat(
    chat_id: int,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    chat = db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.workspace_id == workspace.id
    ).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/{chat_id}/messages", response_model=schemas.ChatMessageOut)
async def add_chat_message(
    chat_id: int,
    message: schemas.ChatMessageCreate,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    chat = db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.workspace_id == workspace.id
    ).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
        
    db_message = models.ChatMessage(
        chat_id=chat_id,
        role=message.role,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    workspace: models.Workspace = Depends(dependencies.get_current_workspace),
    db: Session = Depends(dependencies.get_db)
):
    chat = db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.workspace_id == workspace.id
    ).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
        
    db.delete(chat)
    db.commit()
    return None

@router.post("/scope", response_model=schemas.ChatScopeResponse)
async def chat_scope(request: schemas.ChatScopeRequest):
    """
    Takes a user message, passes it to the LLM runner, and returns a 
    structured extraction of core project details alongside a chat response.
    """
    try:
        # Parse intent to extract project details
        extraction_data = await llm_runner.parse_intent(request.message)
        
        # Generate a conversational response
        chat_response = await llm_runner.generate_response(
            prompt=request.message,
            system_prompt="You are an AI assistant helping to scope a new software project."
        )
        
        extraction = schemas.ProjectScopeExtraction(**extraction_data)
        
        return schemas.ChatScopeResponse(
            extraction=extraction,
            chat_response=chat_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat scope: {str(e)}"
        )

@router.post("/{chat_id}/generate/{doc_type}", response_model=schemas.DocumentOut)
async def generate_document_new(chat_id: int, doc_type: str, request: schemas.DocumentGenerateRequest, db: Session = Depends(dependencies.get_db)):
    """
    Generates a specific project document (PRD, architecture, tasks) 
    based on the provided project context, and saves it to the db.
    """
    try:
        content = await llm_runner.generate_document(
            doc_type=doc_type,
            context=request.context
        )
        
        doc = models.Document(
            chat_id=chat_id,
            title=f"Generated {doc_type}",
            content=content,
            type=doc_type
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        return doc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate document: {str(e)}"
        )

@router.post("/{chat_id}/documents/upload", response_model=schemas.ChatScopeResponse)
async def ingest_document(chat_id: int, file: UploadFile = File(...)):
    """
    Ingests an existing document (e.g. PRD, spec) to automatically seed the extraction context.
    """
    try:
        content = await file.read()
        extraction_data = await llm_runner.ingest_document(content, file.filename)
        
        extraction = schemas.ProjectScopeExtraction(**extraction_data)
        
        return schemas.ChatScopeResponse(
            extraction=extraction,
            chat_response=f"Successfully ingested {file.filename} and extracted project context."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest document: {str(e)}"
        )

@router.post("/refine", response_model=schemas.DocumentRefineResponse)
async def refine_document(request: schemas.DocumentRefineRequest):
    """
    Iterative refinement loop: updates a document based on natural language feedback.
    """
    try:
        result = await llm_runner.refine_document(
            doc_type=request.doc_type,
            current_content=request.current_content,
            feedback=request.feedback
        )
        return schemas.DocumentRefineResponse(
            content=result["content"],
            doc_type=request.doc_type,
            chat_response=result["chat_response"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refine document: {str(e)}"
        )
