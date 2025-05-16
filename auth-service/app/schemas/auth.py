from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


class Login(BaseModel):
    username: str
    password: str


class HashPassword(BaseModel):
    password: str


class ValidateToken(BaseModel):
    token: str