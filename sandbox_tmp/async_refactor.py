import os
import re

FILES_TO_PROCESS = [
    'server/routers/audit.py',
    'server/routers/credentials.py',
    'server/routers/documents.py',
    'server/routers/rbac.py',
    'server/routers/agents.py',
    'server/routers/custom_agents.py',
    'server/routers/chat.py',
    'server/routers/marketplace.py',
    'server/routers/analytics.py',
    'server/routers/api_keys.py',
    'server/routers/projects.py',
    'server/routers/pipelines.py',
    'server/routers/workspaces.py',
    'server/auth.py',
    'server/dependencies.py',
    'server/main.py',
    'server/core/state_manager.py'
]

def add_imports(content):
    if 'from sqlalchemy import select' not in content:
        if 'from sqlalchemy import' in content:
            content = re.sub(r'from sqlalchemy import\s+', r'from sqlalchemy import select, ', content, count=1)
        else:
            content = "from sqlalchemy import select\n" + content
            
    if 'AsyncSession' not in content:
        if 'from sqlalchemy.ext.asyncio import AsyncSession' not in content:
            content = "from sqlalchemy.ext.asyncio import AsyncSession\n" + content
            
    return content

def fix_function_signatures(content):
    # Change db: Session to db: AsyncSession
    content = re.sub(r'db:\s*Session', r'db: AsyncSession', content)
    # Ensure functions taking db: AsyncSession are async
    
    # A bit tricky: find `def func_name(...db: AsyncSession...):` and add async if not present
    # regex won't easily parse across lines if parameters are split, but let's do a simple pass:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') and 'async def' not in line:
            # check if db: AsyncSession is in this line or next few lines up to :
            j = i
            sig = ""
            while j < len(lines) and ':' not in lines[j]:
                sig += lines[j]
                j += 1
            if j < len(lines):
                sig += lines[j]
            
            if 'db' in sig and 'get_db' in sig: # a good proxy
                lines[i] = lines[i].replace('def ', 'async def ')
    return '\n'.join(lines)


def replace_queries(content):
    # .order_by(...).first()
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.order_by\((.*?)\)\.first\(\)', 
                     r'(await db.execute(select(\1).filter(\2).order_by(\3))).scalars().first()', content, flags=re.DOTALL)
    
    # .order_by(...).limit(...).all()
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.order_by\((.*?)\)\.limit\((.*?)\)\.all\(\)', 
                     r'(await db.execute(select(\1).filter(\2).order_by(\3).limit(\4))).scalars().all()', content, flags=re.DOTALL)
                     
    # .filter(...).first()
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.first\(\)', 
                     r'(await db.execute(select(\1).filter(\2))).scalars().first()', content, flags=re.DOTALL)
                     
    # .filter(...).all()
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.all\(\)', 
                     r'(await db.execute(select(\1).filter(\2))).scalars().all()', content, flags=re.DOTALL)
                     
    # .all()
    content = re.sub(r'db\.query\((.*?)\)\.all\(\)', 
                     r'(await db.execute(select(\1))).scalars().all()', content, flags=re.DOTALL)
                     
    # .first()
    content = re.sub(r'db\.query\((.*?)\)\.first\(\)', 
                     r'(await db.execute(select(\1))).scalars().first()', content, flags=re.DOTALL)
                     
    # .scalar() for analytics
    content = re.sub(r'db\.query\((.*?)\)\.filter\((.*?)\)\.scalar\(\)',
                     r'(await db.execute(select(\1).filter(\2))).scalar()', content, flags=re.DOTALL)
                     
    return content

for file in FILES_TO_PROCESS:
    if not os.path.exists(file):
        continue
    with open(file, 'r') as f:
        content = f.read()
    
    orig = content
    content = add_imports(content)
    content = fix_function_signatures(content)
    content = replace_queries(content)
    
    if content != orig:
        with open(file, 'w') as f:
            f.write(content)
        print(f"Refactored {file}")

