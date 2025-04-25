from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Any
from database.

class CreateUserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    role: str = Field(..., min_length=1, max_length=50)

    @model_validator(mode="before")
    @classmethod
    def check_role(cls, data: Any) -> Any:
        if data.role not in ["client", "admin"]:
            raise ValueError("Role must be either 'client' or 'admin'")
        return data
    

