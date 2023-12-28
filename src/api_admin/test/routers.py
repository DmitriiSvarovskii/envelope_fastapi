from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from ..auth.routers import get_current_user_from_token
from ..user.models import User
from ..user.routers import register_new_user
from .schemas import *
from .crud import *


router = APIRouter(
    prefix="/api/v1/test",
    tags=["Test (admin)"])


@router.post("/create_role_and_user/", status_code=201)
async def create_new_role(role: RolesCreate, order_status: CreateOrderStatus, unit: CreateUnit, order_type: CreateOrderType, day_of_week: CreateDayOfWeek, delivery_type: DeliveryTypeCreate,  response: Response, user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    await crud_create_new_role(role=role, unit=unit, order_status=order_status, order_type=order_type, day_of_week=day_of_week, delivery_type=delivery_type, session=session)
    await register_new_user(response=response, user_data=user_data, session=session)
    return {"status": 'ok'}


@router.post("/create_store/", status_code=201)
async def create_new_store(data: CreateStore, token_bot: CreateBotToken, session: AsyncSession = Depends(get_async_session)):
    try:
        new_store = await crud_create_new_store_and_bot(schema='1', data=data, token_bot=token_bot, user_id=1, session=session)
        return new_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/create_new_category/", status_code=201)
async def create_new_category(data: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token
    """
    try:
        new_category = await crud_create_new_category(schema="1", store_id=1,  data=data, user_id=1, session=session)
        return new_category
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/create_product/")
async def create_new_product(data: ProductCreate, session: AsyncSession = Depends(get_async_session)):

    new_product = await crud_create_new_product(schema="1", store_id=1, user_id=1, data=data, session=session)
    return new_product


@router.post("/create_product/")
async def create_new_product(data: ProductCreate, session: AsyncSession = Depends(get_async_session)):

    new_product = await crud_create_new_product(schema="1", store_id=1, user_id=1, data=data, session=session)
    return new_product
