from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status as response_status
from fastapi import HTTPException
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from schemas.auth_schemas import TokenData
from schemas.booking_schemas import CreateBookingBase, RetrieveBookingBase, UpdateBookingBase
from database import get_db
from daos.TableDAO import TableDAO
from daos.BookingDAO import BookingDao
from daos.ScheduleDAO import ScheduleDAO
from daos.RestaurantDAO import RestaurantDAO
from models import Booking
from typing import List

router = APIRouter(prefix="/booking", tags=["Booking"])

admin_only = RoleChecker(allowed_roles=["admin"])
client_or_admin = RoleChecker(allowed_roles=["admin", "client"])


@router.post("/create", status_code=response_status.HTTP_201_CREATED, response_model=RetrieveBookingBase)
async def create_booking(
    booking: CreateBookingBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
):
    booking_data = booking.model_dump(exclude_unset=True)
    booking_data["user_id"] = current_user.user_id

    booking = Booking(**booking_data)

    booking_dao = BookingDao(db)
    restaurant_dao = RestaurantDAO(db)
    table_dao = TableDAO(db)
    schedule_dao = ScheduleDAO(db)
    try:
        # Check if the restaurant exists
        restaurant = restaurant_dao.get_restaurant(booking.restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        # Check if table is exists
        table = table_dao.get_table(booking.table_id)
        if not table:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Table not found",
            )

        # Check if table capacity is sufficient
        if table.capacity < booking.number_of_people:
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Table capacity is less than the number of people",
            )

        # Check if table exists in the restaurant
        if not table_dao.get_table_in_restaurant_by_table_id(
            restaurant_id=booking.restaurant_id, table_id=booking.table_id
        ):
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Table not found in the restaurant",
            )

        # Check if the table is already reserved for the selected time
        if booking_dao.is_table_reserved(
            restaurant_id=table.restaurant_id,
            table_id=booking.table_id,
            date=booking.date,
            start_time=booking.start_time,
            end_time=booking.end_time,
        ):
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Table is already reserved for the selected time",
            )

        # Check if the restaurant has a schedule for the selected date
        schedule = schedule_dao.is_restaurant_open(
            restaurant_id=booking.restaurant_id,
            date=booking.date,
            start_hour=booking.start_time,
            end_hour=booking.end_time,
        )
        if not schedule:
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Restaurant is not open at the selected time",
            )

        # Create the booking
        create_booking = booking_dao.create_booking(booking)
        return create_booking

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


@router.patch("/update/{booking_id}", status_code=response_status.HTTP_200_OK, response_model=CreateBookingBase)
async def update_booking(
    booking_id: int,
    updated_data: UpdateBookingBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> CreateBookingBase:
    booking_dao = BookingDao(db)
    table_dao = TableDAO(db)
    schedule_dao = ScheduleDAO(db)
    try:
        updated_data = updated_data.model_dump(exclude_unset=True)
        actual_booking = booking_dao.get_booking(booking_id)
        if current_user.user_id != actual_booking.user_id:
            raise HTTPException(
                status_code=response_status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this booking",
            )
        if updated_data.get("table_id") and updated_data.get("table_id") != actual_booking.table_id:
            # Check if the new table exists
            table = table_dao.get_table(updated_data["table_id"])
            if not table:
                raise HTTPException(
                    status_code=response_status.HTTP_404_NOT_FOUND,
                    detail="Table not found",
                )
            # Check if the new table is in the same restaurant
            if actual_booking.restaurant_id != table.restaurant_id:
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST,
                    detail="Table does not belong to the same restaurant",
                )

        if (
            updated_data.get("number_of_people")
            and updated_data.get("number_of_people") > actual_booking.table.capacity
        ):
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Table capacity is less than the number of people",
            )
        if updated_data.get("date") or updated_data.get("start_time") or updated_data.get("end_time"):
            # Check if the table is already reserved for the selected time

            if booking_dao.is_table_reserved_excluding_current(
                restaurant_id=actual_booking.restaurant_id,
                booking_id=booking_id,
                table_id=updated_data.get("table_id", actual_booking.table_id),
                date=updated_data.get("date", actual_booking.date),
                start_time=updated_data.get("start_time", actual_booking.start_time),
                end_time=updated_data.get("end_time", actual_booking.end_time),
            ):
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST,
                    detail="Table is already reserved for the selected time",
                )

            schedule = schedule_dao.is_restaurant_open(
                restaurant_id=actual_booking.restaurant_id,
                date=updated_data.get("date", actual_booking.date),
                start_hour=updated_data.get("start_time", actual_booking.start_time),
                end_hour=updated_data.get("end_time", actual_booking.end_time),
            )
            if not schedule:
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST,
                    detail="Restaurant is not open at the selected time",
                )

        booking = booking_dao.update_booking(booking_id, updated_data)
        if not booking:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return booking
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


