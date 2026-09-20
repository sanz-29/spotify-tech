from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class AdminUserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: Literal["user", "artist", "admin"]


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str