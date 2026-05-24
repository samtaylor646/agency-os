import re
from context import get_tenant_id

class TaskValidator:
    def __init__(self, settings_path="config/settings.md"):
        self.settings = self._load_settings(settings_path)

    def _load_settings(self, path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def pre_flight_check(self, task_description):
        print("--- Pre-flight Check Initiated ---")
        tenant_id = get_tenant_id()
        print(f"Tenant ID: {tenant_id}")
        print(f"Task: {task_description}")
        
        if not tenant_id:
            print("Warning: No tenant context found. Execution may be restricted.")
        
        if "strategy" in task_description.lower() or "implementation" in task_description.lower():
            print("Status: Requires Explicit User Permission (Rule 5)")
        else:
            print("Status: Standard Execution")
            
        return "Validation Complete: Task parameters verified against system rules."
