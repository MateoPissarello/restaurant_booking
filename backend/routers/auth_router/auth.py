from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as response_status
from utils.jwt_handler import create_access_token
from database import get_db
from sqlalchemy.orm import Session
from utils.login_logic import base_login
from fastapi import Body
from schemas.auth_schemas import UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=response_status.HTTP_200_OK)
async def login(data: UserLogin = Body(...), db: Session = Depends(get_db)):
    try:
        user_data = base_login(db, data)
    except HTTPException as e:
        if e.status_code == response_status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        elif e.status_code == response_status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=response_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
    access_token = create_access_token(data=user_data.model_dump())
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/admin/login", status_code=response_status.HTTP_200_OK)
async def admin_login(data: UserLogin = Body(...), db: Session = Depends(get_db)):
    try:
        user_data = base_login(db, data)
    except HTTPException as e:
        if e.status_code == response_status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        elif e.status_code == response_status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=response_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
    if user_data.role != "admin":
        raise HTTPException(
            status_code=response_status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource",
        )
    access_token = create_access_token(data=user_data.model_dump())
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
