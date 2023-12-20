from sqlalchemy import select, outerjoin, and_
from sqlalchemy.orm import selectinload, joinedload
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_async_session
from .models import *
from .crud import *
from .schemas import *
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/store",
    tags=["Store (admin)"])


@router.get("/", response_model=List[ListStoreInfo], status_code=200)
async def get_all_store(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        categories = await crud_get_all_stores(schema=str(current_user.id), session=session)
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/one/", status_code=200, response_model=Optional[OneStore])
async def get_one_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        store = await crud_get_one_stores(store_id=store_id, schema=str(current_user.id), session=session)
        return store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/store_token_bot/", status_code=200, response_model=Optional[GetBotToken])
async def get_info_store_token(bot_token: str, session: AsyncSession = Depends(get_async_session)):
    try:
        info_store_token = await crud_get_info_store_token(bot_token=bot_token, session=session)
        return info_store_token
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/store_token_bot_all/", status_code=200, response_model=List[GetBotToken])
async def get_info_store_token(session: AsyncSession = Depends(get_async_session)):
    try:
        info_store_token = await crud_get_info_store_token_all(session=session)
        return info_store_token
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", status_code=201)
async def create_new_store(data: StoreCreate, token_bot: BotTokenCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_store = await crud_create_new_store_and_bot(schema=str(current_user.id), data=data, token_bot=token_bot, user_id=current_user.id, session=session)
        return new_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/", status_code=200)
async def update_store(store_id: int, data: StoreUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/delete/")
async def change_delete_flag_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_store = await crud_change_delete_flag_store(schema=str(current_user.id), user_id=current_user.id, store_id=store_id, session=session)
        return change_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/")
async def delete_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_store = await crud_delete_store(schema=str(current_user.id), store_id=store_id, session=session)
        return change_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/update_activity/")
async def update_store_activity(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        result = await crud_update_store_activity(schema=str(current_user.id), store_id=store_id, session=session)
        return result
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/order_type/", response_model=List[ListOrderType], status_code=200)
# async def get_all_order_types(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def get_all_order_types(session: AsyncSession = Depends(get_async_session)):
    try:
        order_types = await crud_get_all_order_types(session=session)
        return order_types
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/order_type/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_order_type(data: CreateOrderType, session: AsyncSession = Depends(get_async_session)):
    try:
        new_order_type = await crud_create_new_order_type(data=data, session=session)
        return new_order_type
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/order_type/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_order_type(data: CreateOrderType, session: AsyncSession = Depends(get_async_session)):
    pass


@router.patch("/order_type/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_order_type(data: CreateOrderType, session: AsyncSession = Depends(get_async_session)):
    pass


@router.delete("/order_type/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_order_type(order_type_id: int, session: AsyncSession = Depends(get_async_session)):
    pass


@router.post("/store_order_type/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_store_order_types_association(data: BaseStoreOrderTypeAssociation, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_order_type = await crud_create_new_store_order_types_association(schema=str(current_user.id), data=data, session=session)
        return new_order_type
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# @router.post("/day_of_week/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_day_of_week(data: CreateDayOfWeek, session: AsyncSession = Depends(get_async_session)):
    try:
        new_order_type = await crud_create_new_day_of_week(data=data, session=session)
        return new_order_type
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/store_info/", response_model=List[GetStoreInfo], status_code=200)
# async def get_all_order_types(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def get_all_order_types(session: AsyncSession = Depends(get_async_session)):
    try:
        order_types = await crud_get_store_info(session=session)
        return order_types
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/test_store/", status_code=201)
async def create_new_store(store_id: int, data: PostStoreInfo, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_store = await crud_create_new_test(schema=str(current_user.id), store_id=store_id, data=data, session=session)
        return new_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/test/")
async def read_test_many_to_many(session: AsyncSession = Depends(get_async_session)):
    query = (select(Store)
             .where(Store.id == 1)
             .options(joinedload(Store.info))
             .options(selectinload(Store.order_typed))
             .execution_options(
        schema_translate_map={None: "1"}))
    result = await session.execute(query)
    stores = result.scalars().all()
    # return stores

    test_many_to_many_list = [
        TestManyToMany(
            store_id=store.id,
            store_name=store.info.name,
            order_type_name=order_type.name,
            order_type_id=order_type.id,
            is_active=None,
        )
        for store in stores
        for order_type in store.order_typed
    ]
    return test_many_to_many_list


@router.post("/day_of_week/", status_code=201)
# async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
async def create_new_day_of_week(data: TestDayOfWeek, session: AsyncSession = Depends(get_async_session)):
    try:
        new_order_type = await crud_create_new_day_of_week(data=data, session=session)
        return new_order_type
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")

# is_active
# subscription_start_date
# subscription_duration_months
# @router.post("/subscription/", status_code=201)
# # async def create_new_order_type(data: CreateOrderType, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
# async def create_new_subscription(data: TestDayOfWeek, session: AsyncSession = Depends(get_async_session)):
#     try:
#         new_order_type = await crud_create_new_subscription(data=data, session=session)
#         return new_order_type
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/days_of_week_test/")
async def read_test_many_to_many(session: AsyncSession = Depends(get_async_session)):
    query = (select(Store)
             .where(Store.id == 1)
             .options(
                 selectinload(Store.working_days),
                 selectinload(Store.info))
             .execution_options(
        schema_translate_map={None: "1"}))
    result = await session.execute(query)
    stores = result.scalars().all()
    return stores


@router.get("/test_test/", response_model=List[WorkingHours])
async def read_test_many_to_many(session: AsyncSession = Depends(get_async_session)):
    query = (
        select(
            WorkingDay.store_id,
            WorkingDay.day_of_week_id,
            DayOfWeek.day_of_week,
            WorkingDay.opening_time,
            WorkingDay.closing_time,
            WorkingDay.is_working,
        )
        .select_from(
            outerjoin(WorkingDay, DayOfWeek)
            .join(Store)
        )
        .where(Store.id == 1).execution_options(
            schema_translate_map={None: "1"})
    )
    result = await session.execute(query)
    working_hours_list = [
        {
            "store_id": row.store_id,
            "day_of_week_id": row.day_of_week_id,
            "name": row.name,
            "opening_time": row.opening_time,
            "closing_time": row.closing_time,
            "is_working": row.is_working,
        }
        for row in result
    ]
    return working_hours_list


@router.get("/type_order/", response_model=List[ListTypeOrder])
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


# async def read_test_many_to_many(session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             OrderType.id,
#             OrderType.name,
#             StoreOrderTypeAssociation.is_active,
#             StoreOrderTypeAssociation.store_id,
#         )
#         .select_from(
#             outerjoin(OrderType, StoreOrderTypeAssociation)
#         )
#         .where(StoreOrderTypeAssociation.store_id == 1).execution_options(
#             schema_translate_map={None: "1"})
#     )
#     result = await session.execute(query)
#     working_hours_list = [
#         {
#             "order_type_id": row.id,
#             "order_type_name": row.name,
#             "is_active": row.is_active,
#             "store_id": row.store_id,
#         }
#         for row in result
#     ]
#     return working_hours_list
