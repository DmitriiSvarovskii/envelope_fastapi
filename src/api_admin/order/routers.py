from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from .models import Order, OrderDetail
from ..models import Cart
from src.api_admin.product.models import Product
from .schemas import OrderBase, OrderDetailBase
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import Optional
from typing import List, Annotated
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/order",
    tags=["Order (store, admin)"])


@router.get("/")
async def get_all_orders(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)) -> List[OrderBase]:
    query = select(Order).where(Order.store_id == store_id).order_by(Order.id.desc()).execution_options(
            schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/detail")
async def get_all_order_details(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)) -> List[OrderDetailBase]:
    query = select(OrderDetail).where(OrderDetail.store_id == store_id).order_by(OrderDetail.id.desc()).execution_options(
            schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/")
async def create_order(
    schema: str,
    tg_user_id: int,
    store_id: int,
    delivery_city: Optional[str] = None,
    delivery_address: Optional[str] = None,
    customer_name: Optional[str] = None,
    customer_phone: Optional[str] = None,
    customer_comment: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    cart_query = select(Cart).filter(
        Cart.tg_user_id == tg_user_id,
        Cart.store_id == store_id
    ).execution_options(
            schema_translate_map={None: schema})
    cart_items = await session.execute(cart_query)
    cart_items = cart_items.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(
        store_id=store_id,
        tg_user_id=tg_user_id,
        delivery_city=delivery_city,
        delivery_address=delivery_address,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_comment=customer_comment
    ).execution_options(
            schema_translate_map={None: schema})
    session.add(order)
    await session.flush()

    for cart_item in cart_items:
        product = await session.get(Product, cart_item.product_id).execution_options(
            schema_translate_map={None: schema})
        unit_price = product.price

        order_detail = OrderDetail(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=unit_price,
            store_id=store_id
        ).execution_options(
            schema_translate_map={None: schema})
        session.add(order_detail)

    await session.execute(Cart.__table__.delete().where(
        Cart.tg_user_id == tg_user_id,
        Cart.store_id == store_id
    ).execution_options(
            schema_translate_map={None: schema}))

    await session.commit()

    return {"status": "Order created successfully"}
