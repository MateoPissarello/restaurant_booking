from fastapi import Depends, HTTPException, status
from schemas.auth_schemas import TokenData
from get_current_user import get_current_user  # función que decodifica el JWT y retorna el usuario


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
