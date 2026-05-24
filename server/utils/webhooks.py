import httpx
import logging
import asyncio
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

async def send_webhook_payload(
    url: str, 
    payload: Dict[str, Any], 
    headers: Optional[Dict[str, str]] = None,
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> bool:
    """
    Sends a webhook payload to the given URL with a basic retry mechanism.
    
    Args:
        url: The destination URL.
        payload: The data to send.
        headers: Optional headers (e.g., for signatures).
        max_retries: Number of times to retry on failure.
        backoff_factor: Multiplier for exponential backoff delay.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if headers is None:
        headers = {"Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries + 1):
            try:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                logger.info(f"Successfully sent webhook to {url}")
                return True
            except httpx.RequestError as exc:
                logger.warning(f"Request error while sending webhook to {url}: {exc}")
            except httpx.HTTPStatusError as exc:
                logger.warning(f"HTTP error {exc.response.status_code} while sending webhook to {url}: {exc}")
            except Exception as exc:
                logger.error(f"Unexpected error sending webhook to {url}: {exc}")
                
            if attempt < max_retries:
                delay = backoff_factor * (2 ** attempt)
                logger.info(f"Retrying webhook delivery to {url} in {delay}s (Attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(delay)
                
    logger.error(f"Failed to send webhook to {url} after {max_retries} retries")
    return False
