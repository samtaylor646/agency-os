#!/bin/bash
OUTPUT_FILE="docs/qa/qa_docs_git_analysis.md"

echo "# QA Directory Git Commit Analysis" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Analysis of files in \`docs/qa/\` ordered from most recently modified to oldest." >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Create a temporary file to store results for sorting
TMP_FILE=$(mktemp)

for file in docs/qa/*; do
  if [ -f "$file" ]; then
    # Get the last modification date in Unix timestamp for sorting
    LAST_MOD_TS=$(git log -1 --format="%at" -- "$file")
    
    # If file is untracked, it won't have a git log. Use file system modified time.
    if [ -z "$LAST_MOD_TS" ]; then
        LAST_MOD_TS=$(stat -f "%m" "$file" 2>/dev/null || stat -c "%Y" "$file")
    fi
    
    # Format dates
    LAST_MOD_DATE=$(git log -1 --format="%ad" --date=short -- "$file")
    if [ -z "$LAST_MOD_DATE" ]; then LAST_MOD_DATE="Untracked"; fi
    
    CREATED_DATE=$(git log --diff-filter=A --format="%ad" --date=short -- "$file" | tail -n 1)
    if [ -z "$CREATED_DATE" ]; then CREATED_DATE="Unknown"; fi
    
    COMMITS=$(git log --oneline -- "$file" | wc -l | tr -d ' ')
    
    # Get last commit subject
    LAST_SUBJECT=$(git log -1 --format="%s" -- "$file")
    if [ -z "$LAST_SUBJECT" ]; then LAST_SUBJECT="N/A"; fi

    # Store in temp file: TS|FileName|Created|LastMod|Commits|Subject
    echo "$LAST_MOD_TS|$file|$CREATED_DATE|$LAST_MOD_DATE|$COMMITS|$LAST_SUBJECT" >> "$TMP_FILE"
  fi
done

# Sort by timestamp descending
sort -t '|' -k1 -nr "$TMP_FILE" | while IFS='|' read -r ts file created lastmod commits subject; do
    filename=$(basename "$file")
    echo "### \`$filename\`" >> "$OUTPUT_FILE"
    echo "- **Last Modified:** $lastmod" >> "$OUTPUT_FILE"
    echo "- **Created:** $created" >> "$OUTPUT_FILE"
    echo "- **Total Commits:** $commits" >> "$OUTPUT_FILE"
    echo "- **Last Commit Message:** $subject" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

rm "$TMP_FILE"
