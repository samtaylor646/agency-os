import os
import yaml
import re

class AgentParser:
    def __init__(self, agents_dir="agents"):
        self.agents_dir = agents_dir
        self._cache = {}

    def get_agent(self, agent_name: str) -> dict:
        """Get an agent by name from cache or by parsing the markdown file."""
        if agent_name in self._cache:
            return self._cache[agent_name]

        # Search for the agent in the agents directory recursively
        agent_file = self._find_agent_file(agent_name)
        if not agent_file:
            return None

        agent_data = self.parse_file(agent_file)
        if agent_data:
            self._cache[agent_name] = agent_data
        
        return agent_data

    def _find_agent_file(self, agent_name: str) -> str:
        """Recursively find an agent markdown file by name."""
        for root, _, files in os.walk(self.agents_dir):
            for file in files:
                if file.endswith(".md") and file[:-3] == agent_name:
                    return os.path.join(root, file)
        return None

    def parse_file(self, filepath: str) -> dict:
        """Parse a markdown file to extract frontmatter and sections."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None

        return self.parse_content(content)

    def parse_content(self, content: str) -> dict:
        """Parse raw markdown content into a dictionary."""
        agent_data = {
            "metadata": {},
            "identity_and_memory": "",
            "core_mission": "",
            "critical_rules": "",
            "architecture_deliverables": "",
            "communication_style": "",
            "learning_and_memory": "",
            "success_metrics": "",
            "advanced_capabilities": ""
        }

        # Parse Frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if frontmatter_match:
            try:
                agent_data["metadata"] = yaml.safe_load(frontmatter_match.group(1)) or {}
            except yaml.YAMLError as e:
                print(f"Error parsing frontmatter YAML: {e}")
            
            # Remove frontmatter from content for further processing
            content = content[frontmatter_match.end():]

        # Parse Headings using simple regex matching
        # Assuming sections like ## System Prompt, ## Capabilities, ## Guardrails
        def extract_section(title, text):
            # Match section until next ## or end of string
            pattern = rf"##\s+{title}\s*\n(.*?)(?=\n##\s+|\Z)"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

        agent_data["identity_and_memory"] = extract_section(r"🧠 Your Identity & Memory", content)
        agent_data["core_mission"] = extract_section(r"🎯 Your Core Mission", content)
        agent_data["critical_rules"] = extract_section(r"🚨 Critical Rules You Must Follow", content)
        agent_data["architecture_deliverables"] = extract_section(r"📋 Your Architecture Deliverables", content)
        agent_data["communication_style"] = extract_section(r"💭 Your Communication Style", content)
        agent_data["learning_and_memory"] = extract_section(r"🔄 Learning & Memory", content)
        agent_data["success_metrics"] = extract_section(r"🎯 Your Success Metrics", content)
        agent_data["advanced_capabilities"] = extract_section(r"🚀 Advanced Capabilities", content)

        return agent_data
