from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated
from src.secure import oauth2_scheme
from src.api_admin.models import User
from .schemas import UserCreate

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.secure import pwd_context
from src.database import engine
from sqlalchemy.schema import CreateSchema, CreateTable
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete, text
from src.api_admin.models import User, Product, Category, Subcategory, Unit
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session, metadata
from typing import List, Annotated
from src.secure import apikey_scheme
from src.secure import pwd_context
from .db_schema import *
from src.database import Base
from .crud import *


tables_to_create = [Category.__table__,
                    Subcategory.__table__, Unit.__table__, Product.__table__]


async def create_new_unit(schema: str, session: AsyncSession = Depends(get_async_session)):
    unit_dict = [{'name': 'шт'}, {'name': 'порц'},
                 {'name': 'мл'}, {'name': 'л'}]
    stmt = insert(Unit).values(unit_dict).execution_options(
        schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()


async def check_duplication(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    existing_user_data = result.scalar()
    if existing_user_data:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем пользователя уже существует!"
        )


async def create_new_schema_and_table(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    await session.execute(CreateSchema(user_data.username))
    for table in tables_to_create:
        await session.execute(
            CreateTable(table).execution_options(schema_translate_map={None: user_data.username}))
    await session.commit()


# async def register_new_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
#     await check_duplication(user_data=user_data, session=session)
#     create_user = await crud_register_new_user(user_data=user_data, session=session)
#     await create_new_schema_and_table(user_data=user_data, session=session)
#     await create_new_unit(schema=user_data.username, session=session)
#     return create_user


# async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(User).filter(User.username == user_data.username))
#     existing_user = result.scalar()

#     if existing_user:
#         raise HTTPException(
#             status_code=400,
#             detail="User with this email already exists!"
#         )

#     # Создаем нового пользователя
#     user = User(username=user_data.username)
#     user.hashed_password = pwd_context.hash(user_data.hashed_password)
#     # Добавляем пользователя в сессию
#     session.add(user)
#     # Коммитим изменения
#     await session.commit()
#     return {
#         "id": user.id,
#         "username": user.username,
#     }


# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
#     user = await session.execute(User.__table__.select().where(User.token_bot == token))
#     user = user.scalar()
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
