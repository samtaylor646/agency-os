import subprocess
import sys
import os
import json

def run_in_docker(code_string):
    """
    Prototypes running arbitrary python code in a restricted Docker container.
    """
    # Write the code to a temporary file
    os.makedirs("sandbox_tmp", exist_ok=True)
    with open("sandbox_tmp/agent_code.py", "w") as f:
        f.write(code_string)

    print("Running in restricted Docker container...")
    
    # Run a restricted docker container
    # - --rm: remove after run
    # - --network none: no network access
    # - --memory 128m: limit memory
    # - --cpus 0.5: limit CPU
    # - -v: mount the script read-only
    try:
        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            "-v", f"{os.path.abspath('sandbox_tmp/agent_code.py')}:/app/agent_code.py:ro",
            "python:3.9-slim",
            "python", "/app/agent_code.py"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
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
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -2
        }

if __name__ == "__main__":
    # Test 1: Simple script
    safe_code = "print('Hello from the secure sandbox!')\nimport math\nprint(f'Pi is {math.pi}')"
    print("Testing safe code:")
    print(json.dumps(run_in_docker(safe_code), indent=2))
    
    # Test 2: Network attempt (should fail)
    network_code = "import urllib.request\ntry:\n    urllib.request.urlopen('http://google.com', timeout=3)\n    print('Network success')\nexcept Exception as e:\n    print(f'Network failed: {e}')"
    print("\nTesting network attempt:")
    print(json.dumps(run_in_docker(network_code), indent=2))
    
    # Test 3: Resource exhaustion (should be killed)
    # Memory bomb
    mem_code = "a = []\nwhile True:\n    a.append(' ' * 1024 * 1024)"
    print("\nTesting memory bomb:")
    print(json.dumps(run_in_docker(mem_code), indent=2))

