from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi import status as status_code

from schemas.user_schemas import CreateUserBase, RetrieveUserBase
from utils.password_hasher import Hash
from database import get_db
from sqlalchemy.orm import Session
from models import User

hash = Hash()


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=RetrieveUserBase, status_code=status_code.HTTP_201_CREATED)
async def create_user(user: CreateUserBase = Body(...), db: Session = Depends(get_db)) -> RetrieveUserBase:
    """
    Create a new user in the database.
    """
    user_data = User(**user.model_dump(exclude_unset=True))
    user_data.password = hash.get_password_hash(user.password)
    try:
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=status_code.HTTP_400_BAD_REQUEST, detail="Email already registered")
        db.add(user_data)
        db.commit()
        db.refresh(user_data)

        return user_data

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
