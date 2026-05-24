from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, auth
from .database import engine, get_db
from .routers import workspaces

# For development MVP, create tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgencyOS API")

app.include_router(workspaces.router)

@app.get('/')
def read_root():
    return {'status': 'AgencyOS Server Online'}

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Get user's role and workspaces from memberships
    memberships = db.query(models.WorkspaceMember).filter(models.WorkspaceMember.user_id == user.id).all()
    tenant_ids = [m.workspace_id for m in memberships]
    
    # Simple role assignment for MVP: highest role across workspaces or default
    # A real system might encode a mapping of {workspace_id: role}
    roles = [m.role for m in memberships]
    primary_role = models.RoleEnum.SUPER_ADMIN.value if models.RoleEnum.SUPER_ADMIN.value in roles else \
                   (models.RoleEnum.AGENCY_ADMIN.value if models.RoleEnum.AGENCY_ADMIN.value in roles else \
                   models.RoleEnum.CLIENT_APPROVER.value)
                   
    # Super admins should probably be explicitly defined, but for MVP:
    if not roles and user.email == "admin@agencyos.com":
        primary_role = models.RoleEnum.SUPER_ADMIN.value
    elif not roles:
        primary_role = models.RoleEnum.CLIENT_READ_ONLY.value

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": primary_role, "tenant_ids": tenant_ids}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

