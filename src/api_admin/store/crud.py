from sqlalchemy import literal_column
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from sqlalchemy import select, and_, join
from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, outerjoin
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.bot_management import add_new_bot
from src.database import get_async_session
from .models import *
from .schemas import *
from typing import List
from datetime import datetime


async def crud_get_all_stores(schema: str, session: AsyncSession = Depends(get_async_session)):
    query = (select(Store)
             .options(joinedload(Store.info), joinedload(Store.subscriptions))
             .order_by(Store.id.desc())).execution_options(
        schema_translate_map={None: schema})
    result = await session.execute(query)
    stores = result.scalars().all()
    return stores


async def crud_get_one_stores(store_id: int, schema: str, session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Store).
        where(Store.id == store_id).
        options(
            joinedload(Store.info),
            joinedload(Store.subscriptions),
            joinedload(Store.association).
            options(joinedload(StoreOrderTypeAssociation.order_type)))
    ).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    store = result.scalar()
    return store


async def crud_get_info_store_token(bot_token: str, session: AsyncSession = Depends(get_async_session)):
    query = select(BotToken).where(BotToken.token_bot == bot_token)
    result = await session.execute(query)
    store = result.scalar()
    return store


async def crud_get_info_store_token_all(session: AsyncSession = Depends(get_async_session)):
    query = select(BotToken)
    result = await session.execute(query)
    store = result.scalars().all()
    return store


async def read_test_many_to_many(session: AsyncSession = Depends(get_async_session)):
    query = (
        select(StoreOrderTypeAssociation).
        where(StoreOrderTypeAssociation.store_id == 1).
        options(joinedload(StoreOrderTypeAssociation.order_type)
                ).execution_options(
            schema_translate_map={None: "1"})
    )
    result = await session.execute(query)
    stores = result.scalars().all()
    return stores


async def crud_create_new_store(schema: str, user_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Store).values(user_id=user_id, created_by=user_id
                                ).execution_options(schema_translate_map={None: schema}).returning(Store.id)
    result = await session.execute(stmt)
    new_store_id = result.scalar()
    await session.commit()

    return {"status": 201, "id": new_store_id, }


async def crud_create_new_store_and_bot(schema: str, data: StoreCreate, token_bot: BotTokenCreate, user_id: int, session: AsyncSession = Depends(get_async_session)):
    store_result = await crud_create_new_store(schema=schema, user_id=user_id, session=session)
    store_id = store_result.get("id")
    await add_new_bot(token_bot.token_bot)
    await session.execute(insert(BotToken).values(**token_bot.dict(), user_id=user_id, store_id=store_id))
    await session.execute(insert(StoreInfo).values(**data.dict(), store_id=store_id
                                                   ).execution_options(schema_translate_map={None: schema}))
    await session.execute(insert(StoreSubscription).values(store_id=store_id
                                                           ).execution_options(schema_translate_map={None: schema}))
    await session.execute(insert(StorePayment).values(store_id=store_id
                                                      ).execution_options(schema_translate_map={None: schema}))
    await session.execute(insert(ServiceTextAndChat).values(store_id=store_id
                                                            ).execution_options(schema_translate_map={None: schema}))
    await session.execute(insert(LegalInformation).values(store_id=store_id
                                                          ).execution_options(schema_translate_map={None: schema}))

    await session.execute(insert(StoreOrderTypeAssociation).values([
        {'store_id': store_id, 'order_type_id': 1, 'is_active': False},
        {'store_id': store_id, 'order_type_id': 2, 'is_active': False},
        {'store_id': store_id, 'order_type_id': 3, 'is_active': False}
    ]).execution_options(schema_translate_map={None: schema}))
    await session.commit()
    return {"status": 201}
