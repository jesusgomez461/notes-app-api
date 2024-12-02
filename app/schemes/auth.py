from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    document: str
    full_name: str
    email: EmailStr


class UserCreate(BaseModel):
    document: str
    full_name: str
    email: EmailStr
    password: str

    @field_validator('document')
    def validate_document(cls, value):
        if not value.isdigit():
            raise ValueError("The document must contain only numbers.")
        return value


class UserResponse(BaseModel):
    id: int
    document: str
    full_name: str
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True
