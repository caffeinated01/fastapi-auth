from fastapi import status, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import ValidationError
from uuid import uuid4

from app.models.token import RefreshToken
from app.models.user import User
from app.schemas.auth import TokenPayload
from app.utils.auth import create_refresh_token
from app.config import settings


def store_refresh_token(session: Session, user: User) -> RefreshToken:
    refresh_token, expires_at = create_refresh_token(
        data={
            "sub": user.username,
            "jti": str(uuid4())
        }
    )

    if not user.id:
        raise ValueError("User ID cannot be None")

    token = RefreshToken(
        token=refresh_token,
        expires_at=expires_at,
        user_id=user.id
    )

    session.add(token)
    session.commit()
    session.refresh(token)

    return token


def rotate_refresh_token(session: Session, refresh_token: str) -> tuple[RefreshToken, User]:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        token_payload = TokenPayload(**payload)

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    token = session.exec(select(RefreshToken).where(
        RefreshToken.token == refresh_token)).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",  # no token found
        )

    if token.revoked_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",  # token revoked
        )

    token_expires_at = token.expires_at
    if token_expires_at.tzinfo is None:
        token_expires_at = token_expires_at.replace(tzinfo=timezone.utc)

    if token_expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",  # token expired
        )

    token.revoked_at = datetime.now(timezone.utc)
    session.add(token)

    username = token_payload.sub
    user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",  # user not found
        )

    new_refresh_token = store_refresh_token(
        session=session,
        user=user
    )

    session.commit()

    return new_refresh_token, user
