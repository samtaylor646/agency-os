import os
import yaml
import glob

workspace = '/Users/samtaylor/Dev/projects/Agency/agency-os'
os.chdir(os.path.join(workspace, 'site-docs/docs/archive'))

categories = ['core', 'technical', 'research', 'operations', 'qa']
archive_nav = {}

for cat in categories:
    archive_nav[cat] = []
    if not os.path.exists(cat):
        continue
    files = glob.glob(f"{cat}/**/*.md", recursive=True) + glob.glob(f"{cat}/**/*.html", recursive=True)
    for f in sorted(files):
        title = os.path.basename(f).replace('.md', '').replace('.html', '').replace('_', ' ').replace('-', ' ').title()
        archive_nav[cat].append({title: f"docs/archive/{f}"})

os.chdir(workspace)

new_archive = {"Archive": [
    {"Core": archive_nav['core']},
    {"Technical": archive_nav['technical']},
    {"Research": archive_nav['research']},
    {"Operations": archive_nav['operations']},
    {"QA": archive_nav['qa']}
]}

yaml_str = yaml.dump([new_archive], default_flow_style=False, sort_keys=False)

with open('mkdocs.yml', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('- Archive:'):
        start_idx = i
    if start_idx != -1 and line.startswith('theme:'):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [yaml_str] + lines[end_idx:]
    with open('mkdocs.yml', 'w') as f:
        f.writelines(new_lines)
    print("mkdocs.yml updated successfully")
else:
    print(f"Could not find boundaries. start: {start_idx}, end: {end_idx}")

