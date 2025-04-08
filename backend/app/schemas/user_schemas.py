from pydantic import BaseModel, EmailStr
from typing import Annotated


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, 8, 100]
    full_name: Annotated[str, 2, 50]
    role: Annotated[str, 5, 20]
    phone_number: Annotated[str, 10, 15]

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
