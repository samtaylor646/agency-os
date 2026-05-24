from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from ..database import get_db
from .. import models, dependencies

router = APIRouter(prefix="/analytics", tags=["analytics"])

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
