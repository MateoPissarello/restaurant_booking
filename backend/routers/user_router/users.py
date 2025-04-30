from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi import status as status_code

from schemas.user_schemas import CreateUserBase, RetrieveUserBase, UpdateUserBase, UpdateUserBaseAdmin
from utils.password_hasher import Hash
from database import get_db
from sqlalchemy.orm import Session
from models import User
from daos.UserDAO import UserDAO
from schemas.auth_schemas import TokenData
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user

hash = Hash()

admin_only = RoleChecker(allowed_roles=["admin"])
client_or_admin = RoleChecker(allowed_roles=["admin", "client"])


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=RetrieveUserBase, status_code=status_code.HTTP_201_CREATED)
async def create_user(user: CreateUserBase = Body(...), db: Session = Depends(get_db)) -> RetrieveUserBase:
    """
    Create a new user in the database.
    """
    user_data = User(**user.model_dump(exclude_unset=True))
    user_data.password = hash.get_password_hash(user.password)
    dao = UserDAO(db)

    try:
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=status_code.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user_data = dao.create_user(user_data)
        return user_data

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/get/my_info", response_model=RetrieveUserBase, status_code=status_code.HTTP_200_OK)
async def get_user_info(
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
    db: Session = Depends(get_db),
) -> RetrieveUserBase:
    """
    Get the current user's information.
    """
    dao = UserDAO(db)
    user_info = dao.get_user(current_user.user_id)
    if not user_info:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")
    return user_info


@router.get("/get/{user_id}", response_model=RetrieveUserBase, status_code=status_code.HTTP_200_OK)
async def get_user(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
    db: Session = Depends(get_db),
) -> RetrieveUserBase:
    """
    Get a user's information by user ID.
    """
    dao = UserDAO(db)
    user_info = dao.get_user(user_id)
    if not user_info:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")
    return user_info


@router.get("/get_all", response_model=list[RetrieveUserBase], status_code=status_code.HTTP_200_OK)
async def get_all_users(
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
    db: Session = Depends(get_db),
) -> list[RetrieveUserBase]:
    """
    Get all users in the database.
    """
    dao = UserDAO(db)
    users = dao.list_users()
    if not users:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="No users found")
    return users


@router.patch("/update/my_profile", response_model=RetrieveUserBase, status_code=status_code.HTTP_200_OK)
async def update_user(
    update_data: UpdateUserBase = Body(...),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
    db: Session = Depends(get_db),
) -> RetrieveUserBase:
    """
    Update the current user's information.
    """
    dao = UserDAO(db)
    user_info = dao.get_user(current_user.user_id)
    if not user_info:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")
    if update_data.password:
        update_data.password = hash.get_password_hash(update_data.password)

    update_data_dict = update_data.model_dump(exclude_unset=True)
    updated_user = dao.update_user(current_user.user_id, update_data_dict)
    return updated_user


@router.patch("/update/user/{user_id}", response_model=RetrieveUserBase, status_code=status_code.HTTP_200_OK)
async def update_user_admin(
    user_id: int,
    update_data: UpdateUserBaseAdmin = Body(...),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
    db: Session = Depends(get_db),
) -> RetrieveUserBase:
    """
    Update the current user's information.
    """
    dao = UserDAO(db)
    user_info = dao.get_user(user_id)
    update_data_dict = update_data.model_dump(exclude_unset=True)
    if not user_info:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")
    if update_data.password:
        update_data.password = hash.get_password_hash(update_data.password)
    updated_user = dao.update_user(current_user.user_id, update_data_dict)
    return updated_user


@router.delete("/delete/my_profile", status_code=status_code.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete the current user's account.
    """
    dao = UserDAO(db)
    user_info = dao.get_user(current_user.user_id)
    if not user_info:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")
    dao.delete_user(current_user.user_id)


@router.delete("/delete/user/{user_id}", status_code=status_code.HTTP_204_NO_CONTENT)
async def delete_user_admin(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a user's account by user ID.
    """
    dao = UserDAO(db)
    user_info = dao.get_user(user_id)
    if not user_info:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")
    dao.delete_user(user_id)
    return {"detail": "User deleted successfully"}
