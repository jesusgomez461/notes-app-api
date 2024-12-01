from pydantic import BaseModel, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    document: str
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    document: str
    full_name: str
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True
