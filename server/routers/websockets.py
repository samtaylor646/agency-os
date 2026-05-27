from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
import asyncio
from server.services.message_broker import message_broker

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ws",
    tags=["websockets"]
)

@router.websocket("/{pod_id}")
async def websocket_endpoint(websocket: WebSocket, pod_id: str):
    await websocket.accept()
    logger.info(f"WebSocket connected for pod: {pod_id}")
    
    # We will use an asyncio Queue to pass messages from Redis listener to WebSocket
    queue = asyncio.Queue()
    
    async def redis_callback(message_data):
        await queue.put(message_data)
        
    # Subscribe to Redis for this pod
    await message_broker.subscribe(pod_id, redis_callback)
    
    try:
        # Task to forward messages from queue to WebSocket
        async def forward_messages():
            while True:
                message = await queue.get()
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to WebSocket: {e}")
                    break
                    
        forward_task = asyncio.create_task(forward_messages())
        
        # Keep connection open and handle incoming messages if any (optional)
        while True:
            data = await websocket.receive_text()
            # In MVP, client might not send much back, but we handle it
            logger.debug(f"Received message from client {pod_id}: {data}")
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for pod: {pod_id}")
    except Exception as e:
        logger.error(f"WebSocket error for pod {pod_id}: {e}")
    finally:
        # Cleanup
        if 'forward_task' in locals():
            forward_task.cancel()
        # In a full implementation, you'd unsubscribe, but `message_broker.subscribe`
        # spins up an infinite listener loop. For MVP, we might leak listeners if not handled properly.
        # But this fits the current message_broker design.
