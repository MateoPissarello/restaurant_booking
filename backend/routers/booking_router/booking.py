from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status as response_status
from fastapi import HTTPException
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from schemas.auth_schemas import TokenData
from schemas.booking_schemas import CreateBookingBase
from database import get_db
from daos.TableDAO import TableDAO
from daos.BookingDAO import BookingDao
from daos.ScheduleDAO import ScheduleDAO
from daos.RestaurantDAO import RestaurantDAO
from models import Booking

router = APIRouter(prefix="/booking", tags=["Booking"])

admin_only = RoleChecker(allowed_roles=["admin"])
client_or_admin = RoleChecker(allowed_roles=["admin", "client"])


@router.post("/create", status_code=response_status.HTTP_201_CREATED, response_model=CreateBookingBase)
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


# @router.post("/create", status_code=response_status.HTTP_201_CREATED, response_model=RetrieveRestaurantBase)
# async def create_restaurant(
#     restaurant: CreateRestaurantBase,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
#     role_checker: RoleChecker = Depends(admin_only),
# ):
#     restaurant = Restaurant(**restaurant.model_dump(exclude_unset=True))
#     dao = RestaurantDAO(db)
#     try:
#         if dao.get_restaurant_by_name(restaurant.name):
#             raise HTTPException(
#                 status_code=response_status.HTTP_400_BAD_REQUEST,
#                 detail="Restaurant with this name already exists",
#             )
#         create_restaurant = dao.create_restaurant(restaurant)
#         return create_restaurant
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )


# @router.get("/get_all", status_code=response_status.HTTP_200_OK, response_model=List[RetrieveRestaurantBase])
# async def get_all_restaurants(
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
#     role_checker: RoleChecker = Depends(client_or_admin),
# ) -> List[RetrieveRestaurantBase]:
#     dao = RestaurantDAO(db)
#     try:
#         restaurants = dao.list_restaurants()
#         return restaurants
#     except Exception as e:
#         raise HTTPException(
#             status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )


# @router.get("/get/{restaurant_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveRestaurantBase)
# async def get_restaurant_by_id(
#     restaurant_id: int,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
#     role_checker: RoleChecker = Depends(client_or_admin),
# ) -> RetrieveRestaurantBase:
#     dao = RestaurantDAO(db)
#     try:
#         restaurant = dao.get_restaurant(restaurant_id)
#         if not restaurant:
#             raise HTTPException(
#                 status_code=response_status.HTTP_404_NOT_FOUND,
#                 detail="Restaurant not found",
#             )
#         return restaurant
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )


# @router.patch("/update/{restaurant_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveRestaurantBase)
# async def update_restaurant(
#     restaurant_id: int,
#     updated_data: UpdateRestaurantBase,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
#     role_checker: RoleChecker = Depends(admin_only),
# ) -> RetrieveRestaurantBase:
#     dao = RestaurantDAO(db)
#     try:
#         restaurant = dao.update_restaurant(restaurant_id, updated_data.model_dump(exclude_unset=True))
#         if not restaurant:
#             raise HTTPException(
#                 status_code=response_status.HTTP_404_NOT_FOUND,
#                 detail="Restaurant not found",
#             )
#         return restaurant
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )


# @router.delete("/delete/{restaurant_id}", status_code=response_status.HTTP_200_OK)
# async def delete_restaurant(
#     restaurant_id: int,
#     db: Session = Depends(get_db),
#     current_user: TokenData = Depends(get_current_user),
#     role_checker: RoleChecker = Depends(admin_only),
# ) -> dict:
#     dao = RestaurantDAO(db)
#     try:
#         if not dao.delete_restaurant(restaurant_id):
#             raise HTTPException(
#                 status_code=response_status.HTTP_404_NOT_FOUND,
#                 detail="Restaurant not found",
#             )
#         return {"detail": "Restaurant deleted successfully"}
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e),
#         )
