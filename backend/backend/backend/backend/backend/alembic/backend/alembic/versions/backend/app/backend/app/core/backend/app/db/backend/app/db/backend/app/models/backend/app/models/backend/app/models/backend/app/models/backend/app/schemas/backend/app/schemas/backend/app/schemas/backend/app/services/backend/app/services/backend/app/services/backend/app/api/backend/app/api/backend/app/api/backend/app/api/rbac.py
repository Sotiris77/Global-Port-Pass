from fastapi import Depends, HTTPException, status
from app.api.deps import get_current_user

def require_role(*allowed_roles: str):
    def _deps(user = Depends(get_current_user)):
        if user.role not in allowed_roles and not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return _deps
