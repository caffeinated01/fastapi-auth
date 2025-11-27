from typing_extensions import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.crud import user as user_crud
from app.crud import token as token_crud
from app.db.database import SessionDep
from app.schemas.auth import Token
from app.utils.auth import verify_password, create_access_token
from app.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):

    user = user_crud.get_user_by_username(session, form.username)

    if (not user) or (not verify_password(form.password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = token_crud.create_token(session, user)

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token.token,
    )
