import os, sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from server import database, models, auth
db = database.SessionLocal()
user = db.query(models.User).filter(models.User.email == "admin@agencyos.com").first()
memberships = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id).all()
roles = [m.role for m in memberships]
print("Roles:", roles)
primary_role = models.RoleEnum.SUPER_ADMIN.value if models.RoleEnum.SUPER_ADMIN.value in roles else (models.RoleEnum.AGENCY_ADMIN.value if models.RoleEnum.AGENCY_ADMIN.value in roles else models.RoleEnum.CLIENT_APPROVER.value)
if not roles and user.email == "admin@agencyos.com":
    primary_role = models.RoleEnum.SUPER_ADMIN.value
elif not roles:
    primary_role = models.RoleEnum.CLIENT_READ_ONLY.value
print("Primary Role:", primary_role)
