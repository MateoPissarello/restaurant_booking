from pydantic import BaseModel, Field
from datetime import time
from datetime import date as date_type


class CreateBookingBase(BaseModel):
    table_id: int = Field(..., title="Table ID", description="ID of the table")
    restaurant_id: int = Field(..., title="Restaurant ID", description="ID of the restaurant")
    date: date_type = Field(..., title="Date", description="Date of the booking in YYYY-MM-DD format")
    start_time: time = Field(..., title="Start Time", description="Start time of the booking")
    end_time: time = Field(..., title="End Time", description="End time of the booking")
    number_of_people: int = Field(..., title="Number of People", description="Number of people for the booking")


class RetrieveBookingBase(BaseModel):
    booking_id: int = Field(..., title="Booking ID", description="ID of the booking")
    user_id: int = Field(..., title="User ID", description="ID of the user")
    table_id: int = Field(..., title="Table ID", description="ID of the table")
    restaurant_id: int = Field(..., title="Restaurant ID", description="ID of the restaurant")
    date: date_type = Field(..., title="Date", description="Date of the booking in YYYY-MM-DD format")
    start_time: time = Field(..., title="Start Time", description="Start time of the booking")
    end_time: time = Field(..., title="End Time", description="End time of the booking")
    number_of_people: int = Field(..., title="Number of People", description="Number of people for the booking")

    model_config = {"from_attributes": True}
