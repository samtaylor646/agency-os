from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from ..dependencies import get_api_or_user_tenant_context
from ..services.sandbox import sandbox_env

router = APIRouter(
    prefix="/api/v1/sandbox",
    tags=["Sandbox"],
    responses={401: {"description": "Unauthorized"}}
)

class SandboxExecuteRequest(BaseModel):
    code: str

class SandboxExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int

@router.post("/execute", response_model=SandboxExecuteResponse)
async def execute_code(
    request: SandboxExecuteRequest,
    tenant_id: int = Depends(get_api_or_user_tenant_context)
):
    """
    Executes untrusted agent code in a secure sandbox.
    """
    if not request.code:
        raise HTTPException(status_code=400, detail="Code string cannot be empty")
        
    try:
        result = sandbox_env.execute_script(request.code)
        return SandboxExecuteResponse(
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            exit_code=result.get("exit_code", -1)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sandbox execution failed: {str(e)}")
