import pytest
from fastapi.testclient import TestClient
import httpx
from server.main import app
from server.routers.webhooks import webhook_queue
from server.utils.webhooks import send_webhook_payload
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_receive_webhook():
    # Clear the queue before test
    webhook_queue.clear()
    
    payload = {
        "event_type": "test.event",
        "data": {"key": "value"}
    }
    
    response = client.post("/api/v1/webhooks/1/webhook-123", json=payload)
    
    assert response.status_code == 202
    assert response.json() == {"message": "Webhook received successfully", "status": "queued"}
    
    assert len(webhook_queue) == 1
    assert webhook_queue[0]["tenant_id"] == 1
    assert webhook_queue[0]["webhook_id"] == "webhook-123"
    assert webhook_queue[0]["payload"]["event_type"] == "test.event"
    assert webhook_queue[0]["payload"]["data"] == {"key": "value"}

@pytest.mark.asyncio
async def test_send_webhook_payload_success():
    payload = {"event": "success"}
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = AsyncMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = await send_webhook_payload("http://example.com/webhook", payload)
        
        assert result is True
        mock_post.assert_called_once()

@pytest.mark.asyncio
async def test_send_webhook_payload_retry_failure():
    payload = {"event": "failure"}
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = httpx.RequestError("Network error")
        
        # Override asyncio.sleep to not actually sleep during tests
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            result = await send_webhook_payload("http://example.com/webhook", payload, max_retries=2, backoff_factor=0.1)
            
            assert result is False
            assert mock_post.call_count == 3  # Initial + 2 retries
            assert mock_sleep.call_count == 2
