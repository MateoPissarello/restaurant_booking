from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateUserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=50)
    role: str = Field(..., min_length=1, max_length=50)

    @model_validator(mode="after")
    def check_role(self):
        if self.role not in ["client", "admin"]:
            raise ValueError("Role must be either 'client' or 'admin'")
        return self


class RetrieveUserBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}
