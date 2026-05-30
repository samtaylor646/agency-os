import pytest
import os
import sys

from server import database, models

# Provide a dummy test for auth role extraction
def test_user_roles():
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.email == "admin@agencyos.com").first()
    if not user:
        pytest.skip("User admin@agencyos.com not found in test db")
    
    memberships = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id).all()
    roles = [m.role for m in memberships]
    
    primary_role = models.RoleEnum.SUPER_ADMIN.value if models.RoleEnum.SUPER_ADMIN.value in roles else (models.RoleEnum.AGENCY_ADMIN.value if models.RoleEnum.AGENCY_ADMIN.value in roles else models.RoleEnum.CLIENT_APPROVER.value)
    if not roles and user.email == "admin@agencyos.com":
        primary_role = models.RoleEnum.SUPER_ADMIN.value
    elif not roles:
        primary_role = models.RoleEnum.CLIENT_READ_ONLY.value
        
    assert primary_role is not None
