from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone

from app.models.token import RefreshToken
from app.models.user import User
from app.schemas.auth import Token
from app.utils.auth import create_refresh_token
from app.config import settings


def store_refresh_token(session: Session, user: User):
    refresh_token, expires_at = create_refresh_token(
        data={"sub": user.username}
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
