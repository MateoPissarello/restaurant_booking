from pydantic import BaseModel, Field
from datetime import time


class CreateScheduleBase(BaseModel):
    restaurant_id: int = Field(..., title="Restaurant ID", description="ID of the restaurant")
    day: str = Field(..., title="Day", description="Day of the week")
    opening_hour: time = Field(..., title="Opening Time", description="Opening time of the restaurant")
    closing_hour: time = Field(..., title="Closing Time", description="Closing time of the restaurant")


class RetrieveScheduleBase(BaseModel):
    schedule_id: int = Field(..., title="Schedule ID", description="ID of the schedule")
    restaurant_id: int = Field(..., title="Restaurant ID", description="ID of the restaurant")
    day: str = Field(..., title="Day", description="Day of the week")
    opening_hour: time = Field(..., title="Opening Time", description="Opening time of the restaurant")
    closing_hour: time = Field(..., title="Closing Time", description="Closing time of the restaurant")

    model_config = {"from_attributes": True}
