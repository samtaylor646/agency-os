from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import secrets

from .. import models, schemas, auth
from ..database import get_db
from ..dependencies import get_tenant_context

router = APIRouter(
    prefix="/api/v1/api_keys",
    tags=["API Keys"]
)

def generate_api_key_string() -> (str, str):
    """
    Generates a secure random API key.
    Returns (full_key, prefix)
    Format: ak_{prefix}_{random_chars}
    Prefix is useful for DB lookups.
    """
    prefix = secrets.token_hex(4) # 8 characters
    random_part = secrets.token_urlsafe(32)
    full_key = f"ak_{prefix}_{random_part}"
    full_prefix = f"ak_{prefix}"
    return full_key, full_prefix

@router.post("/", response_model=schemas.APIKeyCreateOut)
def create_api_key(
    key_data: schemas.APIKeyCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_context)
):
    """
    Generate a new API key for the current workspace.
    The plain text key is only returned once.
    """
    full_key, prefix = generate_api_key_string()
    hashed_key = auth.get_api_key_hash(full_key)
    
    expires_at = None
    if key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=key_data.expires_in_days)
        
    db_key = models.WorkspaceAPIKey(
        workspace_id=tenant_id,
        name=key_data.name,
        prefix=prefix,
        hashed_key=hashed_key,
        expires_at=expires_at,
        is_active=1
    )
    
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    
    # Return the full key only once
    response = schemas.APIKeyCreateOut.from_orm(db_key)
    response.key = full_key
    
    return response

@router.get("/", response_model=List[schemas.APIKeyOut])
def list_api_keys(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_context)
):
    """
    List all API keys for the current workspace.
    """
    keys = db.query(models.WorkspaceAPIKey).filter(
        models.WorkspaceAPIKey.workspace_id == tenant_id
    ).all()
    return keys

@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_context)
):
    """
    Revoke an API key.
    """
    db_key = db.query(models.WorkspaceAPIKey).filter(
        models.WorkspaceAPIKey.id == key_id,
        models.WorkspaceAPIKey.workspace_id == tenant_id
    ).first()
    
    if not db_key:
        raise HTTPException(status_code=404, detail="API Key not found")
        
    db_key.is_active = 0
    db.commit()
    return None
