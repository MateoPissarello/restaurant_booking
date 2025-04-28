from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Time, UniqueConstraint, Date
import enum
from database import Base


class UserRole(enum.Enum):
    client = "client"
    admin = "admin"


class days(enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
    all = "all"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.client)


class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    restaurant_type = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)


class Schedule(Base):
    __tablename__ = "schedules"
    schedule_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    day = Column(Enum(days, name="days_enum"), nullable=False)
    opening_hour = Column(Time, nullable=False)
    closing_hour = Column(Time, nullable=False)


class Table(Base):
    __tablename__ = "tables"
    table_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("restaurant_id", "number", name="unique_table_number"),)


class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "table_id", "date", name="unique_booking"),)
