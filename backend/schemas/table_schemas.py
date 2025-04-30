from pydantic import BaseModel, Field
from typing import Optional


class CreateTableBase(BaseModel):
    restaurant_id: int = Field(..., description="Unique identifier for the restaurant")
    number: int = Field(..., description="Table number")
    capacity: int = Field(..., description="Seating capacity of the table")


class RetrieveTableBase(BaseModel):
    table_id: int = Field(..., description="Unique identifier for the table")
    restaurant_id: int = Field(..., description="Unique identifier for the restaurant")
    number: int = Field(..., description="Table number")
    capacity: int = Field(..., description="Seating capacity of the table")

    model_config = {"from_attributes": True}


class UpdateTableBase(BaseModel):
    number: Optional[int] = Field(None, description="Table number")
    capacity: Optional[int] = Field(None, description="Seating capacity of the table")
