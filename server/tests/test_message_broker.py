import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from server.services.message_broker import MessageBroker

@pytest.fixture
def broker():
    return MessageBroker()

@pytest.mark.asyncio
async def test_message_broker_connect(broker):
    with patch("server.services.message_broker.redis.from_url") as mock_redis:
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        
        await broker.connect()
        
        mock_redis.assert_called_once_with(broker.redis_url, decode_responses=True)
        assert broker.redis_client == mock_client
        mock_client.pubsub.assert_called_once()

@pytest.mark.asyncio
async def test_message_broker_publish(broker):
    with patch("server.services.message_broker.redis.from_url") as mock_redis:
        mock_client = AsyncMock()
        mock_redis.return_value = mock_client
        broker.redis_client = mock_client # bypass connect if needed, but connect sets pubsub
        
        await broker.publish("test-pod-id", {"status": "started"})
        
        mock_client.publish.assert_called_once()
        args, kwargs = mock_client.publish.call_args
        assert args[0] == "pod:test-pod-id:messages"
        assert '{"status": "started"}' in args[1]
