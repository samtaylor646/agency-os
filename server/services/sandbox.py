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
        cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", self.memory_limit,
            "--cpus", self.cpu_limit,
            self.image,
            "python", "-"
        ]
        
        try:
            result = subprocess.run(cmd, input=code_string, capture_output=True, text=True, timeout=self.timeout)
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
