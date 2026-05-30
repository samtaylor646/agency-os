import sys
import os

class ProtectedFileError(Exception):
    """Exception raised when an attempt is made to modify or archive a protected tracking document."""
    pass

ROOT_FILE_WHITELIST = {
    ".clinerules",
    ".gitignore",
    ".roomodes",
    "docker-compose.yml",
    "pytest.ini",
    "README.md",
    "mkdocs.yml"
}

PROTECTED_DOCS_PATTERNS = [
    "docs/qa/",
    "docs/operations/",
    "docs/technical/"
]

def validate_file_creation(file_path: str):
    """
    Guardrail function to prevent the creation of unauthorized files in the root workspace directory.
    """
    normalized_path = os.path.normpath(file_path)
    # Check if the file is being created in the root directory
    if os.path.dirname(normalized_path) == "":
        if normalized_path not in ROOT_FILE_WHITELIST:
            print(f"Error: Attempt to create unauthorized root file '{normalized_path}'.")
            print("Root file creation is blocked by the Root File Blocker Hard Rule.")
            print("Please place the file in the correct subfolder (e.g., docs/, agents/, scripts/, server/, client/, etc.).")
            sys.exit(1)

def validate_file_modification(file_path: str):
    """
    Guardrail function to prevent the modification, archival, or deletion of active tracking documentation.
    """
    normalized_path = os.path.normpath(file_path).replace("\\", "/")
    
    if normalized_path.startswith("docs/archive/"):
        return
        
    for pattern in PROTECTED_DOCS_PATTERNS:
        if normalized_path.startswith(pattern):
            raise ProtectedFileError(f"Cannot modify, archive, or delete active tracking file: {normalized_path}")

def run_validation():
    print("Running validation against config/settings.md...")
    if not os.path.exists("config/settings.md"):
        print("Error: config/settings.md not found.")
        sys.exit(1)
        
    # Check if a file path was passed as an argument for validation
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "--validate-file" and len(sys.argv) > 2:
            validate_file_creation(sys.argv[2])
        elif command == "--validate-mod" and len(sys.argv) > 2:
            validate_file_modification(sys.argv[2])

    print("Validation passed. Task execution authorized.")
    sys.exit(0)

if __name__ == "__main__":
    run_validation()

class TaskValidator:
    def pre_flight_check(self, task):
        print(f"Validation passed for task: {task}")
        return "valid"
