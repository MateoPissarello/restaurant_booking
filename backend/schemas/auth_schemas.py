from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserLogin(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class TokenData(BaseModel):
    sub: str
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: Literal["admin", "client"]
