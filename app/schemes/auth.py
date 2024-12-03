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
    password_confirmation: str

    @field_validator('document')
    def validate_document(cls, value):
        if not value.isdigit():
            raise ValueError("The document must contain only numbers.")
        return value

    # @field_validator('password')
    # def validate_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("The password must be at least 8 characters.")
    #     return value

    # @field_validator('password_confirmation')
    # def validate_password_confirmation(cls, value, values):
    #     if 'password' in values and value != values['password']:
    #         raise ValueError(
    #             "The password and password confirmation must be the same."
    #         )
    #     return value


class UserResponse(BaseModel):
    id: int
    document: str
    full_name: str
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True
