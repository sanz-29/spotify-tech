from pydantic import BaseModel
from typing import Literal


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class AdminUserUpdate(BaseModel):
    username: str
    email: str
    role: Literal["user", "artist", "admin"]


class UserLogin(BaseModel):
    username: str
    password: str