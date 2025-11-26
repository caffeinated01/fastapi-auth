from fastapi import HTTPException, status
from sqlmodel import Session

from app.crud import user as user_crud
from app.schemas.auth import UserCreate


def check_user_exists(user_create: UserCreate, db: Session):
    if user_crud.get_user_by_email(db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with the email {user_create.email} already exists",
        )

    if user_crud.get_user_by_username(db, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with the username {user_create.username} already exists",
        )
