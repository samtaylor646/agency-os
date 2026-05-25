from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json

from ..database import get_db
from ..models import Pipeline, PipelineRun, PipelineMessage

router = APIRouter(prefix="/pipelines", tags=["pipelines"])

class PipelineRunResponse(BaseModel):
    id: int
    pipeline_id: int
    status: str
    error_message: Optional[str] = None

    class Config:
        orm_mode = True

class ApprovalRequest(BaseModel):
    action: str # "approve" or "reject"
    comments: Optional[str] = None

@router.post("/{pipeline_id}/run", response_model=PipelineRunResponse)
def start_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    run = PipelineRun(pipeline_id=pipeline_id, status="RUNNING")
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

@router.post("/runs/{run_id}/pause", response_model=PipelineRunResponse)
def pause_pipeline_for_approval(run_id: int, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run.status = "WAITING_APPROVAL"
    db.commit()
    db.refresh(run)
    return run

@router.post("/runs/{run_id}/approve", response_model=PipelineRunResponse)
def approve_pipeline(run_id: int, request: ApprovalRequest, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if run.status != "WAITING_APPROVAL":
        raise HTTPException(status_code=400, detail="Run is not waiting for approval")
        
    if request.action == "approve":
        run.status = "RUNNING"
    elif request.action == "reject":
        run.status = "REJECTED"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
        
    db.commit()
    db.refresh(run)
    return run

@router.post("/runs/{run_id}/error", response_model=PipelineRunResponse)
def escalate_pipeline_error(run_id: int, error_message: str, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run.status = "ERROR"
    run.error_message = error_message
    db.commit()
    db.refresh(run)
    return run

@router.post("/runs/{run_id}/chat")
def post_chat_message(run_id: int, role: str, content: str, db: Session = Depends(get_db)):
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
        
    msg = PipelineMessage(pipeline_run_id=run_id, role=role, content=content)
    db.add(msg)
    db.commit()
    return {"status": "ok"}

@router.websocket("/runs/{run_id}/ws")
async def websocket_chat(websocket: WebSocket, run_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        await websocket.close(code=1008)
        return
        
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            msg = PipelineMessage(pipeline_run_id=run_id, role=payload.get("role", "user"), content=payload.get("content", ""))
            db.add(msg)
            db.commit()
            
            # echo back
            await websocket.send_text(json.dumps({"status": "received", "content": payload.get("content")}))
    except WebSocketDisconnect:
        pass

