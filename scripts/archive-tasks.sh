#!/bin/bash

# Ensure directories exist
mkdir -p .roo-tasks .roo-tasks-archive

# Check if there are any files in .roo-tasks
if [ -z "$(ls -A .roo-tasks)" ]; then
    echo "No tasks found in .roo-tasks."
    exit 0
fi

# Count markdown files
count=$(ls -1q .roo-tasks/*.md 2>/dev/null | wc -l)

if [ "$count" -le 1 ]; then
    echo "Only $count task(s) present. Nothing to archive."
    exit 0
fi

# List files sorted by modification time (newest first)
# Use tail to skip the first (most recent) file and move the rest
echo "Archiving older tasks..."
ls -1t .roo-tasks/*.md | tail -n +2 | while read file; do
    mv "$file" ".roo-tasks-archive/"
    echo "Archived: $(basename "$file")"
done

echo "Archive complete. Most recent task retained in .roo-tasks."
