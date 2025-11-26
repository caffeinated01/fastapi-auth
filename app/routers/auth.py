from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.crud import user as user_crud
from app.db.database import SessionDep
from app.schemas.auth import Token
from app.utils.auth import get_password_hash, verify_password


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):

    user = user_crud.get_user_by_username(session, form.username)

    if (not user) or (not verify_password(form.password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return {"access_token": "example", "token_type": "bearer"}
