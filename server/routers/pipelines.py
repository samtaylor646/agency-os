from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional
import json

from ..database import get_db
from .. import dependencies
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
async def start_pipeline(pipeline_id: int, db: AsyncSession = Depends(dependencies.get_async_db)):
    pipeline = (await db.execute(select(Pipeline).filter(Pipeline.id == pipeline_id))).scalars().first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    run = PipelineRun(pipeline_id=pipeline_id, status="RUNNING")
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run

@router.post("/runs/{run_id}/pause", response_model=PipelineRunResponse)
async def pause_pipeline_for_approval(run_id: int, db: AsyncSession = Depends(dependencies.get_async_db)):
    run = (await db.execute(select(PipelineRun).filter(PipelineRun.id == run_id))).scalars().first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run.status = "WAITING_APPROVAL"
    await db.commit()
    await db.refresh(run)
    return run

@router.post("/runs/{run_id}/approve", response_model=PipelineRunResponse)
async def approve_pipeline(run_id: int, request: ApprovalRequest, db: AsyncSession = Depends(dependencies.get_async_db)):
    run = (await db.execute(select(PipelineRun).filter(PipelineRun.id == run_id))).scalars().first()
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
        
    await db.commit()
    await db.refresh(run)
    return run

@router.post("/runs/{run_id}/error", response_model=PipelineRunResponse)
async def escalate_pipeline_error(run_id: int, error_message: str, db: AsyncSession = Depends(dependencies.get_async_db)):
    run = (await db.execute(select(PipelineRun).filter(PipelineRun.id == run_id))).scalars().first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    run.status = "ERROR"
    run.error_message = error_message
    await db.commit()
    await db.refresh(run)
    return run

@router.post("/runs/{run_id}/chat")
async def post_chat_message(run_id: int, role: str, content: str, db: AsyncSession = Depends(dependencies.get_async_db)):
    run = (await db.execute(select(PipelineRun).filter(PipelineRun.id == run_id))).scalars().first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
        
    msg = PipelineMessage(pipeline_run_id=run_id, role=role, content=content)
    db.add(msg)
    await db.commit()
    return {"status": "ok"}

@router.post("/runs/{run_id}/intervene")
async def inject_intervention_to_run(run_id: int, request: ApprovalRequest, db: AsyncSession = Depends(dependencies.get_async_db)):
    run = (await db.execute(select(PipelineRun).filter(PipelineRun.id == run_id))).scalars().first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
        
    # If the user sends comments as intervention
    intervention_text = request.comments or "Approved/Intervened"
    
    # Send intervention to state_manager
    from server.core.state_manager import StateManager
    sm = StateManager()
    success = sm.inject_intervention(str(run_id), intervention_text)
    
    # Emit intervention_received over message broker (which routes to WS)
    from server.services.message_broker import message_broker
    import asyncio
    
    if message_broker:
        try:
            # Get the tenant ID or use 'GLOBAL' if we don't have it here
            tenant_id = run.pipeline.workspace_id if hasattr(run.pipeline, 'workspace_id') else 'GLOBAL'
        except Exception:
            tenant_id = 'GLOBAL'
            
        # Using a background task or event loop to run async function
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(message_broker.publish(str(tenant_id), {
                "type": "intervention_received",
                "workflow_id": str(run_id),
                "text": intervention_text
            }))
        except RuntimeError:
            pass # No running event loop
            
    if not success:
        raise HTTPException(status_code=500, detail="Failed to inject intervention")
        
    return {"status": "intervention_injected"}

@router.websocket("/runs/{run_id}/ws")
async def websocket_chat(websocket: WebSocket, run_id: int, db: AsyncSession = Depends(dependencies.get_async_db)):
    await websocket.accept()
    run = (await db.execute(select(PipelineRun).filter(PipelineRun.id == run_id))).scalars().first()
    if not run:
        await websocket.close(code=1008)
        return
        
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            msg = PipelineMessage(pipeline_run_id=run_id, role=payload.get("role", "user"), content=payload.get("content", ""))
            db.add(msg)
            await db.commit()
            
            # echo back
            await websocket.send_text(json.dumps({"status": "received", "content": payload.get("content")}))
    except WebSocketDisconnect:
        pass

