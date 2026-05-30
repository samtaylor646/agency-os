import os
import shutil
import json
import re
from datetime import datetime
from pathlib import Path

ROOTASKS_DIR = Path(".rootasks")
ARCHIVE_DIR = Path(".rootasks-archive")
INDEX_FILE = ARCHIVE_DIR / "index.md"

def init_dirs():
    """Ensure directories exist."""
    if not ROOTASKS_DIR.exists():
        print(f"Directory {ROOTASKS_DIR} does not exist. Creating it.")
        ROOTASKS_DIR.mkdir(parents=True, exist_ok=True)
        
    if not ARCHIVE_DIR.exists():
        print(f"Directory {ARCHIVE_DIR} does not exist. Creating it.")
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def is_completed(filepath: Path) -> bool:
    """
    Check if a task file is marked as completed.
    Looks for 'status: completed', 'status: done' or similar indicators.
    """
    try:
        content = filepath.read_text(encoding='utf-8').lower()
        # Look for explicit status markers
        if re.search(r'status:\s*(completed|done|archived)', content):
            return True
        # Look for completed checkboxes without pending ones
        if '[x]' in content and '[ ]' not in content:
            return True
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def update_index(archived_files):
    """Update the summary index with newly archived files."""
    if not archived_files:
        return
        
    is_new = not INDEX_FILE.exists()
    
    with open(INDEX_FILE, 'a', encoding='utf-8') as f:
        if is_new:
            f.write("# Archived Tasks Index\n\n")
            f.write("| Date Archived | Task File | Description/Title |\n")
            f.write("|---------------|-----------|-------------------|\n")
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for filename in archived_files:
            f.write(f"| {timestamp} | {filename} | Archived automatically |\n")

def run_archive():
    init_dirs()
    
    archived_count = 0
    archived_files = []
    
    print(f"Scanning {ROOTASKS_DIR} for completed tasks...")
    for filepath in ROOTASKS_DIR.glob("*.md"):
        if is_completed(filepath):
            dest_path = ARCHIVE_DIR / filepath.name
            
            # Handle potential filename collisions
            if dest_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                dest_path = ARCHIVE_DIR / f"{filepath.stem}_{timestamp}{filepath.suffix}"
                
            shutil.move(str(filepath), str(dest_path))
            archived_files.append(dest_path.name)
            archived_count += 1
            print(f"Archived: {filepath.name} -> {dest_path.name}")
            
    if archived_count > 0:
        update_index(archived_files)
        print(f"Successfully archived {archived_count} tasks.")
    else:
        print("No completed tasks found to archive.")

if __name__ == "__main__":
    run_archive()
