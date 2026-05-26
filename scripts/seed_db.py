import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from server import database, models, auth
from sqlalchemy.orm import Session

db = database.SessionLocal()
models.Base.metadata.create_all(bind=database.engine)

user = db.query(models.User).filter(models.User.email == "admin@agencyos.com").first()
if not user:
    hashed_password = auth.get_password_hash("password123")
    user = models.User(email="admin@agencyos.com", hashed_password=hashed_password)
    db.add(user)
    db.commit()
    print("User seeded")
else:
    print("User already exists")

workspace = db.query(models.Workspace).filter(models.Workspace.id == 1).first()
if not workspace:
    workspace = models.Workspace(id=1, name="Acme Corp")
    db.add(workspace)
    db.commit()
    print("Workspace 1 seeded")

workspace2 = db.query(models.Workspace).filter(models.Workspace.id == 2).first()
if not workspace2:
    workspace2 = models.Workspace(id=2, name="Globex Inc")
    db.add(workspace2)
    db.commit()
    print("Workspace 2 seeded")

member = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id, models.WorkspaceMember.workspace_id == 1).first()
if not member:
    member = models.WorkspaceMember(workspace_id=1, user_id=user.id, role=models.RoleEnum.SUPER_ADMIN.value)
    db.add(member)
    db.commit()
    print("Workspace member 1 seeded")

member2 = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id, models.WorkspaceMember.workspace_id == 2).first()
if not member2:
    member2 = models.WorkspaceMember(workspace_id=2, user_id=user.id, role=models.RoleEnum.SUPER_ADMIN.value)
    db.add(member2)
    db.commit()
    print("Workspace member 2 seeded")

db.close()
