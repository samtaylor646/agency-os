import pytest
import os
import asyncio
from pathlib import Path

# Add project root to sys.path if needed
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.agent_parser import AgentParser
from scripts.central_runner import DAGOrchestrator

@pytest.fixture
def dummy_agent_dir(tmp_path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    
    # Create a valid agent
    valid_agent = agents_dir / "valid-agent.md"
    valid_agent.write_text("""---
name: Valid Agent
role: Tester
---
## 🎯 Your Core Mission
You are a test agent.

## 🚀 Advanced Capabilities
- Testing
- More testing

## 🚨 Critical Rules You Must Follow
No failing tests.
""")

    # Create an agent with malformed yaml
    invalid_yaml_agent = agents_dir / "invalid-yaml.md"
    invalid_yaml_agent.write_text("""---
name: [Invalid
role: Tester
---
## 🎯 Your Core Mission
System prompt here
""")

    # Create an agent with missing sections
    missing_sections_agent = agents_dir / "missing-sections.md"
    missing_sections_agent.write_text("""---
name: Missing
---
Just some text
""")

    return str(agents_dir)


def test_agent_parser_valid(dummy_agent_dir):
    parser = AgentParser(agents_dir=dummy_agent_dir)
    agent = parser.get_agent("valid-agent")
    
    assert agent is not None
    assert agent["metadata"].get("name") == "Valid Agent"
    assert "You are a test agent." in agent["core_mission"]
    assert "Testing" in agent["advanced_capabilities"]
    assert "No failing tests." in agent["critical_rules"]

def test_agent_parser_missing(dummy_agent_dir):
    parser = AgentParser(agents_dir=dummy_agent_dir)
    agent = parser.get_agent("non-existent-agent")
    assert agent is None

def test_agent_parser_invalid_yaml(dummy_agent_dir):
    parser = AgentParser(agents_dir=dummy_agent_dir)
    agent = parser.get_agent("invalid-yaml")
    
    assert agent is not None
    # YAML parse fails, so metadata might be empty or fallback
    assert agent.get("metadata") == {}
    assert "System prompt here" in agent["core_mission"]

def test_agent_parser_caching(dummy_agent_dir):
    parser = AgentParser(agents_dir=dummy_agent_dir)
    agent1 = parser.get_agent("valid-agent")
    
    # Modify file to test cache
    valid_agent = Path(dummy_agent_dir) / "valid-agent.md"
    valid_agent.write_text("Modified completely")
    
    agent2 = parser.get_agent("valid-agent")
    # Should be served from cache, so unchanged
    assert agent1 == agent2


# DAG Orchestrator Tests

def test_dag_topological_sort():
    orchestrator = DAGOrchestrator()
    orchestrator.add_node("A", "agent1", "task A")
    orchestrator.add_node("B", "agent2", "task B")
    orchestrator.add_node("C", "agent3", "task C")
    orchestrator.add_node("D", "agent4", "task D")
    
    orchestrator.add_edge("A", "B")
    orchestrator.add_edge("A", "C")
    orchestrator.add_edge("B", "D")
    orchestrator.add_edge("C", "D")
    
    levels = orchestrator.get_topological_sort()
    assert len(levels) == 3
    assert levels[0] == ["A"]
    assert set(levels[1]) == {"B", "C"}
    assert levels[2] == ["D"]

def test_dag_cycle_detection():
    orchestrator = DAGOrchestrator()
    orchestrator.add_node("A", "agent1", "task A")
    orchestrator.add_node("B", "agent2", "task B")
    
    orchestrator.add_edge("A", "B")
    orchestrator.add_edge("B", "A")  # Cycle
    
    with pytest.raises(ValueError, match="Cycle detected"):
        orchestrator.get_topological_sort()

@pytest.mark.asyncio
async def test_dag_execution_success():
    orchestrator = DAGOrchestrator()
    orchestrator.add_node("A", "agent1", "task A")
    orchestrator.add_node("B", "agent2", "task B")
    orchestrator.add_edge("A", "B")
    
    results = await orchestrator.execute_workflow("tenant-test")
    
    assert "A" in results
    assert "B" in results
    assert "Output from A" in results["A"]
    assert "Output from B" in results["B"]

@pytest.mark.asyncio
async def test_dag_execution_cycle_error():
    orchestrator = DAGOrchestrator()
    orchestrator.add_node("A", "agent1", "task A")
    orchestrator.add_node("B", "agent2", "task B")
    orchestrator.add_edge("A", "B")
    orchestrator.add_edge("B", "A")
    
    results = await orchestrator.execute_workflow("tenant-test")
    assert "error" in results
    assert "Cycle detected" in results["error"]
