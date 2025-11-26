from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.config import settings
from app.db.database import SessionDep
from app.schemas.auth import TokenPayload
from app.crud import user as user_crud


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_access_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        token_payload = TokenPayload(**payload)

    except (JWTError, ValidationError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_payload


def get_current_user(db: SessionDep, token: TokenPayload = Depends(get_access_token)):
    user = user_crud.get_user_by_username(db, username=token.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
