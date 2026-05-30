import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # 1. Import AsyncSession and select
    if 'db.query(' in content or 'db.commit(' in content or 'db: Session' in content or 'Session =' in content:
        if 'AsyncSession' not in content:
            if 'from sqlalchemy.orm import Session' in content:
                content = content.replace('from sqlalchemy.orm import Session', 'from sqlalchemy.orm import Session\nfrom sqlalchemy.ext.asyncio import AsyncSession')
            elif 'from sqlalchemy import' in content:
                content = re.sub(r'from sqlalchemy import (.*?)\n', r'from sqlalchemy import \1\nfrom sqlalchemy.ext.asyncio import AsyncSession\n', content, count=1)
            else:
                content = "from sqlalchemy.ext.asyncio import AsyncSession\n" + content

        if 'select' not in content and ('db.query' in content or 'db.execute' in content):
            if 'from sqlalchemy import' in content:
                content = re.sub(r'from sqlalchemy import (.*?)\n', r'from sqlalchemy import \1, select\n', content, count=1)
            else:
                content = "from sqlalchemy import select\n" + content

    # 2. Change `db: Session` to `db: AsyncSession`
    content = content.replace('db: Session', 'db: AsyncSession')
    
    # Also in dependencies.py: `Session = Depends`
    content = content.replace('Session = Depends', 'AsyncSession = Depends')

    # 3. Change `def ` to `async def ` for route handlers
    # Find functions containing `db: AsyncSession` or `db: Session` and make them async if they aren't
    def repl_def(m):
        if 'async def' not in m.group(0):
            return m.group(0).replace('def ', 'async def ')
        return m.group(0)
    
    # We use a regex to find function signatures that have db: AsyncSession
    content = re.sub(r'(?:async\s+)?def\s+[a-zA-Z0-9_]+\(.*?\b(db:\s*AsyncSession|Depends\(get_db\))\b.*?\):', repl_def, content, flags=re.DOTALL)

    # Note: dependencies also need async def. We might just replace all route defs.
    content = re.sub(r'(?<!async )def ([a-zA-Z0-9_]+\(.*?\)):', r'async def \1:', content)
    # Revert `async def mask_key` if it exists and doesn't do async things?
    # Better to just change `def` to `async def` in all router files since FastAPI handles async.
    # Wait, some helper functions shouldn't be async if they aren't awaited. Let's rely on manual fixing if needed, or better, only make async if it uses await.
    
    # 4. Replace db.query(Model) with await db.execute(select(Model))
    # db.query(Model).filter(...).all()
    # db.query(Model).filter(...).first()
    # db.query(Model).all()
    # db.query(Model).first()
    
    def repl_query(m):
        model = m.group(1)
        rest = m.group(2) # e.g. .filter(X == Y).all()
        # We need to turn .all() -> .scalars().all()
        # and .first() -> .scalars().first()
        rest = rest.replace('.all()', '.scalars().all()')
        rest = rest.replace('.first()', '.scalars().first()')
        return f'(await db.execute(select({model}){rest}))'

    # Match db.query(...)...all() or .first()
    content = re.sub(r'db\.query\((.*?)\)((?:\.[a-zA-Z0-9_]+\(.*?\))*?\.(?:all|first)\(\))', repl_query, content)
    
    # For queries without .all() or .first() (just returning the query or using it in subquery)
    # It's rarer. We'll do a simple replace for remaining db.query
    content = re.sub(r'db\.query\((.*?)\)', r'(await db.execute(select(\1)))', content)
    # Wait, if we do the above, it will double await if we don't be careful.
    
    # 5. db.commit() and db.refresh()
    content = content.replace('db.commit()', 'await db.commit()')
    content = re.sub(r'db\.refresh\((.*?)\)', r'await db.refresh(\1)', content)

    # Remove double awaits
    content = content.replace('await await', 'await')
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Refactored {filepath}")

import glob

for filepath in glob.glob('server/routers/**/*.py', recursive=True):
    process_file(filepath)

process_file('server/dependencies.py')
process_file('scripts/seed_db.py')

