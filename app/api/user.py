from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.security import hash_password, verify_password
from app.auth import create_access_token
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if user is None:
        return {
            "message": "Invalid username or password"
        }

    if not verify_password(
        user_data.password,
        user.password
    ):
        return {
            "message": "Invalid username or password"
        }

    access_token = create_access_token({
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    })

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }

@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "Authenticated user",
        "user": current_user
    }