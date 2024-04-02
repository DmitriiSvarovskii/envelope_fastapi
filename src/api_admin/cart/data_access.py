import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func

from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from typing import List, Optional

from ..models import (
    Product,
    Cart,
    BotToken,
    Order,
    OrderDetail,
    StoreInfo,
    OrderCustomerInfo
)
from .schemas import (
    CartResponse,
    CartCreate,
    CreateOrder,
    CreateCustomerInfo,
    CartItem
)
from src.api_admin.product.schemas import ProductListStore, ProductOne
from src.api_admin.category.schemas import CategoryBaseStore
from src.api_admin.category.crud import crud_get_all_categories
from src.database import get_async_session
from src.bot.handlers import (
    new_order_mess_text_order_chat,
    new_order_mess_text_customer
)
from src.bot.keyboards import (
    create_order_acceptance_keyboard,
    create_order_cancellation_keyboard
)


async def get_cart_items(session, tg_user_id, store_id, schema):
    cart_query = (
        select(
            Cart.product_id,
            Cart.quantity,
            Product.name.label("product_name"),
            (Product.price * Cart.quantity).label("unit_price"),
            func.sum(Cart.quantity * Product.price).over().label("total_price")
        )
        .join(Cart, Cart.product_id == Product.id)
        .filter(Cart.tg_user_id == tg_user_id, Cart.store_id == store_id)
        .execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(cart_query)
    return result.scalars().all()


async def create_order_record(session, data_order, schema):
    stmt_order = (
        insert(Order)
        .values(**data_order.model_dump())
        .returning(Order.id)
        .execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(stmt_order)
    return result.scalar()


def format_order_text(cart_items):
    order_text = ""
    for item in cart_items:
        order_text += f"{item['product_name']} x {item['quantity']}\n"
    return order_text


async def get_bot_token(session, schema, store_id):
    query_token_bot = (
        select(BotToken)
        .where(BotToken.user_id == int(schema), BotToken.store_id == store_id)
    )
    result = await session.execute(query_token_bot)
    return result.scalar().token_bot


async def update_order_details(session, values_list, schema):
    stmt_order_detail = (
        insert(OrderDetail)
        .values(values_list)
        .execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt_order_detail)


async def clear_cart(session, tg_user_id, store_id, schema):
    stmt = (
        delete(Cart)
        .where(Cart.tg_user_id == tg_user_id, Cart.store_id == store_id)
        .execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt)


async def remove_keyboard_later(
    token_bot: str,
    chat_id: int,
    message_id: int,
    delay: int
):
    await asyncio.sleep(delay)
    try:
        bot = Bot(token=token_bot)
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )
    except Exception as e:
        print(f"Ошибка при удалении клавиатуры: {e}")
    finally:
        await bot.session.close()


async def send_message(
    chat_id: int,
    text: str,
    token_bot: str,
    url=None,
    reply_markup=None
):
    try:
        bot = Bot(token=token_bot)
        if url:
            reply_markup = create_keyboard(
                url=url)
        message = await bot.send_message(
            chat_id,
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        await bot.session.close()
        return {
            "status": "success",
            "message": "Сообщение успешно отправлено",
            "message_id": message.message_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


def create_keyboard(url: int):
    button_store: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата наличными',
        callback_data='payment_cash')
    button_store2: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата картой',
        url=url)
    keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_store_builder.row(button_store2, button_store, width=1)
    keyboard_store = keyboard_store_builder.as_markup()
    return keyboard_store
