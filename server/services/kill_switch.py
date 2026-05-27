import os
import redis
import logging

logger = logging.getLogger(__name__)

class KillSwitch:
    """
    LLM Kill Switch to contain autonomous blast radiuses.
    Provides immediate halting of N:N Pods and autonomous DAG executions.
    """
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self._redis_client = None

    @property
    def redis(self):
        if not self._redis_client:
            try:
                self._redis_client = redis.from_url(self.redis_url, decode_responses=True)
            except Exception as e:
                logger.error(f"Failed to connect to Redis for Kill Switch: {e}")
        return self._redis_client

    def activate(self, tenant_id: str = "GLOBAL"):
        """Activate the kill switch for a specific tenant or globally."""
        key = f"kill_switch_active:{tenant_id}"
        try:
            if self.redis:
                self.redis.set(key, "1")
                logger.warning(f"KILL SWITCH ACTIVATED FOR: {tenant_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to activate kill switch via Redis: {e}")
            # Fallback could be implemented here
        return False

    def deactivate(self, tenant_id: str = "GLOBAL"):
        """Deactivate the kill switch."""
        key = f"kill_switch_active:{tenant_id}"
        try:
            if self.redis:
                self.redis.delete(key)
                logger.info(f"Kill switch deactivated for: {tenant_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to deactivate kill switch via Redis: {e}")
        return False

    def is_active(self, tenant_id: str = "GLOBAL") -> bool:
        """Check if the kill switch is currently active."""
        try:
            if self.redis:
                # Check global first, then tenant
                if self.redis.get("kill_switch_active:GLOBAL") == "1":
                    return True
                if tenant_id != "GLOBAL" and self.redis.get(f"kill_switch_active:{tenant_id}") == "1":
                    return True
        except Exception as e:
            logger.error(f"Failed to check kill switch status via Redis: {e}")
        return False

kill_switch = KillSwitch()
