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

from src.bot.keyboards import (
    create_order_acceptance_keyboard,
    create_order_cancellation_keyboard
)
from src.bot.handlers import (
    new_order_mess_text_customer,
    new_order_mess_text_order_chat
)


router = APIRouter(
    prefix="/api/v1/store_bot",
    tags=["Store (bot)"])


@router.get("/product/", response_model=List[ProductListStore])
async def get_all_products(
    schema: str,
    store_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        where(
            not Product.deleted_flag,
            Product.store_id == store_id
        ).
        order_by(
            Product.popular.desc(),
            Product.id.desc()
        ).
        execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@router.get("/product/{product_id}/", response_model=Optional[ProductOne])
async def get_one_product(
    schema: str,
    store_id: int,
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Product).
        options(selectinload(Product.unit)).
        where(Product.deleted_flag is not True).
        where(
            Product.store_id == store_id,
            Product.id == product_id).
        execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query)
    products = result.scalar()
    return products


@router.get(
    "/category/",
    response_model=List[CategoryBaseStore],
    status_code=200
)
async def get_all_category(
    schema: str,
    store_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        categories = await crud_get_all_categories(
            schema=schema,
            store_id=store_id,
            session=session
        )
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/cart/", response_model=Optional[CartResponse])
async def read_cart_items_and_totals(
    schema: str,
    store_id: int,
    tg_user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(
            Product.id,
            Product.name,
            Product.image,
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
    cart_items = []
    total_price = 0
    for row in result:
        cart_item = CartItem(
            id=row[0],
            name=row[1],
            image=row[2],
            quantity=row[3],
            unit_price=row[4]
        )
        cart_items.append(cart_item)
        total_price = row[5]
    response_data = {
        "cart_items": cart_items,
        "total_price": total_price
    }
    return response_data


@router.post("/cart/add/")
async def add_to_cart(
    schema: str,
    data: CartCreate,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Cart).
        where(
            Cart.tg_user_id == data.tg_user_id,
            Cart.product_id == data.product_id
        ).
        execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query)
    cart_item = result.scalars().all()
    if cart_item:
        stmt = (
            update(Cart).
            where(
                Cart.tg_user_id == data.tg_user_id,
                Cart.product_id == data.product_id
            ).
            values(quantity=func.coalesce(Cart.quantity, 0) + 1).
            execution_options(schema_translate_map={None: schema})
        )
        await session.execute(stmt)
    else:
        stmt = (
            insert(Cart).
            values(**data.model_dump(), quantity=1).
            execution_options(schema_translate_map={None: schema})
        )
        await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'data': data}


@router.delete("/cart/decrease/")
async def decrease_cart_item(
    schema: str,
    data: CartCreate,
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Cart).
        where(
            Cart.tg_user_id == data.tg_user_id,
            Cart.product_id == data.product_id
        ).
        execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query)
    cart_item = result.scalar().quantity

    if cart_item:
        if cart_item > 1:
            stmt = (
                update(Cart).
                where(
                    Cart.tg_user_id == data.tg_user_id,
                    Cart.product_id == data.product_id
                ).
                values(quantity=Cart.quantity - 1).
                execution_options(schema_translate_map={None: schema})
            )
        else:
            stmt = (
                delete(Cart).
                where(
                    Cart.tg_user_id == data.tg_user_id,
                    Cart.product_id == data.product_id).
                execution_options(schema_translate_map={None: schema})
            )
        await session.execute(stmt)
    else:
        return {"status": "error", "message": "Товар не найден в корзине"}

    await session.commit()
    return {"status": 201, 'data': data}


