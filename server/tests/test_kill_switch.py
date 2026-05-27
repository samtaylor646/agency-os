import pytest
import fakeredis
from unittest.mock import patch
from server.services.kill_switch import KillSwitch

@pytest.fixture
def kill_switch():
    ks = KillSwitch()
    ks._redis_client = fakeredis.FakeRedis(decode_responses=True)
    return ks

def test_kill_switch_global(kill_switch):
    assert kill_switch.is_active() == False
    kill_switch.activate()
    assert kill_switch.is_active() == True
    kill_switch.deactivate()
    assert kill_switch.is_active() == False

def test_kill_switch_tenant(kill_switch):
    assert kill_switch.is_active("TENANT_A") == False
    kill_switch.activate("TENANT_A")
    assert kill_switch.is_active("TENANT_A") == True
    assert kill_switch.is_active("TENANT_B") == False
    
    # Global overrides
    kill_switch.activate("GLOBAL")
    assert kill_switch.is_active("TENANT_B") == True
