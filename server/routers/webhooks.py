from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..schemas import WebhookPayload
import logging

router = APIRouter(
    prefix="/api/v1/webhooks",
    tags=["webhooks"]
)

logger = logging.getLogger(__name__)

# A simple in-memory queue to simulate RabbitMQ/Redis for MVP
webhook_queue = []

@router.post("/{tenant_id}/{webhook_id}", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(
    tenant_id: int, 
    webhook_id: str, 
    payload: WebhookPayload,
    # Depending on requirements, we might want some auth here, but typically webhooks 
    # from third parties don't use our user auth, they might use a signature. 
    # For MVP, we'll just accept it.
):
    """
    Inbound webhook endpoint.
    Validates payload and pushes to a local queue.
    """
    logger.info(f"Received webhook for tenant {tenant_id}, webhook_id {webhook_id}: {payload.event_type}")
    
    # Store in our mock queue
    queue_item = {
        "tenant_id": tenant_id,
        "webhook_id": webhook_id,
        "payload": payload.model_dump()
    }
    webhook_queue.append(queue_item)
    
    return {"message": "Webhook received successfully", "status": "queued"}
