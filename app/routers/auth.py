from typing_extensions import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.schemas.auth import Token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()]):

    # login logic here

    return {"access_token": "example", "token_type": "bearer"}