@router.patch("/update/admin/{booking_id}", status_code=response_status.HTTP_200_OK, response_model=CreateBookingBase)
async def update_booking_admin(
    booking_id: int,
    updated_data: UpdateBookingBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> CreateBookingBase:
    booking_dao = BookingDao(db)
    table_dao = TableDAO(db)
    schedule_dao = ScheduleDAO(db)
    try:
        updated_data = updated_data.model_dump(exclude_unset=True)
        actual_booking = booking_dao.get_booking(booking_id)
        if updated_data.get("table_id") and updated_data.get("table_id") != actual_booking.table_id:
            # Check if the new table exists
            table = table_dao.get_table(updated_data["table_id"])
            if not table:
                raise HTTPException(
                    status_code=response_status.HTTP_404_NOT_FOUND,
                    detail="Table not found",
                )
            # Check if the new table is in the same restaurant
            if actual_booking.restaurant_id != table.restaurant_id:
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST,
                    detail="Table does not belong to the same restaurant",
                )

        if (
            updated_data.get("number_of_people")
            and updated_data.get("number_of_people") > actual_booking.table.capacity
        ):
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Table capacity is less than the number of people",
            )
        if updated_data.get("date") or updated_data.get("start_time") or updated_data.get("end_time"):
            # Check if the table is already reserved for the selected time

            if booking_dao.is_table_reserved_excluding_current(
                restaurant_id=actual_booking.restaurant_id,
                booking_id=booking_id,
                table_id=updated_data.get("table_id", actual_booking.table_id),
                date=updated_data.get("date", actual_booking.date),
                start_time=updated_data.get("start_time", actual_booking.start_time),
                end_time=updated_data.get("end_time", actual_booking.end_time),
            ):
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST,
                    detail="Table is already reserved for the selected time",
                )

            schedule = schedule_dao.is_restaurant_open(
                restaurant_id=actual_booking.restaurant_id,
                date=updated_data.get("date", actual_booking.date),
                start_hour=updated_data.get("start_time", actual_booking.start_time),
                end_hour=updated_data.get("end_time", actual_booking.end_time),
            )
            if not schedule:
                raise HTTPException(
                    status_code=response_status.HTTP_400_BAD_REQUEST,
                    detail="Restaurant is not open at the selected time",
                )

        booking = booking_dao.update_booking(booking_id, updated_data)
        if not booking:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return booking
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


@router.get("/get/my_bookings", status_code=response_status.HTTP_200_OK, response_model=List[RetrieveBookingBase])
async def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> List[RetrieveBookingBase]:
    dao = BookingDao(db)
    try:
        bookings = dao.get_bookings_by_user(current_user.user_id)
        if not bookings:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Bookings not found",
            )
        return bookings
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


@router.get("/get/{booking_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveBookingBase)
async def get_booking_by_id(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> RetrieveBookingBase:
    dao = BookingDao(db)
    try:
        booking = dao.get_booking(booking_id)
        if not booking:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return booking
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


@router.delete("/delete/admin/{booking_id}", status_code=response_status.HTTP_200_OK)
async def delete_booking_admin(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
) -> dict:
    dao = BookingDao(db)
    try:
        booking = dao.get_booking(booking_id)
        if not booking:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        dao.delete_booking(booking_id)
        return {"detail": "Booking deleted successfully"}
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


@router.delete("/delete/{booking_id}", status_code=response_status.HTTP_200_OK)
async def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> dict:
    dao = BookingDao(db)
    try:
        booking = dao.get_booking(booking_id)
        if not booking:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        if booking.user_id != current_user.user_id:
            raise HTTPException(
                status_code=response_status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this booking",
            )
        dao.delete_booking(booking_id)
        return {"detail": "Booking deleted successfully"}
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
