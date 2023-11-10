from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.schema import CreateSchema, CreateTable

from src.database import get_async_session
from src.api_admin.models import Store, User, Product, Category, Subcategory, Unit
from .schemas import *
from .crud import *


tables_to_create = [Store.__table__, Category.__table__,
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
