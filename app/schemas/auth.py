from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
    exp: int


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
