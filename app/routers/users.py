from fastapi import APIRouter

from app.schemas.auth import UserWrite, UserRead

router = APIRouter()


@router.post("/users", response_model=UserRead)
async def create_user(user: UserWrite):

    # user creation logic here

    return UserRead(username=user.username, email=user.email)
