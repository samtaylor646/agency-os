from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import json

from .database import SessionLocal
from .audit import log_audit_event
from .auth import decode_access_token

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Only log mutating actions
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            tenant_id = request.headers.get("X-Tenant-ID")
            if tenant_id:
                try:
                    tenant_id_int = int(tenant_id)
                    user_id = None
                    auth_header = request.headers.get("Authorization")
                    if auth_header and auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]
                        payload = decode_access_token(token)
                        if payload and "sub" in payload:
                            # Usually sub is email, we'd need user ID, but we just log email or None for now
                            user_email = payload["sub"]
                            db = SessionLocal()
                            from .models import User
                            user = db.query(User).filter(User.email == user_email).first()
                            if user:
                                user_id = user.id
                            db.close()
                    
                    db = SessionLocal()
                    log_audit_event(
                        db=db,
                        workspace_id=tenant_id_int,
                        action=f"{request.method} {request.url.path}",
                        user_id=user_id,
                        resource_type="API Route",
                        resource_id=request.url.path
                    )
                    db.close()
                except Exception as e:
                    print(f"Failed to log audit event: {e}")

        return response
