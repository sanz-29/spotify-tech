from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import verify_token
from app.database import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)

    user_id = payload.get("user_id") if payload else None
    if user_id is None:
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Invalid or expired token"
        )

    return user


def require_user(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user


def require_artist(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role not in {"artist", "admin"}:
        raise HTTPException(
            status_code=403,
            detail="Artist role required"
        )

    return current_user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin role required"
        )

    return current_user