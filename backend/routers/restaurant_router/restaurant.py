from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status as response_status
from schemas.restaurant_schemas import CreateRestaurantBase, RetrieveRestaurantBase, UpdateRestaurantBase
from fastapi import HTTPException
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from schemas.auth_schemas import TokenData
from database import get_db
from daos.RestaurantDAO import RestaurantDAO
from models import Restaurant
from typing import List

router = APIRouter(prefix="/restaurant", tags=["Restaurant"])

admin_only = RoleChecker(allowed_roles=["admin"])
client_or_admin = RoleChecker(allowed_roles=["admin", "client"])


@router.post("/create", status_code=response_status.HTTP_201_CREATED, response_model=RetrieveRestaurantBase)
async def create_restaurant(
    restaurant: CreateRestaurantBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
):
    restaurant = Restaurant(**restaurant.model_dump(exclude_unset=True))
    dao = RestaurantDAO(db)
    try:
        if dao.get_restaurant_by_name(restaurant.name):
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Restaurant with this name already exists",
            )
        create_restaurant = dao.create_restaurant(restaurant)
        return create_restaurant
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get_all", status_code=response_status.HTTP_200_OK, response_model=List[RetrieveRestaurantBase])
async def get_all_restaurants(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> List[RetrieveRestaurantBase]:
    dao = RestaurantDAO(db)
    try:
        restaurants = dao.list_restaurants()
        return restaurants
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get/{restaurant_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveRestaurantBase)
async def get_restaurant_by_id(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> RetrieveRestaurantBase:
    dao = RestaurantDAO(db)
    try:
        restaurant = dao.get_restaurant(restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        return restaurant
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/update/{restaurant_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveRestaurantBase)
async def update_restaurant(
    restaurant_id: int,
    updated_data: UpdateRestaurantBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
) -> RetrieveRestaurantBase:
    dao = RestaurantDAO(db)
    try:
        restaurant = dao.update_restaurant(restaurant_id, updated_data.model_dump(exclude_unset=True))
        if not restaurant:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        return restaurant
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/delete/{restaurant_id}", status_code=response_status.HTTP_200_OK)
async def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
) -> dict:
    dao = RestaurantDAO(db)
    try:
        if not dao.delete_restaurant(restaurant_id):
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        return {"detail": "Restaurant deleted successfully"}
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
