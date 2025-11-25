from fastapi import APIRouter

from app.schemas.auth import UserCreate, UserPublic

router = APIRouter()


@router.post("/users", response_model=UserPublic)
async def create_user(user: UserCreate):

    # user creation logic here

    return UserPublic(id=123, username=user.username, email=user.email)
