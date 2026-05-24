from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db
from ..utils.crypto import CryptoService
from ..context import get_tenant_id

router = APIRouter(
    prefix="/api/v1/credentials",
    tags=["credentials"],
    dependencies=[Depends(auth.get_current_user)]
)

def mask_key(key: str) -> str:
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"

@router.post("/", response_model=schemas.CredentialOut)
def create_credential(cred_in: schemas.CredentialCreate, db: Session = Depends(get_db)):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required")
        
    workspace = db.query(models.Workspace).filter(models.Workspace.id == tenant_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    crypto_service = CryptoService()
    
    # Initialize workspace DEK if it doesn't exist
    if not workspace.encrypted_dek:
        dek = crypto_service.generate_key()
        workspace.encrypted_dek = crypto_service.encrypt_dek(dek)
        db.commit()
        
    # Check if provider already exists for tenant
    existing = db.query(models.Credential).filter(
        models.Credential.tenant_id == tenant_id,
        models.Credential.provider == cred_in.provider
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Credential for {cred_in.provider} already exists")
        
    # Encrypt the key
    encrypted_key = crypto_service.encrypt_tenant_data(workspace.encrypted_dek, cred_in.key)
    
    new_cred = models.Credential(
        tenant_id=tenant_id,
        provider=cred_in.provider,
        encrypted_key=encrypted_key
    )
    db.add(new_cred)
    db.commit()
    db.refresh(new_cred)
    
    return {
        "id": new_cred.id,
        "tenant_id": new_cred.tenant_id,
        "provider": new_cred.provider,
        "created_at": new_cred.created_at,
        "updated_at": new_cred.updated_at,
        "masked_key": mask_key(cred_in.key)
    }

@router.get("/", response_model=List[schemas.CredentialOut])
def get_credentials(db: Session = Depends(get_db)):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required")
        
    credentials = db.query(models.Credential).filter(models.Credential.tenant_id == tenant_id).all()
    
    result = []
    if credentials:
        workspace = db.query(models.Workspace).filter(models.Workspace.id == tenant_id).first()
        crypto_service = CryptoService()
        for c in credentials:
            try:
                decrypted_key = crypto_service.decrypt_tenant_data(workspace.encrypted_dek, c.encrypted_key)
                masked = mask_key(decrypted_key)
            except Exception:
                masked = "**** (Decryption Failed)"
                
            result.append({
                "id": c.id,
                "tenant_id": c.tenant_id,
                "provider": c.provider,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
                "masked_key": masked
            })
            
    return result

@router.put("/{credential_id}", response_model=schemas.CredentialOut)
def update_credential(credential_id: int, cred_in: schemas.CredentialUpdate, db: Session = Depends(get_db)):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required")
        
    credential = db.query(models.Credential).filter(
        models.Credential.id == credential_id,
        models.Credential.tenant_id == tenant_id
    ).first()
    
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
        
    workspace = db.query(models.Workspace).filter(models.Workspace.id == tenant_id).first()
    crypto_service = CryptoService()
    
    encrypted_key = crypto_service.encrypt_tenant_data(workspace.encrypted_dek, cred_in.key)
    credential.encrypted_key = encrypted_key
    
    db.commit()
    db.refresh(credential)
    
    return {
        "id": credential.id,
        "tenant_id": credential.tenant_id,
        "provider": credential.provider,
        "created_at": credential.created_at,
        "updated_at": credential.updated_at,
        "masked_key": mask_key(cred_in.key)
    }

@router.delete("/{credential_id}")
def delete_credential(credential_id: int, db: Session = Depends(get_db)):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required")
        
    credential = db.query(models.Credential).filter(
        models.Credential.id == credential_id,
        models.Credential.tenant_id == tenant_id
    ).first()
    
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
        
    db.delete(credential)
    db.commit()
    return {"detail": "Credential deleted successfully"}
