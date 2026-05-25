import yaml
import os
from server.services.queue_manager import QueueManager

class AgentRunner:
    def __init__(self, agent_domain=None, agent_file=None):
        self.agent_domain = agent_domain
        self.agent_file = agent_file
        self.config = self._load_config()

    def _load_config(self):
        if self.agent_file and os.path.exists(self.agent_file):
            with open(self.agent_file, 'r') as file:
                # Basic parsing if it's a markdown prompt file
                content = file.read()
                return {"identity": {"name": os.path.basename(self.agent_file), "role": "Dynamically Assigned Agent"}}
        elif self.agent_domain:
            path = f"agents/{self.agent_domain}/config.yaml"
            if os.path.exists(path):
                with open(path, 'r') as file:
                    return yaml.safe_load(file)
        return None

    def execute_task(self, task_description):
        if not self.config:
            return "Error: Agent configuration not found."
        
        print(f"Initializing {self.config['identity']['name']} for task...")
        return f"Task '{task_description}' processed by {self.config['identity']['role']}."

class CentralOrchestrator:
    def __init__(self):
        self.queue_manager = QueueManager()
    
    def process_task_list(self, markdown_tasks: str):
        tasks = self.queue_manager.parse_markdown_tasks(markdown_tasks)
        print(f"Parsed {len(tasks)} tasks.")
        
        ready_tasks = self.queue_manager.get_ready_tasks()
        while ready_tasks:
            for task in ready_tasks:
                print(f"Assigning task: {task.description}")
                # Use queue manager to find best agent
                agent_path = self.queue_manager.match_agent_to_task(task)
                task.assigned_agent = agent_path
                
                runner = AgentRunner(agent_file=agent_path)
                result = runner.execute_task(task.description)
                print(result)
                
                self.queue_manager.mark_completed(task.id)
            
            ready_tasks = self.queue_manager.get_ready_tasks()

if __name__ == "__main__":
    orchestrator = CentralOrchestrator()
    sample_markdown = """
    - [ ] Task 1: Setup database schema
    - [ ] Task 2: Create API endpoints (Depends on: task_1)
    """
    orchestrator.process_task_list(sample_markdown)
