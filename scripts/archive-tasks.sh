#!/bin/bash

# Ensure directories exist
mkdir -p .rootasks .rootasks-archive

# Check if there are any files in .rootasks
if [ -z "$(ls -A .rootasks)" ]; then
    echo "No tasks found in .rootasks."
    exit 0
fi

# Count files
count=$(ls -1q .rootasks | wc -l)

if [ "$count" -le 1 ]; then
    echo "Only $count task(s) present. Nothing to archive."
    exit 0
fi

# List files sorted by modification time (newest first)
# Use tail to skip the first (most recent) file and move the rest
echo "Archiving older tasks..."
ls -1t .rootasks/* | tail -n +2 | while read file; do
    mv "$file" ".rootasks-archive/"
    echo "Archived: $(basename "$file")"
done

echo "Archive complete. Most recent task retained in .rootasks."
