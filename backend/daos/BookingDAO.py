from sqlalchemy.orm import Session
from models import Booking, User
from datetime import time
from sqlalchemy import and_
from datetime import date as dt
from typing import List


class BookingDao:
    def __init__(self, db: Session):
        self.db = db

    def get_booking(self, booking_id: int) -> Booking | None:
        booking = self.db.query(Booking).filter(Booking.booking_id == booking_id).first()
        return booking

    def create_booking(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_bookings_by_user(self, user_id: int) -> List[Booking]:
        bookings = self.db.query(Booking).filter(Booking.user_id == user_id).all()
        return bookings

    def get_booking_by_restaurant(self, restaurant_id: int) -> List[Booking]:
        bookings = self.db.query(Booking).filter(Booking.restaurant_id == restaurant_id).all()
        return bookings

    def get_bookings_by_email(self, email: str) -> List[Booking]:
        bookings = self.db.query(Booking).join(User, Booking.user_id == User.user_id).filter(User.email == email).all()
        return bookings

    def get_bookings(self) -> List[Booking]:
        bookings = self.db.query(Booking).all()
        return bookings

    def update_booking(self, booking_id: int, updated_data: dict) -> Booking | None:
        booking = self.get_booking(booking_id)
        if booking:
            for key, value in updated_data.items():
                setattr(booking, key, value)
            self.db.commit()
            self.db.refresh(booking)
            return booking
        return None

    def delete_booking(self, booking_id: int) -> bool:
        booking = self.get_booking(booking_id)
        if booking:
            self.db.delete(booking)
            self.db.commit()
            return True
        return False

    def is_table_reserved_excluding_current(
        self, booking_id, restaurant_id: int, table_id: int, date: dt, start_time: time, end_time: time
    ) -> bool:
        conflict = (
            self.db.query(Booking)
            .filter(
                Booking.restaurant_id == restaurant_id,
                Booking.table_id == table_id,
                Booking.date == date,
                and_(Booking.start_time < end_time, Booking.end_time > start_time),
            )
            .filter(Booking.booking_id != booking_id)
            .first()
        )
        return conflict is not None

    def is_table_reserved(self, restaurant_id: int, table_id: int, date: dt, start_time: time, end_time: time) -> bool:
        conflict = (
            self.db.query(Booking)
            .filter(
                Booking.restaurant_id == restaurant_id,
                Booking.table_id == table_id,
                Booking.date == date,
                and_(Booking.start_time < end_time, Booking.end_time > start_time),
            )
            .first()
        )
        return conflict is not None
