import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.future import select
from strawberry.permission import BasePermission


from db import AsyncSessionLocal
from models import User
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
        Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    """
        Authenticate a user by username and password.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(username=username))
        user = result.scalars().first()
        if not user:
            return None
        if user.password != password:
            return None
        return user


async def get_user_from_token(token: str):
    """
        Decode the JWT token and retrieve the user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
    except Exception:
        return None
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(username=username))
        return result.scalars().first()



class IsAuthenticated(BasePermission):
    """
    Permission class to check if user is authenticated.
    """
    message = "Authentication required"

    def has_permission(self, source, info, **kwargs):
        context = getattr(info, "context", {})
        return bool(context and context.get("current_user"))
