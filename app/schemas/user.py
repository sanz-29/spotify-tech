from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str