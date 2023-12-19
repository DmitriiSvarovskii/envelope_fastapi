from sqlalchemy.schema import CreateSchema, CreateTable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete, text
from ..models import *
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Annotated
from src.secure import pwd_context


async def crud_create_new_role(role: RolesCreate, order_status: CreateOrderStatus, unit: CreateUnit, day_of_week: CreateDayOfWeek, order_type: CreateOrderType,  session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Role).values(role.dict())
    await session.execute(stmt)
    unit_list_data = unit.dict().get('data_unit', [])
    order_type_list_data = order_type.dict().get('data_order_type', [])
    day_of_week_list_data = day_of_week.dict().get('data_day_of_week', [])
    order_status_list_data = order_status.dict().get('data_order_status', [])
    for item in day_of_week_list_data:
        stmt = insert(DayOfWeek).values(item)
        await session.execute(stmt)
    for item in unit_list_data:
        stmt = insert(Unit).values(item)
        await session.execute(stmt)
    for item in order_type_list_data:
        stmt = insert(OrderType).values(item)
        await session.execute(stmt)
    for item in order_status_list_data:
        stmt = insert(OrderStatus).values(item)
        print(stmt)
        await session.execute(stmt)
    await session.commit()
    return {"status": 201}


async def crud_create_new_store(schema: str, user_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Store).values(user_id=user_id, created_by=user_id
                                ).execution_options(schema_translate_map={None: schema}).returning(Store.id)
    result = await session.execute(stmt)
    new_store_id = result.scalar()
    await session.commit()
    return {"status": 201, "id": new_store_id, }


async def crud_create_new_store_and_bot(schema: str, data: CreateStore, token_bot: CreateBotToken, user_id: int, session: AsyncSession = Depends(get_async_session)):
    store_result = await crud_create_new_store(schema=schema, user_id=user_id, session=session)
    store_id = store_result.get("id")
    stmt_token = insert(BotToken).values(
        **token_bot.dict(), user_id=user_id, store_id=store_id)
    await session.execute(stmt_token)
    stmt = insert(StoreInfo).values(**data.dict(), store_id=store_id
                                    ).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"status": 201}


async def crud_create_new_unit(unit: CreateUnit, day_of_week: CreateDayOfWeek, order_type: CreateOrderType, session: AsyncSession = Depends(get_async_session)):
    unit_list_data = unit.dict().get('data_unit', [])

    order_type_list_data = order_type.dict().get('data_order_type', [])
    day_of_week_list_data = day_of_week.dict().get('data_day_of_week', [])
    for item in day_of_week_list_data:
        stmt = insert(DayOfWeek).values(item)
        await session.execute(stmt)
    for item in unit_list_data:
        stmt = insert(Unit).values(item)
        await session.execute(stmt)
    for item in order_type_list_data:
        stmt = insert(OrderType).values(item)
        await session.execute(stmt)

    await session.commit()
    return {"status": 201}


async def crud_create_new_category(schema: str, store_id: int, data: CategoryCreate, user_id: int, session: AsyncSession = Depends(get_async_session)):
    category_data = data.dict()
    # Устанавливаем created_by из текущего пользователя
    category_data["created_by"] = user_id
    stmt = insert(Category).values(**data.dict(), store_id=store_id, created_by=user_id
                                   ).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'date': data}


async def crud_create_new_product(store_id: int, schema: str, user_id: int,  data: ProductCreate,  session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Product).values(**data.dict(), store_id=store_id, created_by=user_id).execution_options(
            schema_translate_map={None: schema})
        await session.execute(stmt)
        await session.commit()
        return {"status": 201, }
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
