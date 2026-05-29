from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
import sys
from datetime import datetime

try:
    from server.database import SessionLocal
    from server.models import WorkflowExecution
except ImportError:
    SessionLocal = None
    WorkflowExecution = None

class WorkflowState(BaseModel):
    """Represents the state of a workflow in the system."""
    workflow_id: str
    status: str = Field(default="pending", description="Current status: pending, running, completed, failed, paused, awaiting_approval")
    context: Dict[str, Any] = Field(default_factory=dict, description="State variables and context")
    error: Optional[str] = None

class StateManagerBase(ABC):
    """Abstract base class for state management."""

    @abstractmethod
    def load_state(self, workflow_id: str) -> Dict[str, Any]:
        """Retrieve the current state of a workflow."""
        pass

    @abstractmethod
    def save_state(self, workflow_id: str, tenant_id: str, workflow_name: str, status: str, state: Dict[str, Any]) -> None:
        """Set or completely override the state of a workflow."""
        pass

    @abstractmethod
    def inject_intervention(self, workflow_id: str, intervention_text: str) -> bool:
        """Inject human intervention text into the workflow context."""
        pass

class StateManager(StateManagerBase):
    """Concrete implementation for state management connected to DB."""
    
    def load_state(self, workflow_id: str) -> Dict[str, Any]:
        if not SessionLocal or not WorkflowExecution:
            return {}
            
        db = SessionLocal()
        try:
            exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
            if exec_record and exec_record.execution_context:
                return exec_record.execution_context
            return {}
        except Exception as e:
            print(f"Failed to load workflow state: {e}")
            return {}
        finally:
            db.close()

    def save_state(self, workflow_id: str, tenant_id: str, workflow_name: str, status: str, state: Dict[str, Any]) -> None:
        if not SessionLocal or not WorkflowExecution:
            return
            
        db = SessionLocal()
        try:
            completed_nodes = []
            failed_nodes = []
            for node_id, data in state.items():
                if data.get("status") == "success":
                    completed_nodes.append(node_id)
                elif data.get("status") in ["failed", "skipped"]:
                    failed_nodes.append(node_id)

            exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
            if not exec_record:
                exec_record = WorkflowExecution(
                    id=workflow_id,
                    tenant_id=int(tenant_id),
                    pipeline_id=workflow_name,
                    status=status,
                    completed_nodes=completed_nodes,
                    failed_nodes=failed_nodes,
                    execution_context=state,
                    retry_counts={}
                )
                db.add(exec_record)
            else:
                exec_record.status = status
                exec_record.completed_nodes = completed_nodes
                exec_record.failed_nodes = failed_nodes
                exec_record.execution_context = state
            db.commit()
        except Exception as e:
            print(f"Failed to save workflow state: {e}")
        finally:
            db.close()

    def inject_intervention(self, workflow_id: str, intervention_text: str) -> bool:
        """Inject human intervention text into the workflow context."""
        if not SessionLocal or not WorkflowExecution:
            return False
            
        db = SessionLocal()
        try:
            exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
            if not exec_record:
                return False
                
            context = exec_record.execution_context or {}
            
            # Append intervention text
            interventions = context.get("human_interventions", [])
            interventions.append({
                "text": intervention_text,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending_injection"
            })
            context["human_interventions"] = interventions
            
            exec_record.execution_context = context
            db.commit()
            return True
        except Exception as e:
            print(f"Failed to inject intervention: {e}")
            return False
        finally:
            db.close()
