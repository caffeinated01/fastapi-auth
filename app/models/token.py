from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func


if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(index=True, unique=True)
    expires_at: datetime
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        )
    )
    revoked_at: Optional[datetime] = Field(default=None)

    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="refresh_tokens")
