import yaml
import os

class AgentRunner:
    def __init__(self, agent_domain):
        self.agent_domain = agent_domain
        self.config = self._load_config()

    def _load_config(self):
        path = f"agents/{self.agent_domain}/config.yaml"
        if os.path.exists(path):
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        return None

    def execute_task(self, task_description):
        if not self.config:
            return "Error: Agent configuration not found."
        
        print(f"Initializing {self.config['identity']['name']} for {self.agent_domain}...")
        return f"Task '{task_description}' processed by {self.config['identity']['role']}."
