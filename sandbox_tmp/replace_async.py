import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    orig_content = content

    # Add sqlalchemy select import if not present
    if 'from sqlalchemy import select' not in content and 'from sqlalchemy import' in content:
        content = re.sub(r'(from sqlalchemy import\s+)(.*?)', r'\1select, \2', content, count=1)
    elif 'from sqlalchemy import select' not in content:
        if 'import sqlalchemy' in content:
            content = content.replace('import sqlalchemy', 'import sqlalchemy\nfrom sqlalchemy import select')
        else:
            # try to insert near other imports
            content = "from sqlalchemy import select\n" + content
            
    # func import for analytics
    if 'func.' in content and 'from sqlalchemy import select, func' not in content:
        content = content.replace('from sqlalchemy import select, ', 'from sqlalchemy import select, func, ')

    # Basic substitutions for query(...).filter(...)
    # We'll use a loop to replace them one by one to handle different combinations
    
    # query().filter().first()
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.first\(\)', r'(await db.execute(select(\1).filter(\2))).scalars().first()', content, flags=re.DOTALL)
    
    # query().filter().all()
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.all\(\)', r'(await db.execute(select(\1).filter(\2))).scalars().all()', content, flags=re.DOTALL)
    
    # query().all()
    content = re.sub(r'db\.query\((.*?)\)\.all\(\)', r'(await db.execute(select(\1))).scalars().all()', content, flags=re.DOTALL)
    
    # query().first()
    content = re.sub(r'db\.query\((.*?)\)\.first\(\)', r'(await db.execute(select(\1))).scalars().first()', content, flags=re.DOTALL)

    # Some multiline queries might be broken up differently, or might not have first()/all() on the same line.
    
    if orig_content != content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk('server'):
    for file in files:
        if file.endswith('.py'):
            process_file(os.path.join(root, file))

