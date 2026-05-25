from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, dependencies
from ..services.llm_runner import llm_runner

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
    dependencies=[Depends(dependencies.get_current_user)]
)

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
