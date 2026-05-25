import re
import os
import glob
from typing import List, Dict, Any, Optional

class TaskNode:
    def __init__(self, id: str, description: str, dependencies: List[str] = None):
        self.id = id
        self.description = description
        self.dependencies = dependencies or []
        self.status = "pending"
        self.assigned_agent = None

class QueueManager:
    def __init__(self):
        self.tasks: Dict[str, TaskNode] = {}
        self.agents_registry = self._load_agents_registry()

    def _load_agents_registry(self) -> Dict[str, str]:
        """Loads available agents and their descriptions from the agents directory."""
        registry = {}
        # Get all md files in agents directory
        agent_files = glob.glob("agents/**/*.md", recursive=True)
        for file in agent_files:
            if "agent-list.md" in file or "playbooks" in file:
                continue
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Use a simplified representation of capabilities based on the file content
                registry[file] = content.lower()
        return registry

    def match_agent_to_task(self, task: TaskNode) -> str:
        """
        Dynamically matches a task to the most appropriate agent based on capabilities.
        Uses simple keyword matching for this implementation.
        """
        desc_lower = task.description.lower()
        best_match = None
        highest_score = -1

        keywords = desc_lower.split()
        
        for agent_file, capabilities in self.agents_registry.items():
            score = sum(1 for kw in keywords if kw in capabilities and len(kw) > 3)
            
            if score > highest_score:
                highest_score = score
                best_match = agent_file
                
        # Fallback if no specific match
        if best_match is None and self.agents_registry:
            best_match = list(self.agents_registry.keys())[0]
            
        return best_match

    def parse_markdown_tasks(self, markdown_content: str) -> List[TaskNode]:
        """
        Parses a markdown string containing tasks and converts them into DAG nodes.
        Expected format:
        - [ ] Task 1: Description
        - [ ] Task 2: Description (Depends on: Task 1)
        """
        tasks = []
        lines = markdown_content.split('\n')
        
        task_counter = 1
        for line in lines:
            line = line.strip()
            if line.startswith("- [ ]") or line.startswith("* [ ]"):
                # Extract task description and dependencies
                match = re.search(r'\[ \]\s*(.*?)(?:\s*\(Depends on:\s*(.*?)\))?$', line)
                if match:
                    description = match.group(1).strip()
                    deps_str = match.group(2)
                    
                    # Instead of generic IDs, try to extract 'Task X' prefix for dependency mapping
                    task_id_match = re.match(r'(Task \d+):', description, re.IGNORECASE)
                    if task_id_match:
                        task_id = task_id_match.group(1).lower().replace(" ", "_")
                    else:
                        task_id = f"task_{task_counter}"
                        
                    dependencies = []
                    if deps_str:
                        dependencies = [d.strip().lower().replace(" ", "_") for d in deps_str.split(',')]
                    
                    node = TaskNode(id=task_id, description=description, dependencies=dependencies)
                    self.tasks[task_id] = node
                    tasks.append(node)
                    task_counter += 1
                    
        return tasks

    def get_ready_tasks(self) -> List[TaskNode]:
        """Returns tasks that have no pending dependencies."""
        ready = []
        for task in self.tasks.values():
            if task.status == "pending":
                if all(self.tasks.get(dep, TaskNode("", "")).status == "completed" for dep in task.dependencies):
                    ready.append(task)
        return ready

    def mark_completed(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = "completed"
