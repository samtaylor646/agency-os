#!/bin/bash

# Define paths
CLINERULES=".clinerules"
TOGGLE_FILE="config/clinerules_ecosystem_board_toggle.md"
MARKER="# 🚨 MANDATE: ECOSYSTEM REVIEW BOARD (TOGGLEABLE)"

# Check if .clinerules exists
if [ ! -f "$CLINERULES" ]; then
    echo "Error: $CLINERULES not found."
    exit 1
fi

# Check if the toggle file exists
if [ ! -f "$TOGGLE_FILE" ]; then
    echo "Error: $TOGGLE_FILE not found."
    exit 1
fi

# Check if the rule is already in .clinerules
if grep -q "$MARKER" "$CLINERULES"; then
    echo "Ecosystem Review Board is currently ON. Toggling OFF..."
    # Create a temporary file
    temp_file=$(mktemp)
    
    # We use sed to delete everything from the MARKER to the end of the file 
    # (Assuming the toggle is always appended at the bottom)
    sed "/$MARKER/,\$d" "$CLINERULES" > "$temp_file"
    
    # Replace the original file
    mv "$temp_file" "$CLINERULES"
    echo "✅ Success: Ecosystem Review Board has been REMOVED from .clinerules."
    echo "Maximum development velocity restored."
else
    echo "Ecosystem Review Board is currently OFF. Toggling ON..."
    
    # Append the toggle file to the bottom of .clinerules
    echo "" >> "$CLINERULES"
    cat "$TOGGLE_FILE" >> "$CLINERULES"
    
    echo "✅ Success: Ecosystem Review Board has been ADDED to .clinerules."
    echo "Enterprise-grade architectural safety checks are now active."
fi
