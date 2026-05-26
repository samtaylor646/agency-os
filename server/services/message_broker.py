import os
import json
import asyncio
import logging
from typing import Callable, Any, Dict, Optional
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class MessageBroker:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub = None

    async def connect(self):
        """Initialize Redis connection if it doesn't exist."""
        if not self.redis_client:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            self.pubsub = self.redis_client.pubsub()

    async def close(self):
        """Close the Redis connection and pubsub."""
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.aclose()

    async def publish(self, pod_id: str, message: Dict[str, Any]):
        """Publish a message to a specific pod's channel."""
        await self.connect()
        channel = f"pod:{pod_id}:messages"
        try:
            await self.redis_client.publish(channel, json.dumps(message))
            logger.debug(f"Published message to {channel}")
        except Exception as e:
            logger.error(f"Failed to publish message to {channel}: {e}")

    async def subscribe(self, pod_id: str, callback: Callable[[Dict[str, Any]], Any]):
        """Subscribe to a pod's channel and invoke the callback on new messages."""
        await self.connect()
        channel = f"pod:{pod_id}:messages"
        
        try:
            await self.pubsub.subscribe(channel)
            logger.debug(f"Subscribed to {channel}")
        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {e}")
            return
            
        async def listener():
            try:
                async for message in self.pubsub.listen():
                    if message["type"] == "message":
                        try:
                            data = json.loads(message["data"])
                            if asyncio.iscoroutinefunction(callback):
                                await callback(data)
                            else:
                                callback(data)
                        except json.JSONDecodeError:
                            logger.error("Failed to decode message data as JSON")
                        except Exception as e:
                            logger.error(f"Error in message callback: {e}")
            except asyncio.CancelledError:
                logger.info(f"Listener for {channel} cancelled")
            except Exception as e:
                logger.error(f"Error in pubsub listener: {e}")

        # Start the listener in the background
        asyncio.create_task(listener())

# Global singleton instance
message_broker = MessageBroker()
