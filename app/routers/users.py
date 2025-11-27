from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated

from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.auth import UserCreate, UserPublic
from app.db.database import SessionDep
from app.crud import user as user_crud
from app.utils.validation import check_user_exists

router = APIRouter()


@router.post("/", response_model=UserPublic)
async def create_user(user_create: UserCreate, db: SessionDep):
    # raise error if email or username already exist
    check_user_exists(user_create, db)

    user = user_crud.create_user(db, user_create)

    return UserPublic.model_validate(user, from_attributes=True)


@router.get("/me", response_model=UserPublic)
async def fetch_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.get("/{username}", response_model=UserPublic)
async def fetch_user_by_username(username: str, db: SessionDep):
    user = user_crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserPublic.model_validate(user, from_attributes=True)
