from pydantic import BaseModel, Field
from typing import Optional


class CreateRestaurantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    restaurant_type: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=15)
    address: str = Field(..., min_length=1, max_length=100)


class RetrieveRestaurantBase(BaseModel):
    restaurant_id: int
    name: str
    description: str
    restaurant_type: str
    phone_number: str
    address: str

    model_config = {"from_attributes": True}


class UpdateRestaurantBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    restaurant_type: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=1, max_length=15)
    address: Optional[str] = Field(None, min_length=1, max_length=100)
