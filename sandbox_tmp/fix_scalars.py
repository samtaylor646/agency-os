import re
import os
from pathlib import Path

def fix_scalars_syntax(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The issue is code like: `(await db.execute(select(models.Template).filter(...))).scalars())).scalars().first()`
    # And maybe `(await db.execute(select(...).scalars())).first()`
    # We want to make sure it's strictly `(await db.execute(select(...))).scalars().first()` or `...all()`
    
    # 1. Replace `.scalars())).scalars()` with `)).scalars()`
    # Let's just fix all weird `.scalars()`
    
    # Let's replace `)).scalars())).scalars()` with `)).scalars()`
    content = content.replace(")).scalars())).scalars()", ")).scalars()")
    content = content.replace("))).scalars())).scalars()", "))).scalars()")
    content = content.replace(")))).scalars())).scalars()", ")))).scalars()")
    
    # Let's replace `.scalars())).scalars())).scalars()`
    content = re.sub(r'(\)\)*)\.scalars\(\)\)+\.scalars\(\)', r'\1.scalars()', content)
    content = re.sub(r'(\)\)*)\.scalars\(\)\)+\.scalars\(\)', r'\1.scalars()', content) # run again just in case
    
    # Let's look for `select(...).scalars()` inside `db.execute()`
    content = re.sub(r'(await db\.execute\([^)]+)\.scalars\(\)\)', r'\1).scalars()', content)

    # Let's just do a simpler search and replace.
    # Actually, I will write it back
    with open(filepath, 'w') as f:
        f.write(content)

def main():
    server_dir = Path("server")
    for file in server_dir.rglob("*.py"):
        if "venv" in str(file):
            continue
        fix_scalars_syntax(file)

if __name__ == "__main__":
    main()
