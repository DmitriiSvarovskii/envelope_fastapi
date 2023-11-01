from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, label, join
from .models import Cart
from src.api_admin.product.models import Product
from .schemas import CartBase, CartCreate, CartItem
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Dict


router = APIRouter(
    prefix="/cart",
    tags=["Cart"])


@router.get("/", response_model=List[CartItem])
async def read_cart_items(tg_user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product.id,
                   Product.name,
                   Product.description,
                   Cart.quantity,
                   (Cart.quantity * Product.price).label("unit_price")).join(Cart, Cart.product_id == Product.id).where(Cart.tg_user_id == tg_user_id)
    result = await session.execute(query)
    cart_items = []
    for row in result:
        cart_items.append(CartItem(
            id=row[0],
            name=row[1],
            description=row[2],
            quantity=row[3],
            unit_price=row[4]
        ))

    return cart_items


@router.post("/add/")
async def add_to_cart(new_product: CartCreate, session: AsyncSession = Depends(get_async_session)):
    existing_cart_items = await session.execute(
        select(Cart).filter_by(
            tg_user_id=new_product.tg_user_id,
            product_id=new_product.product_id
        )
    )
    existing_cart_items = existing_cart_items.scalars().all()

    if existing_cart_items:
        existing_cart_item = existing_cart_items[0]
        existing_cart_item.quantity += 1
    else:
        new_cart_item = Cart(**new_product.dict())
        session.add(new_cart_item)

    await session.commit()
    return {"status": "success"}


@router.post("/decrease/")
async def decrease_cart_item(new_product: CartCreate, quantity: int = 1, session: AsyncSession = Depends(get_async_session)):
    cart_item = await session.execute(
        select(Cart).filter_by(
            tg_user_id=new_product.tg_user_id,
            product_id=new_product.product_id
        )
    )
    cart_item = cart_item.scalars().first()

    if cart_item:
        cart_item.quantity -= quantity

        if cart_item.quantity <= 0:
            session.delete(cart_item)
    else:
        return {"status": "error", "message": "Товар не найден в корзине"}

    await session.commit()
    return {"status": "success"}


@router.delete("/clear/")
async def delete_cart_items_by_tg_user_id(tg_user_id: int, session: Session = Depends(get_async_session)):
    try:
        await session.execute(Cart.__table__.delete().where(Cart.tg_user_id == tg_user_id))
        await session.commit()
        return {"status": "success", "message": f"All items for tg_user_id {tg_user_id} have been deleted."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
