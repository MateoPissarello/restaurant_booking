from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi import status as response_status
from daos.ScheduleDAO import ScheduleDAO
from models import Schedule
from sqlalchemy.orm import Session
from schemas.auth_schemas import TokenData
from utils.get_current_user import get_current_user
from utils.RoleChecker import RoleChecker
from database import get_db
from utils.restaurant_utils import validate_restaurant_existence
from typing import List
from schemas.schedule_schemas import CreateScheduleBase, RetrieveScheduleBase

router = APIRouter(prefix="/schedule", tags=["Schedule"])

admin_only = RoleChecker(allowed_roles=["admin"])
client_or_admin = RoleChecker(allowed_roles=["admin", "client"])


@router.post("/create", status_code=response_status.HTTP_201_CREATED)
async def create_schedule(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
    schedule: CreateScheduleBase = Body(...),
):
    dao = ScheduleDAO(db)
    try:
        schedule = Schedule(**schedule.model_dump(exclude_unset=True))
        create_schedule = dao.create_schedule(schedule)
        return create_schedule
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get/{restaurant_id}", status_code=response_status.HTTP_200_OK, response_model=List[RetrieveScheduleBase])
async def get_schedule_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
):
    dao = ScheduleDAO(db)
    try:
        restaurant = validate_restaurant_existence(restaurant_id, db)
        if not restaurant:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        schedule = dao.get_schedule_by_restaurant(restaurant_id)
        if not schedule:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Schedule not found",
            )
        return schedule
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


@router.delete("/delete/{schedule_id}", status_code=response_status.HTTP_200_OK)
async def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
):
    dao = ScheduleDAO(db)
    try:
        schedule = dao.get_schedule(schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Schedule not found",
            )
        dao.delete_schedule(schedule_id)
        return {"detail": "Schedule deleted successfully"}
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
