from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, join, label
from .models import Order, OrderDetail
from src.cart.models import Cart
from src.product.models import Product
from .schemas import OrderBase, OrderDetailBase
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List, Dict
from typing import Optional


router = APIRouter(
    prefix="/order",
    tags=["Order"])


@router.get("/")
async def get_all_orders(session: AsyncSession = Depends(get_async_session)) -> List[OrderBase]:
    query = select(Order).order_by(Order.id.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/detail")
async def get_all_order_details(session: AsyncSession = Depends(get_async_session)) -> List[OrderDetailBase]:
    query = select(OrderDetail).order_by(OrderDetail.id.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/")
async def create_order(
    tg_user_id: int,
    shop_id: int,
    delivery_city: Optional[str] = None,
    delivery_address: Optional[str] = None,
    customer_name: Optional[str] = None,
    customer_phone: Optional[str] = None,
    customer_comment: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    cart_query = select(Cart).filter(
        Cart.tg_user_id == tg_user_id,
        Cart.shop_id == shop_id
    )
    cart_items = await session.execute(cart_query)
    cart_items = cart_items.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(
        shop_id=shop_id,
        tg_user_id=tg_user_id,
        delivery_city=delivery_city,
        delivery_address=delivery_address,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_comment=customer_comment
    )
    session.add(order)
    await session.flush()

    for cart_item in cart_items:
        product = await session.get(Product, cart_item.product_id)
        unit_price = product.price

        order_detail = OrderDetail(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=unit_price,
            shop_id=shop_id
        )
        session.add(order_detail)

    await session.execute(Cart.__table__.delete().where(
        Cart.tg_user_id == tg_user_id,
        Cart.shop_id == shop_id
    ))

    await session.commit()

    return {"status": "Order created successfully"}
