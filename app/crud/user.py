from sqlmodel import Session, select

from app.models.user import User
from app.schemas.auth import UserCreate
from app.utils.auth import get_password_hash


def get_user_by_email(session: Session, email: str):
    user = session.exec(select(User).where(User.email == email)).first()

    return user


def get_user_by_username(session: Session, username: str):
    user = session.exec(select(User).where(User.username == username)).first()

    return user


def create_user(session: Session, user_create: UserCreate):
    hashed_password = get_password_hash(user_create.password)

    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
