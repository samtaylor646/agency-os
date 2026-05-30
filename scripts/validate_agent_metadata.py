#!/usr/bin/env python3
import sys
import os
import re

def validate_agent_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Simple regex to check for YAML frontmatter
    # e.g.,
    # ---
    # role: ...
    # ---
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return False, "Missing or malformed YAML frontmatter (must start with ---)."

    frontmatter = frontmatter_match.group(1).lower()

    # Check for required fields in frontmatter (simple string check)
    required_fields = ['role:', 'description:']
    missing = [field for field in required_fields if field not in frontmatter]
    if missing:
        return False, f"Frontmatter missing required fields: {', '.join(missing)}"

    return True, ""

def main():
    # If files are passed via args (from pre-commit), check those.
    # Otherwise, check all markdown files in agents/
    files_to_check = sys.argv[1:]

    if not files_to_check:
        print("No files provided, checking all agents... (Manual run)")
        for root, dirs, files in os.walk('agents'):
            for file in files:
                if file.endswith('.md') and not file.endswith('agent-list.md'):
                    files_to_check.append(os.path.join(root, file))
    
    if not files_to_check:
        sys.exit(0)

    has_errors = False
    for filepath in files_to_check:
        if not filepath.startswith('agents/') or not filepath.endswith('.md'):
            continue
        
        # Skip agent-list.md and team directories
        if 'agent-list.md' in filepath or '/teams/' in filepath:
            continue

        if os.path.exists(filepath):
            valid, reason = validate_agent_file(filepath)
            if not valid:
                print(f"[Error] {filepath}: {reason}")
                has_errors = True

    if has_errors:
        print("\nAgent Metadata Validation Failed.")
        print("Agents must have valid YAML frontmatter containing 'role:' and 'description:'.")
        print("This ensures proper routing, auditability, and SOC2 compliance.")
        sys.exit(1)
    else:
        print("Agent Metadata Validation Passed. All agents compliant.")
        sys.exit(0)

if __name__ == '__main__':
    main()
