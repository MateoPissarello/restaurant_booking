from fastapi import HTTPException
from fastapi import status as response_status
from utils.password_hasher import Hash
from sqlalchemy.orm import Session
from models import User
from schemas.auth_schemas import UserLogin, TokenData


def base_login(db: Session, data: UserLogin):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=response_status.HTTP_404_NOT_FOUND, detail="User not found")
    hash = Hash()
    if not hash.verify_password(data.password, user.password):
        raise HTTPException(status_code=response_status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_data = TokenData(
        sub=str(user.user_id),
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role.value,
    )
    return user_data