#     except IntegrityError as e:
#         await crud_delete_store(schema=schema, store_id=store_id)
#         # Откат изменений в случае ошибки
#         # await session.rollback()
# # async def crud_create_new_store(schema: str, data: StoreCreate, user_id: int, session: AsyncSession = Depends(get_async_session)) -> List[StoreCreate]:
# #     stmt = insert(Store).values(**data.dict(), user_id=user_id, created_by=user_id
# #                                 ).execution_options(schema_translate_map={None: schema}).returning(Store.id)
# #     result = await session.execute(stmt)
# #     new_store_id = result.scalar()
# #     await session.commit()
#     return {"status": 201, "id": new_store_id, 'date': data}


# async def crud_create_new_store_and_bot(schema: str, data: StoreCreate, token_bot: BotTokenCreate, user_id: int, session: AsyncSession = Depends(get_async_session)):
#     store_result = await crud_create_new_store(schema=schema, data=data, user_id=user_id, session=session)
#     store_id = store_result.get("id")
#     print(store_id)

#     stmt_token = insert(BotToken).values(
#         **token_bot.dict(), user_id=user_id, store_id=store_id)
#     await session.execute(stmt_token)
#     await session.commit()
#     return {"status": 201}


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


async def crud_update_store_activity(schema: str, store_id: int, session: Session = Depends(get_async_session)):
    stmt = update(StoreSubscription).where(StoreSubscription.store_id == store_id).values(
        is_active=~StoreSubscription.is_active).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"message": f"Изменён статус активности"}


async def crud_create_new_order_type(data: CreateOrderType, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(OrderType).values(
        **data.dict())
    await session.execute(stmt)
    await session.commit()

    return {"status": 201, "data": data}


async def crud_get_all_order_types(session: AsyncSession = Depends(get_async_session)) -> List[ListOrderType]:
    query = select(OrderType).order_by(OrderType.id.desc())
    result = await session.execute(query)
    stores = result.scalars().all()
    return stores


async def crud_create_new_store_order_types_association(schema: str, data: BaseStoreOrderTypeAssociation, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(StoreOrderTypeAssociation).values(
        **data.dict()).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()

    return {"status": 201, "data": data}


async def crud_create_new_day_of_week(data: TestDayOfWeek, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(WorkingDay).values(
        **data.dict()).execution_options(schema_translate_map={None: '1'})
    await session.execute(stmt)
    await session.commit()

    return {"status": 201, "data": data}


# async def crud_create_new_day_of_week(data: CreateDayOfWeek, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(DayOfWeek).values(**data.dict())
#     await session.execute(stmt)
#     await session.commit()

#     return {"status": 201, "data": data}


async def crud_get_store_info(session: AsyncSession = Depends(get_async_session)):
    query = select(StoreInfo).order_by(StoreInfo.id.desc()
                                       ).execution_options(schema_translate_map={None: '1'})
    result = await session.execute(query)
    store_info = result.scalars().all()
    return store_info


async def crud_create_new_test(schema: str, store_id: int, data: PostStoreInfo, session: AsyncSession = Depends(get_async_session)):
    stmt = update(StoreInfo).where(StoreInfo.store_id == store_id).values(
        **data.dict()).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()

    return {"status": 201, }


async def crud_test_get_one_stores(store_id: int, schema: str, session: AsyncSession = Depends(get_async_session)) -> Optional[GetStoreInfo]:
    query = select(StoreInfo).where(StoreInfo.store_id == store_id).execution_options(
        schema_translate_map={None: schema})
    result = await session.execute(query)
    store = result.scalar()
    return store


async def crud_test_many_to_many(store_id: int, schema: str, session: AsyncSession = Depends(get_async_session)) -> Optional[GetStoreInfo]:
    query = select(StoreInfo).where(StoreInfo.store_id == store_id).execution_options(
        schema_translate_map={None: schema})
    result = await session.execute(query)
    store = result.scalar()
    return store


# @router.get("/test_one/", response_model=Optional[GetStoreInfo])
# async def get_all_product(schema: str, store_id: int, product_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = select(Product).options(selectinload(Product.unit)).where(
#         Product.deleted_flag != True).where(Product.store_id == store_id).where(Product.id == product_id).execution_options(schema_translate_map={None: schema})
#     result = await session.execute(query)
#     products = result.scalar()
#     return products
