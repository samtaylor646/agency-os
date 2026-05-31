import yaml
import glob
import os

os.chdir('site-docs/docs/archive')

categories = ['core', 'technical', 'research', 'operations', 'qa']
archive_nav = {}

for cat in categories:
    archive_nav[cat] = []
    if not os.path.exists(cat):
        continue
    files = glob.glob(f"{cat}/**/*.md", recursive=True) + glob.glob(f"{cat}/**/*.html", recursive=True)
    for f in sorted(files):
        # f is like 'core/architectural-review.md'
        title = os.path.basename(f).replace('.md', '').replace('.html', '').replace('_', ' ').replace('-', ' ').title()
        archive_nav[cat].append({title: f"docs/archive/{f}"})

print("Generated Archive Nav:")
print(yaml.dump({"Archive": [{"Core": archive_nav['core']}, {"Technical": archive_nav['technical']}, {"Research": archive_nav['research']}, {"Operations": archive_nav['operations']}, {"QA": archive_nav['qa']}]}, default_flow_style=False, sort_keys=False))

