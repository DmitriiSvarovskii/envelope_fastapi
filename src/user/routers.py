from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from .models import User
from .schemas import UserBase, UserCreate, UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List, Annotated
from src.secure import apikey_scheme
from .controller import register
from fastapi.encoders import jsonable_encoder
from src.secure import pwd_context


router = APIRouter(
    prefix="/user",
    tags=["User"])


@router.get("/", status_code=201)
async def get_all_users(access_token: Annotated[str, Depends(apikey_scheme)], session: AsyncSession = Depends(get_async_session)) -> List[UserBase]:
    query = select(User).order_by(User.id.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/register")
async def register(access_token: Annotated[str, Depends(apikey_scheme)], user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this username already exists!"
        )

    user = User(username=user_data.username)
    user.hashed_password = pwd_context.hash(user_data.hashed_password)
    session.add(user)
    await session.commit()
    return jsonable_encoder({
        "id": user.id,
        "username": user.username,
    })
