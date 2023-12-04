from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Store
from .schemas import *
from typing import List
from datetime import datetime


async def crud_get_all_stores(schema: str, session: AsyncSession = Depends(get_async_session)) -> List[StoreList]:
    query = select(Store).where(
        Store.deleted_flag != True).order_by(Store.id.desc()).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    stores = result.scalars().all()
    return stores


async def crud_get_one_stores(store_id: int, schema: str, session: AsyncSession = Depends(get_async_session)) -> List[StoreList]:
    query = select(Store).where(
        Store.deleted_flag != True, Store.id == store_id).order_by(Store.id.desc()).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    stores = result.scalar()
    return stores


async def crud_create_new_store(schema: str, data: StoreCreate, user_id: int, session: AsyncSession = Depends(get_async_session)) -> List[StoreCreate]:
    # store_data = data.dict()
    # Устанавливаем created_by из текущего пользователя
    # store_data["created_by"] = user_id
    stmt = insert(Store).values(**data.dict(), user_id=user_id, created_by=user_id
                                ).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'date': data}


async def crud_update_store(schema: str, user_id: int, store_id: int, data: StoreUpdate, session: AsyncSession = Depends(get_async_session)) -> List[StoreUpdate]:
    stmt = update(Store).where(
        Store.id == store_id).values(**data.dict(), updated_by=user_id).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", 'date': data}


async def crud_change_delete_flag_store(schema: str, user_id: int, store_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Store).where(Store.id == store_id).values(
        deleted_flag=~Store.deleted_flag,
        deleted_at=datetime.now(),
        deleted_by=user_id).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"message": f"Статус для deleted_flag изменен"}


# async def crud_update_store_field(schema: str, store_id: int, user_id: int, checkbox: str, session: AsyncSession = Depends(get_async_session)):
#     stmt = update(Store).where(Store.id == store_id).values(
#         availability=~Store.availability,
#         updated_at=datetime.now(),
#         updated_by=user_id).execution_options(schema_translate_map={None: schema})
#     await session.execute(stmt)
#     await session.commit()
#     return {"message": f"Статус для {checkbox} изменен"}


async def crud_delete_store(schema: str, store_id: int, session: Session = Depends(get_async_session)):
    try:
        stmt = delete(Store).where(Store.id == store_id).execution_options(
            schema_translate_map={None: schema})
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": f"Магазин, c id {store_id}, успешно удалена."}
    except IntegrityError as e:
        raise HTTPException(
            status_code=400, detail="Удаление этого магазина невозможно, так как на нее ссылаются продукты.")
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
