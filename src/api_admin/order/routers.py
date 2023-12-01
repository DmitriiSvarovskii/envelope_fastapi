from fastapi import Depends, APIRouter
from sqlalchemy import func, desc
from sqlalchemy.future import select
from typing import List, Dict, Optional, Union
from typing import List, Union, Dict
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import func
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from .models import Order, OrderDetail
from ..models import Cart, Category, Product, Customer
from ..customer.schemas import *
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


# @router.get("/customer/")
# # async def get_all_customer(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)) -> List[CustomerBase]:
# #     query = select(Customer).where(Customer.store_id == store_id).order_by(
# #         Customer.id.desc()).execution_options(schema_translate_map={None: str(current_user.id)})
# #     result = await session.execute(query)
# #     return result.scalars().all()


# @router.get("/total_category/", response_model=List[ReportCategoryTotal])
# async def get_category_data(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             Category.name.label("category_name"),
#             func.sum(OrderDetail.unit_price).label("total_sales"))
#         .join(Product, Product.category_id == Category.id)
#         .join(OrderDetail, OrderDetail.product_id == Product.id)
#         .where(OrderDetail.store_id == store_id)
#         .group_by(Category.name)).order_by(desc("total_sales")).execution_options(
#         schema_translate_map={None: str(current_user.id)})
#     result = await session.execute(query)
#     data = result.all()
#     return {"Отчёт по категориям": data}


# @router.get("/customer/", response_model=List[ReportCustomer])
# async def get_customer_data(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             Customer.id,
#             Customer.tg_user_id,
#             Customer.username,
#             Customer.first_name,
#             Customer.last_name,
#             Customer.is_premium,
#             func.coalesce(func.sum(OrderDetail.quantity *
#                                    OrderDetail.unit_price), 0).label("total_sales"),
#             func.coalesce(func.to_char(func.max(Order.created_at),
#                                        'DD.MM.YYYY'), '-').label("last_order_date")
#         )
#         .outerjoin(Order)
#         .outerjoin(OrderDetail, OrderDetail.order_id == Order.id)
#         .select_from(Customer)
#         .group_by(Customer.id)
#         .order_by(desc(Customer.id))
#         .where(Customer.store_id == store_id)
#         .execution_options(schema_translate_map={None: str(current_user.id)})
#     )

#     result = await session.execute(query)
#     data = result.all()
#     return {"Отчёт по клиентам": data}


# @router.get("/total_product/", response_model=List[ReportProductTotal])
# async def get_product_data(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             Product.name.label("product_name"),
#             Category.name.label("category_name"),
#             func.sum(OrderDetail.unit_price).label("total_sales"))
#         .join(Product, Product.category_id == Category.id)
#         .join(OrderDetail, OrderDetail.product_id == Product.id)
#         .where(OrderDetail.store_id == store_id)
#         .group_by(Product.name, Category.name)).order_by(desc("total_sales")).execution_options(
#         schema_translate_map={None: str(current_user.id)})
#     result = await session.execute(query)
#     data = result.all()
#     return {"Отчёт по продуктам": data}


# @router.get("/total_report/", response_model=Optional[ReportMain])
# async def get_main_data(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             func.sum(OrderDetail.unit_price).label("total_sales"))
#         .where(OrderDetail.store_id == store_id)
#         .execution_options(
#             schema_translate_map={None: str(current_user.id)}))
#     result = await session.execute(query)
#     data = result.scalar()
#     return {"Отчёт по общим продажам": data}


async def get_category_data(store_id: int, current_user: User, session: AsyncSession):
    query = (
        select(
            Category.name.label("category_name"),
            func.sum(OrderDetail.unit_price).label("total_sales"))
        .join(Product, Product.category_id == Category.id)
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .where(OrderDetail.store_id == store_id)
        .group_by(Category.name)).order_by(desc("total_sales")).execution_options(
        schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    data = result.all()
    return [{"category_name": item.category_name, "total_sales": item.total_sales} for item in data]


async def get_customer_data(store_id: int, current_user: User, session: AsyncSession):
    query = (
        select(
            Customer.id,
            Customer.tg_user_id,
            Customer.username,
            Customer.first_name,
            Customer.last_name,
            Customer.is_premium,
            func.coalesce(func.sum(OrderDetail.quantity *
                                   OrderDetail.unit_price), 0).label("total_sales"),
            func.coalesce(func.to_char(func.max(Order.created_at),
                                       'DD.MM.YYYY'), '-').label("last_order_date")
        )
        .outerjoin(Order)
        .outerjoin(OrderDetail, OrderDetail.order_id == Order.id)
        .select_from(Customer)
        .group_by(Customer.id)
        .order_by(desc(Customer.id))
        .where(Customer.store_id == store_id)
        .execution_options(schema_translate_map={None: str(current_user.id)})
    )

    result = await session.execute(query)
    data = result.all()
    return [
        {
            "customer_id": item.id,
            "tg_user_id": item.tg_user_id,
            "username": str(item.username) if item.username else None,
            "first_name": str(item.first_name) if item.first_name else None,
            "last_name": str(item.last_name) if item.last_name else None,
            "is_premium": item.is_premium,
            "total_sales": item.total_sales,
            "last_order_date": item.last_order_date,
        }
        for item in data
    ]


async def get_product_data(store_id: int, current_user: User, session: AsyncSession):
    query = (
        select(
            Product.name.label("product_name"),
            Category.name.label("category_name"),
            func.sum(OrderDetail.unit_price).label("total_sales"))
        .join(Product, Product.category_id == Category.id)
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .where(OrderDetail.store_id == store_id)
        .group_by(Product.name, Category.name)).order_by(desc("total_sales")).execution_options(
        schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    data = result.all()
    return [{"product_name": item.product_name, "category_name": item.category_name, "total_sales": item.total_sales} for item in data]


async def get_main_data(store_id: int, current_user: User, session: AsyncSession):
    query = (
        select(
            func.sum(OrderDetail.unit_price).label("total_sales"))
        .where(OrderDetail.store_id == store_id)
        .execution_options(
            schema_translate_map={None: str(current_user.id)}))
    result = await session.execute(query)
    data = result.scalar()
    return [{"total_sales": data}]


@router.get("/analytics/", response_model=Dict[str, List[Dict[str, Union[str, float]]]])
async def get_analytics(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    category_data = await get_category_data(store_id, current_user, session)
    customer_data = await get_customer_data(store_id, current_user, session)
    product_data = await get_product_data(store_id, current_user, session)
    main_data = await get_main_data(store_id, current_user, session)

    analytics_data = {
        "Отчёт по категориям": category_data,
        "Отчёт по клиентам": customer_data,
        "Отчёт по продуктам": product_data,
        "Отчёт по общим продажам": main_data,
    }

    return analytics_data
