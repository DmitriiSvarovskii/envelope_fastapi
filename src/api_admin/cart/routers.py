from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from sqlalchemy import insert, select, label, join, update, delete
from .models import Cart
from ..models import Product, Order, OrderDetail
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Dict, Optional
from src.api_admin.product.schemas import *
from src.api_admin.product.crud import *
from src.api_admin.category.schemas import *
from src.api_admin.category.crud import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload


router = APIRouter(
    prefix="/api/v1/store_bot",
    tags=["Store (bot)"])


@router.get("/product/", response_model=List[ProductListStore])
async def get_all_product(schema: str, store_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).where(
        Product.deleted_flag != True).where(Product.store_id == store_id).order_by(Product.id.desc()).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@router.get("/category/", response_model=List[CategoryBaseStore], status_code=200)
async def get_all_category(schema: str, store_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        categories = await crud_get_all_categories(schema=schema, store_id=store_id, session=session)
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/cart/", response_model=List[CartResponse])
async def read_cart_items_and_totals(schema: str, store_id: int, tg_user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = (
        select(
            Product.id,
            Product.name,
            Cart.quantity,
            (Cart.quantity * Product.price).label("unit_price"),
            func.sum(Cart.quantity * Product.price).over().label("total_price")
        )
        .join(Cart, Cart.product_id == Product.id)
        .where(
            (Cart.tg_user_id == tg_user_id) & (Cart.store_id == store_id)
        )
        .group_by(Product.id, Cart.quantity, Product.name, Cart.tg_user_id)
        .execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query)
    user_data = {}
    for row in result:
        tg_user_id = row[4]
        if tg_user_id not in user_data:
            user_data[tg_user_id] = {
                "cart_items": [],
                "total_price": 0
            }
        user_data[tg_user_id]["cart_items"].append({
            "id": row[0],
            "name": row[1],
            "quantity": row[2],
            "unit_price": row[3],
        })
        user_data[tg_user_id]["total_price"] = row[4]
    response_data = [
        {
            "cart_items": user_info["cart_items"],
            "total_price": user_info["total_price"]
        }
        for user_info in user_data.values()
    ]
    return response_data


@router.post("/cart/add/")
async def add_to_cart(schema: str, data: CartCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id ==
                               data.product_id).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    cart_item = result.scalars().all()
    if cart_item:
        stmt = update(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id == data.product_id).values(
            quantity=func.coalesce(Cart.quantity, 0) + 1).execution_options(schema_translate_map={None: schema})
        await session.execute(stmt)
    else:
        stmt = insert(Cart).values(
            **data.dict(), quantity=1).execution_options(schema_translate_map={None: schema})
        await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'data': data}


@router.delete("/cart/decrease/")
async def decrease_cart_item(schema: str, data: CartCreate,  session: AsyncSession = Depends(get_async_session)):
    query = select(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id ==
                               data.product_id).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    cart_item = result.scalar()
    if cart_item:
        if cart_item.quantity > 0:
            stmt = update(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id == data.product_id).values(
                quantity=func.coalesce(Cart.quantity, 0) - 1).execution_options(schema_translate_map={None: schema})
        else:
            stmt = delete(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id == data.product_id).execution_options(
                schema_translate_map={None: schema})
        await session.execute(stmt)
    else:
        return {"status": "error", "message": "Товар не найден в корзине"}
    await session.commit()
    return {"status": 201, 'data': data}


@router.delete("/cart/clear/")
async def delete_cart_items_by_tg_user_id(schema: str, store_id: int, tg_user_id: int, session: Session = Depends(get_async_session)):
    try:
        stmt = delete(Cart).where(Cart.tg_user_id == tg_user_id, Cart.store_id == store_id).execution_options(
            schema_translate_map={None: schema})
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": f"Корзина для пользователя №{tg_user_id} очищена."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/cart/order/")
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


# @router.get("/cart/", response_model=List[CartItem])
# async def read_cart_items(schema: str, store_id: int, tg_user_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = select(Product.id,
#                    Product.name,
#                    Cart.quantity,
#                    (Cart.quantity * Product.price).label("unit_price")).join(Cart, Cart.product_id == Product.id).where(Cart.tg_user_id == tg_user_id, Cart.store_id == store_id).execution_options(schema_translate_map={None: schema})
#     result = await session.execute(query)
#     cart_items = []
#     for row in result:
#         cart_items.append(CartItem(
#             id=row[0],
#             name=row[1],
#             quantity=row[2],
#             unit_price=row[3]
#         ))
#     return cart_items


# @router.get("/cart_total_price/", response_model=List[CartItemTotal])
# async def read_cart_items(schema: str, store_id: int, tg_user_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             Cart.tg_user_id,
#             func.sum(Cart.quantity * Product.price).label("total_price")
#         )
#         .join(Product, Cart.product_id == Product.id)
#         .where(
#             (Cart.tg_user_id == tg_user_id) & (Cart.store_id == store_id)
#         ).group_by(Cart.tg_user_id)
#         .execution_options(schema_translate_map={None: schema})
#     )

#     result = await session.execute(query)

#     cart_items = [
#         CartItemTotal(total_price=row[0])
#         for row in result.fetchall()
#     ]

#     return cart_items
