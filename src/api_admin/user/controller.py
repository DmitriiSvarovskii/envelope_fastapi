from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateSchema, CreateTable

from src.database import get_async_session
from src.api_admin.models import (
    Store, Category,
    Subcategory, Product,
    Customer, Cart,
    Order, OrderDetail,
    Unit, User
)
from .schemas import UserCreate
from ..models import model_for_new_schema


tables_to_create = [Store.__table__, Category.__table__,
                    Subcategory.__table__, Product.__table__,
                    Customer.__table__, Cart.__table__, Order.__table__,
                    OrderDetail.__table__,]


async def create_new_unit(
    schema: str,
    session: AsyncSession = Depends(get_async_session)
):
    unit_dict = [{'name': 'шт'}, {'name': 'порц'},
                 {'name': 'мл'}, {'name': 'л'}]
    stmt = insert(Unit).values(unit_dict).execution_options(
        schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()


async def check_duplication(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    existing_user_data = result.scalar()
    if existing_user_data:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем пользователя уже существует!"
        )


# async def create_new_schema_and_table(
    # user_data: UserCreate,
    # session: AsyncSession = Depends(get_async_session)
    # ):
async def create_new_schema_and_table(
    user_data: str,
    session: AsyncSession = Depends(get_async_session)
):
    await session.execute(CreateSchema(user_data))
    for table in model_for_new_schema:
        await session.execute(
            CreateTable(table).execution_options(
                schema_translate_map={None: user_data}
            ))
    await session.commit()
