from fastapi import APIRouter
from typing_extensions import Annotated

from app.schemas.auth import UserCreate, UserPublic
from app.db.database import SessionDep
from app.crud import user as user_crud
from app.utils.validation import check_user_exists

router = APIRouter()


@router.post("/users", response_model=UserPublic)
async def create_user(user_create: UserCreate, db: SessionDep):
    # raise error if email or username already exist
    check_user_exists(user_create, db)

    user = user_crud.create_user(db, user_create)

    return UserPublic.model_validate(user, from_attributes=True)
