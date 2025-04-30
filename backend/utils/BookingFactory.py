from abc import ABC, abstractmethod
from daos.BookingDAO import BookingDao
from daos.RestaurantDAO import RestaurantDAO
from daos.TableDAO import TableDAO
from daos.ScheduleDAO import ScheduleDAO
from fastapi import HTTPException, status
from models import Booking
from sqlalchemy.orm import Session
from typing import Dict


class BookingCreator(ABC):  # Interfaz para el creador de reservas
    """
    Interfaz abstracta para la creación de reservas. Define el método
    que las clases concretas deben implementar.
    """

    @abstractmethod
    def create_booking(self, booking_data: Dict, user_id: int) -> Booking:
        """
        Crea una reserva.

        Args:
            booking_data (dict): Datos para la reserva.
            user_id (int): ID del usuario que realiza la reserva.

        Returns:
            Booking: La reserva creada.

        Raises:
            NotImplementedError: Si el método no está implementado
                                 en una clase concreta.
        """
        raise NotImplementedError("Subclasses must implement create_booking method")


class StandardBookingCreator(BookingCreator):
    """
    Implementación concreta del creador de reservas para el flujo
    estándar de creación.  Esta es tu BookingFactory adaptada.
    """

    def __init__(self, db: Session):
        """
        Inicializa el creador de reservas estándar.

        Args:
            db (Session): La sesión de la base de datos de SQLAlchemy.
        """
        self.db = db
        self.booking_dao = BookingDao(db)
        self.restaurant_dao = RestaurantDAO(db)
        self.table_dao = TableDAO(db)
        self.schedule_dao = ScheduleDAO(db)

    def create_booking(self, booking_data: Dict, user_id: int) -> Booking:
        """
        Crea una reserva estándar con validaciones.

        Args:
            booking_data (dict): Datos para la reserva.
            user_id (int): ID del usuario que realiza la reserva.

        Returns:
            Booking: La reserva creada.

        Raises:
            HTTPException: Si alguna de las validaciones falla.
        """
        booking_data["user_id"] = user_id
        booking = Booking(**booking_data)

        # Validaciones
        restaurant = self.restaurant_dao.get_restaurant(booking.restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        table = self.table_dao.get_table(booking.table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found",
            )

        if table.capacity < booking.number_of_people:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table capacity is less than the number of people",
            )

        if not self.table_dao.get_table_in_restaurant_by_table_id(
            restaurant_id=booking.restaurant_id,
            table_id=booking.table_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found in the restaurant",
            )

        if self.booking_dao.is_table_reserved(
            restaurant_id=booking.restaurant_id,
            table_id=booking.table_id,
            date=booking.date,
            start_time=booking.start_time,
            end_time=booking.end_time,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table is already reserved for the selected time",
            )

        if not self.schedule_dao.is_restaurant_open(
            restaurant_id=booking.restaurant_id,
            date=booking.date,
            start_hour=booking.start_time,
            end_hour=booking.end_time,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant is not open at the selected time",
            )

        return self.booking_dao.create_booking(booking)
