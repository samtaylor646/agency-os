from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
import csv
from io import StringIO
from ..database import get_db
from .. import models, dependencies

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

@router.get("/metrics/execution")
def get_execution_metrics(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    """Get aggregated metrics for agent executions."""
    # Example simple aggregation
    total_executions = db.query(func.count(models.AgentExecutionMetric.id)).filter(
        models.AgentExecutionMetric.workspace_id == tenant_id
    ).scalar()
    
    total_tokens = db.query(func.sum(models.AgentExecutionMetric.tokens_used)).filter(
        models.AgentExecutionMetric.workspace_id == tenant_id
    ).scalar() or 0
    
    avg_duration = db.query(func.avg(models.AgentExecutionMetric.execution_duration_ms)).filter(
        models.AgentExecutionMetric.workspace_id == tenant_id
    ).scalar() or 0.0

    success_count = db.query(func.count(models.AgentExecutionMetric.id)).filter(
        models.AgentExecutionMetric.workspace_id == tenant_id,
        models.AgentExecutionMetric.status == "success"
    ).scalar() or 0

    return {
        "total_executions": total_executions,
        "total_tokens": total_tokens,
        "avg_duration_ms": avg_duration,
        "success_rate": (success_count / total_executions) if total_executions > 0 else 0
    }

@router.get("/metrics/agent/{agent_name}")
def get_agent_metrics(
    agent_name: str,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    metrics = db.query(models.AgentExecutionMetric).filter(
        models.AgentExecutionMetric.workspace_id == tenant_id,
        models.AgentExecutionMetric.agent_name == agent_name
    ).order_by(models.AgentExecutionMetric.created_at.desc()).limit(100).all()
    return metrics

@router.get("/export")
def export_analytics(
    format: str = "csv",
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_tenant_context)
):
    if format != "csv":
        raise HTTPException(status_code=400, detail="Unsupported format")
        
    metrics = db.query(models.AgentExecutionMetric).filter(
        models.AgentExecutionMetric.workspace_id == tenant_id
    ).order_by(models.AgentExecutionMetric.created_at.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "agent_name", "execution_duration_ms", "tokens_used", "status", "created_at"])
    
    for m in metrics:
        writer.writerow([m.id, m.agent_name, m.execution_duration_ms, m.tokens_used, m.status, m.created_at])
        
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=analytics_export.csv"
    return response
