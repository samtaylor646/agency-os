import subprocess
import os
import uuid
import tempfile
import logging

logger = logging.getLogger(__name__)

class SecureSandbox:
    def __init__(self, memory_limit="128m", cpu_limit="0.5", timeout=10):
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.timeout = timeout
        self.image = "python:3.9-slim"

    def execute_script(self, code_string: str) -> dict:
        """
        Executes arbitrary python code in a restricted Docker container.
        Returns a dict with stdout, stderr, and exit_code.
        """
        # Create a temporary directory to store the script
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = os.path.join(temp_dir, "agent_code.py")
            with open(script_path, "w") as f:
                f.write(code_string)
            
            cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", self.memory_limit,
                "--cpus", self.cpu_limit,
                "-v", f"{os.path.abspath(script_path)}:/app/agent_code.py:ro",
                self.image,
                "python", "/app/agent_code.py"
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode
                }
            except subprocess.TimeoutExpired:
                return {
                    "stdout": "",
                    "stderr": "Execution timed out",
                    "exit_code": -1
                }
            except Exception as e:
                logger.error(f"Sandbox execution failed: {e}")
                return {
                    "stdout": "",
                    "stderr": str(e),
                    "exit_code": -2
                }

# Singleton instance
sandbox_env = SecureSandbox()
