import os
import shutil

os.makedirs('docs/archive/operations', exist_ok=True)
shutil.move('docs/operations/Project_Tracking_and_Dependencies.md', 'docs/archive/operations/Project_Tracking_and_Dependencies.md')
shutil.move('docs/operations/strategy_structure.md', 'docs/archive/operations/strategy_structure.md')
