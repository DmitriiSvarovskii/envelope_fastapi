from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated
from src.secure import oauth2_scheme
from .models import User
from .schemas import UserCreate

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from .models import User
from .schemas import UserBase, UserCreate, UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from src.secure import pwd_context


async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).filter(User.username == user_data.username))
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists!"
        )

    # Создаем нового пользователя
    user = User(username=user_data.username)
    user.hashed_password = pwd_context.hash(user_data.hashed_password)
    # Добавляем пользователя в сессию
    session.add(user)
    # Коммитим изменения
    await session.commit()
    return {
        "id": user.id,
        "username": user.username,
    }


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(User.__table__.select().where(User.token_bot == token))
    user = user.scalar()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