@router.delete("/cart/clear/")
async def delete_cart_items_by_tg_user_id(
    schema: str,
    store_id: int,
    tg_user_id: int,
    session: Session = Depends(get_async_session)
):
    try:
        stmt = (
            delete(Cart).
            where(
                Cart.tg_user_id == tg_user_id,
                Cart.store_id == store_id
            ).
            execution_options(schema_translate_map={None: schema})
        )
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "message": f"Корзина для пользователя №{tg_user_id} очищена."
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/create_order/")
async def create_order(
    schema: str,
    data_order: CreateOrder,
    date_customer_info: CreateCustomerInfo = None,
    session: AsyncSession = Depends(get_async_session)
):
    store_id = data_order.store_id
    tg_user_id = data_order.tg_user_id
    customer_comment = date_customer_info.customer_comment
    cart_query = (
        select(
            Cart.product_id,
            Cart.quantity,
            Product.name.label("product_name"),
            (Product.price * Cart.quantity).label("unit_price"),
            func.sum(
                Cart.quantity * Product.price
            ).over().label("total_price")
        ).
        join(Cart, Cart.product_id == Product.id).
        filter(
            Cart.tg_user_id == tg_user_id,
            Cart.store_id == store_id
        ).execution_options(
            schema_translate_map={None: schema})
    )

    cart_items = await session.execute(cart_query)
    cart_items = cart_items.all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    stmt_order = (
        insert(Order).
        values(**data_order.model_dump()).
        returning(Order.id).
        execution_options(schema_translate_map={None: schema})
    )

    result = await session.execute(stmt_order)
    order_id = result.scalar()
    values_list = []
    order_text = ""
    order_sum = cart_items[0][4]

    for cart_item in cart_items:
        values_list.append({
            "store_id": store_id,
            "order_id": order_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "unit_price": cart_item.unit_price
        })
        product_name = cart_item[2]
        quantity = cart_item[1]
        order_text += f"{product_name} x {quantity}\n"

    order_chat_text = await new_order_mess_text_order_chat(
        order_id=order_id,
        tg_user_id=tg_user_id,
        order_text=order_text,
        order_sum=order_sum,
        delivery_address=date_customer_info.delivery_address,
        customer_phone=date_customer_info.customer_phone,
        customer_comment=customer_comment,
        customer_name=date_customer_info.customer_name,
        tg_user_name=date_customer_info.tg_user_name,
        table_number=date_customer_info.table_number
    )

    query_token_bot = (
        select(BotToken).
        where(
            BotToken.user_id == int(schema),
            BotToken.store_id == store_id
        )
    )
    result = await session.execute(query_token_bot)
    token_bot = result.scalar().token_bot

    new_order_keyboard = create_order_acceptance_keyboard(
        order_id=order_id,
        order_sum=order_sum,
        user_id=tg_user_id,
        order_status='Новый',
        message_id=None
    )

    query_store_info = (
        select(StoreInfo).
        where(StoreInfo.store_id == store_id).
        execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query_store_info)
    store_info = result.scalar()

    customer_text = await new_order_mess_text_customer(
        order_id=order_id,
        tg_user_id=tg_user_id,
        order_text=order_text,
        order_sum=order_sum,
        adress=store_info.adress,
        number_phone=store_info.number_phone,
        customer_comment=customer_comment
    )

    message_id_admin_chat = await send_message(
        token_bot=token_bot,
        chat_id=-1002144078281,
        text=order_chat_text,
        reply_markup=new_order_keyboard
    )

    customer_keyboard = create_order_cancellation_keyboard(
        order_id=order_id,
        order_sum=order_sum,
        user_id=tg_user_id,
        order_status='Отказ',
        message_id=message_id_admin_chat['message_id']
    )

    message_id_customer_chat = await send_message(
        token_bot=token_bot,
        chat_id=tg_user_id,
        text=customer_text,
        reply_markup=customer_keyboard
    )

    asyncio.create_task(remove_keyboard_later(
        token_bot,
        tg_user_id,
        message_id_customer_chat['message_id'],
        10  # Задать значение в самой функции !!!
    ))

    stmt_order_detail = (
        insert(OrderDetail).
        values(values_list).
        execution_options(schema_translate_map={None: schema})
    )

    await session.execute(stmt_order_detail)

    if date_customer_info:
        stmt_customer_infol = (
            insert(OrderCustomerInfo).
            values(
                **date_customer_info.model_dump(),
                store_id=store_id,
                tg_user_id=tg_user_id,
                order_id=order_id
            ).
            execution_options(schema_translate_map={None: schema})
        )
        await session.execute(stmt_customer_infol)
    stmt = (
        delete(Cart).
        where(
            Cart.tg_user_id == tg_user_id,
            Cart.store_id == store_id).
        execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "Order created successfully"}


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


# @router.get("/cart/", response_model=List[CartResponse])
# async def read_cart_items_and_totals(
    # schema: str,
    # store_id: int,
    # tg_user_id: int,
    # session: AsyncSession = Depends(get_async_session)
    # ):
#     query = (
#         select(
#             Product.id,
#             Product.name,
#             Cart.quantity,
#             (Cart.quantity * Product.price).label("unit_price"),
#             func.sum(Cart.quantity * Product.price).over().
# label("total_price")
#         )
#         .join(Cart, Cart.product_id == Product.id)
#         .where(
#             (Cart.tg_user_id == tg_user_id) & (Cart.store_id == store_id)
#         )
#         .group_by(Product.id, Cart.quantity, Product.name, Cart.tg_user_id)
#         .execution_options(schema_translate_map={None: schema})
#     )
#     result = await session.execute(query)
#     user_data = {}
#     for row in result:
#         tg_user_id = row[4]
#         if tg_user_id not in user_data:
#             user_data[tg_user_id] = {
#                 "cart_items": [],
#                 "total_price": 0
#             }
#         user_data[tg_user_id]["cart_items"].append({
#             "id": row[0],
#             "name": row[1],
#             "quantity": row[2],
#             "unit_price": row[3],
#         })
#         user_data[tg_user_id]["total_price"] = row[4]
#     response_data = [
#         {
#             "cart_items": user_info["cart_items"],
#             "total_price": user_info["total_price"]
#         }
#         for user_info in user_data.values()
#     ]
#     return response_data
