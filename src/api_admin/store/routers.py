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


# @router.get("/one/", status_code=200, response_model=Optional[OneStore])
@router.get("/one/", status_code=200, )
async def get_one_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        store = await crud_get_one_stores(store_id=store_id, schema=str(current_user.id), session=session)
        return store
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


@router.delete("/")
async def delete_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_store = await crud_delete_store(schema=str(current_user.id), store_id=store_id, session=session)
        return change_store
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


@router.put("/store_info/", status_code=200)
async def update_store_info(store_id: int, data: UpdateStoreInfo,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store_info(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/store_info/")
async def update_checkbox_store_info(store_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    # Параметры:
    #     - `store_id`: идентификатор магазина.
    #     - `checkbox`: имя поля, которое требуется изменить.
    #     Для типа оплаты доступны следующие значения: `format_unified`, `format_24_7`, `format_custom`
    """
    try:
        result = await crud_update_checkbox_store_info(schema=str(current_user.id), store_id=store_id, checkbox=checkbox, session=session)
        return result
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


@router.patch("/order_type/")
async def update_order_type(store_id: int, order_type_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        result = await crud_update_order_type(schema=str(current_user.id), store_id=store_id, order_type_id=order_type_id, session=session)
        return result
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/day_of_week/", status_code=201)
async def update_new_day_of_week(store_id: int, day_of_week_id: int,  data: UpdaneDayOfWeek, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_order_type = await crud_update_new_day_of_week(schema=str(current_user.id), store_id=store_id, day_of_week_id=day_of_week_id, data=data, user_id=current_user.id, session=session)
        return new_order_type
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/day_of_week/")
async def update_day_of_week(store_id: int, day_of_week_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        result = await crud_update_day_of_week(schema=str(current_user.id), store_id=store_id, day_of_week_id=day_of_week_id, session=session)
        return result
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/store_payments/", status_code=200)
async def update_store_payments(store_id: int, data: UpdateStorePayment,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store_payments(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/store_payments/")
async def update_checkbox_payments(store_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    # Параметры:
    #     - `store_id`: идентификатор магазина.
    #     - `checkbox`: имя поля, которое требуется изменить.
    #     Для типа оплаты доступны следующие значения: `cash`, `card`
    """
    try:
        result = await crud_update_checkbox_payments(schema=str(current_user.id), store_id=store_id, checkbox=checkbox, session=session)
        return result
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/delivery_distance/", status_code=200)
async def create_store_delivery_distance(data: PostDeliveryDistance,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_create_store_delivery_distance(schema=str(current_user.id), data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/delivery_distance/", status_code=200)
async def update_store_delivery_distance(store_id: int, data: UpdateDeliveryDistance,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store_delivery_distance(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/delivery_fix/", status_code=200)
async def create_store_delivery_fix(data: PostDeliveryFix,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_create_store_delivery_fix(schema=str(current_user.id), data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/delivery_fix/", status_code=200)
async def update_store_delivery_fix(store_id: int, data: UpdateDeliveryFix,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store_delivery_fix(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/delivery_district/", status_code=200)
async def create_store_delivery_district(store_id: int, data: PostDeliveryDistrict,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_create_store_delivery_district(schema=str(current_user.id), data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/delivery_district/", status_code=200)
async def update_store_delivery_district(store_id: int, delivery_id: int, data: UpdateDeliveryDistrict,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store_delivery_district(schema=str(current_user.id), store_id=store_id, delivery_id=delivery_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/delivery_district/")
async def delete_delivery_district(store_id: int, delivery_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_store = await crud_delete_delivery_district(schema=str(current_user.id), store_id=store_id, delivery_id=delivery_id, session=session)
        return change_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/service_text_and_chats/", status_code=200)
async def update_service_text_and_chats(store_id: int, data: UpdateServiceTextAndChat,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_service_text_and_chats(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/legal_informations/", status_code=200)
async def update_store_legal_informations(store_id: int, data: UpdateLegalInformation,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store_legal_informations(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
