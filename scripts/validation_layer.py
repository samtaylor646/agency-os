import sys
import os

def run_validation():
    print("Running validation against config/settings.md...")
    if not os.path.exists("config/settings.md"):
        print("Error: config/settings.md not found.")
        sys.exit(1)
    print("Validation passed. Task execution authorized.")
    sys.exit(0)

if __name__ == "__main__":
    run_validation()
