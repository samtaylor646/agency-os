import os
import re

replacements = [
    (r'docs/core/future_features_backlog\.md', 'docs/operations/future_features_backlog.md'),
    (r'core/future_features_backlog\.md', 'operations/future_features_backlog.md'),
    
    (r'docs/core/Documentation_TOC\.md', 'docs/operations/Documentation_TOC.md'),
    (r'core/Documentation_TOC\.md', 'operations/Documentation_TOC.md'),
    
    (r'docs/core/Epic_Phase5_Feedback_Loops_PRD\.md', 'docs/archive/Epic_Phase5_Feedback_Loops_PRD.md'),
    (r'core/Epic_Phase5_Feedback_Loops_PRD\.md', 'archive/Epic_Phase5_Feedback_Loops_PRD.md'),
    
    (r'docs/core/Epic_Phase6_Template_Library_PRD\.md', 'docs/archive/Epic_Phase6_Template_Library_PRD.md'),
    (r'core/Epic_Phase6_Template_Library_PRD\.md', 'archive/Epic_Phase6_Template_Library_PRD.md'),
    
    (r'docs/core/Epic_TechDebt_Nexus_Refactor\.md', 'docs/archive/Epic_TechDebt_Nexus_Refactor.md'),
    (r'core/Epic_TechDebt_Nexus_Refactor\.md', 'archive/Epic_TechDebt_Nexus_Refactor.md'),
    
    (r'docs/core/Reprioritization_Proposal_Phase5\.md', 'docs/archive/Reprioritization_Proposal_Phase5.md'),
    (r'core/Reprioritization_Proposal_Phase5\.md', 'archive/Reprioritization_Proposal_Phase5.md'),
]

for root, dirs, files in os.walk("docs"):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = re.sub(old, new, new_content)
                
            if new_content != content:
                print(f"Updated {filepath}")
                with open(filepath, 'w') as f:
                    f.write(new_content)
