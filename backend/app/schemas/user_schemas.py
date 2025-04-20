from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=50)
    role: str = Field(..., min_length=5, max_length=20)
    phone_number: str = Field(..., min_length=10, max_length=15)
    company_name: Optional[str] = Field(None, min_length=2, max_length=100)
    company_address: Optional[str] = Field(None)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    company_name: Optional[str] = None
    company_address: Optional[str] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


