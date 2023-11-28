from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import func
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from .models import Order, OrderDetail
from ..models import Cart, Category, Product
from src.api_admin.product.models import Product
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import Optional
from typing import List, Annotated
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/report",
    tags=["Report (admin)"])


@router.get("/order/")
async def get_all_orders(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)) -> List[OrderBase]:
    query = select(Order).where(Order.store_id == store_id).order_by(Order.id.desc()).execution_options(
        schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/order_detail/")
async def get_all_order_details(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)) -> List[OrderDetailBase]:
    query = select(OrderDetail).where(OrderDetail.store_id == store_id).order_by(OrderDetail.id.desc()).execution_options(
        schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    return result.scalars().all()


# @router.get("/detail/")
# async def get_all_order_details(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)) -> List[OrderDetailBase]:
#     query = select(OrderDetail).where(OrderDetail.store_id == store_id).order_by(OrderDetail.id.desc()).execution_options(
#         schema_translate_map={None: str(current_user.id)})
#     result = await session.execute(query)
#     return result.scalars().all()


@router.get("/total_category/", response_model=List[OrderCategoryTotal])
async def category_unit_price(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    query = (
        select(
            Category.name.label("category_name"),
            func.sum(OrderDetail.unit_price).label("total_price"))
        .join(Product, Product.category_id == Category.id)
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .where(OrderDetail.store_id == store_id)
        .group_by(Category.name)).execution_options(
        schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    data = result.all()
    return data
