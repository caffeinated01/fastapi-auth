from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated

from app.schemas.auth import UserCreate, UserPublic
from app.db.database import SessionDep
from app.crud import user as user_crud

router = APIRouter()


@router.post("/users", response_model=UserPublic)
async def create_user(user_create: UserCreate, db: SessionDep):

    user = user_crud.get_user_by_email(db, user_create.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with the email {user_create.email} already exists",
        )

    user = user_crud.create_user(db, user_create)

    return UserPublic.model_validate(user, from_attributes=True)
