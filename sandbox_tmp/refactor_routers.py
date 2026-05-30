import os
import re

ROUTERS = [
    "server/routers/chat.py",
    "server/routers/custom_agents.py",
    "server/routers/pipelines.py",
    "server/routers/documents.py"
]

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Imports
    if "from sqlalchemy.ext.asyncio import AsyncSession" not in content:
        content = re.sub(
            r"from sqlalchemy.orm import Session",
            "from sqlalchemy.orm import Session\nfrom sqlalchemy.ext.asyncio import AsyncSession\nfrom sqlalchemy.future import select",
            content
        )
    
    # Change dependencies.get_db / get_db -> dependencies.get_async_db / get_async_db
    content = content.replace("Depends(dependencies.get_db)", "Depends(dependencies.get_async_db)")
    content = content.replace("Depends(get_db)", "Depends(dependencies.get_async_db)")
    
    # Change db: Session -> db: AsyncSession
    content = content.replace("db: Session", "db: AsyncSession")

    # Function defs def -> async def
    content = re.sub(r"(@router\.[a-z]+\([^)]+\)\n)def ", r"\1async def ", content)
    
    # DB Queries
    # db.query(models.Model).filter(...).all()
    # db.query(models.Model).filter(...).first()
    
    # Needs a bit more complex replacement for queries
    # Let's replace db.query(X).filter(Y).all() -> (await db.execute(select(X).filter(Y))).scalars().all()
    # and db.query(X).filter(Y).first() -> (await db.execute(select(X).filter(Y))).scalars().first()
    
    def repl_query(match):
        model = match.group(1)
        rest = match.group(2)
        end = match.group(3) # .all() or .first()
        
        # We might have .filter(...)
        new_q = f"(await db.execute(select({model}){rest})).scalars().{end}()"
        return new_q

    content = re.sub(r"db\.query\((.*?)\)(.*?)\.(all|first)\(\)", repl_query, content)
    
    # db.commit() -> await db.commit()
    content = content.replace("db.commit()", "await db.commit()")
    content = content.replace("db.rollback()", "await db.rollback()")
    content = content.replace("db.refresh(", "await db.refresh(")
    content = content.replace("db.flush()", "await db.flush()")

    # Handle dependencies import in pipelines and documents
    if "from ..dependencies import get_async_db" not in content and "get_async_db" in content and "dependencies.get_async_db" not in content:
        content = content.replace("from ..database import get_db", "from ..database import get_db\nfrom .. import dependencies")

    with open(filepath, "w") as f:
        f.write(content)

for filepath in ROUTERS:
    process_file(filepath)
    print(f"Processed {filepath}")

