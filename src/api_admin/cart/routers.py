import yookassa
from aiohttp import web
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func

from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from typing import List

from ..models import *
from .schemas import *
from src.api_admin.product.schemas import *
from src.api_admin.product.crud import *
from src.api_admin.category.schemas import *
from src.api_admin.category.crud import *
from ..customer.schemas import CustomerCreate
from src.database import get_async_session


router = APIRouter(
    prefix="/api/v1/store_bot",
    tags=["Store (bot)"])


@router.get("/product/", response_model=List[ProductListStore])
async def get_all_product(schema: str, store_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).where(
        Product.deleted_flag != True, Product.store_id == store_id).order_by(Product.popular.desc(), Product.id.desc()).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@router.get("/product/{product_id}/", response_model=Optional[ProductOne])
async def get_all_product(schema: str, store_id: int, product_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).options(selectinload(Product.unit)).where(
        Product.deleted_flag != True).where(Product.store_id == store_id).where(Product.id == product_id).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    products = result.scalar()
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


@router.get("/cart/", response_model=Optional[CartResponse])
async def read_cart_items_and_totals(schema: str, store_id: int, tg_user_id: int, session: AsyncSession = Depends(get_async_session)):
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


# @router.get("/cart/", response_model=List[CartResponse])
# async def read_cart_items_and_totals(schema: str, store_id: int, tg_user_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = (
#         select(
#             Product.id,
#             Product.name,
#             Cart.quantity,
#             (Cart.quantity * Product.price).label("unit_price"),
#             func.sum(Cart.quantity * Product.price).over().label("total_price")
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
async def decrease_cart_item(schema: str, data: CartCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id ==
                               data.product_id).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    cart_item = result.scalar()

    if cart_item:
        if cart_item.quantity > 1:
            stmt = update(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id == data.product_id).values(
                quantity=Cart.quantity - 1).execution_options(schema_translate_map={None: schema})
        else:
            stmt = delete(Cart).where(Cart.tg_user_id == data.tg_user_id, Cart.product_id ==
                                      data.product_id).execution_options(schema_translate_map={None: schema})
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


@router.post("/create_order/")
async def create_order(schema: str, data_order: CreateOrder, date_customer_info: CreateCustomerInfo = None, session: AsyncSession = Depends(get_async_session)):
    store_id = data_order.store_id
    tg_user_id = data_order.tg_user_id
    cart_query = (
        select(Cart.product_id,
               Cart.quantity,
               Product.name.label("product_name"),
               (Product.price * Cart.quantity).label("unit_price"),
               func.sum(Cart.quantity * Product.price).over().label("total_price")).
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
        raise HTTPException(status_code=400, detail="Cart is empty")

    stmt_order = (
        insert(Order).
        values(**data_order.dict()).
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

    query_store_info = (
        select(StoreInfo).
        where(StoreInfo.store_id == store_id).
        execution_options(schema_translate_map={None: schema}))
    result = await session.execute(query_store_info)
    store_info = result.scalar()

    text = await new_order_mess_text_customer(
        order_id=order_id,
        tg_user_id=tg_user_id,
        order_text=order_text,
        order_sum=order_sum,
        adress=store_info.adress,
        number_phone=store_info.number_phone
    )

    query_token_bot = (
        select(BotToken).
        where(BotToken.user_id == int(schema),
              BotToken.store_id == store_id)
    )
    result = await session.execute(query_token_bot)
    token_bot = result.scalar()

    url, payment_id = await create_pay(total_price=order_sum, order_id=order_id)

    await send_message(token_bot=token_bot.token_bot, chat_id=tg_user_id, text=text, url=url)
    await send_message(token_bot=token_bot.token_bot, chat_id=-1001519347936, text=text)

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
                **date_customer_info.dict(),
                store_id=store_id,
                tg_user_id=tg_user_id,
                order_id=order_id
            ).
            execution_options(schema_translate_map={None: schema})
        )
        await session.execute(stmt_customer_infol)
    stmt = delete(Cart).where(Cart.tg_user_id == tg_user_id, Cart.store_id == store_id).execution_options(
        schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"status": "Order created successfully"}


async def send_message(chat_id: int, text: str, url: str, token_bot: str, reply_markup=None):
    try:
        bot = Bot(token=token_bot)
        keyboard = create_keyboard(
            url=url) if reply_markup is not None else None
        await bot.send_message(
            chat_id,
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


async def new_order_mess_text_customer(order_id: int, tg_user_id: int, order_text: str, order_sum: int, adress: str, number_phone: str):
    try:
        current_time = datetime.now()
        coocking_time = timedelta(minutes=45)
        order_time = current_time + coocking_time

        text = f"Заказ №{order_id} от {current_time.strftime('%d.%m.%Y')} в {current_time.strftime('%H:%M')}\n" \
            f"Код клиента: {tg_user_id}\n" \
            "--------------------\n" \
            "Ваш выбор:\n\n" \
            f"{order_text}" \
            f"\nСумма: {order_sum} руб.\n" \
            "--------------------\n" \
            f"Статус: Новый\n" \
            f"Дата и время выдачи: {order_time.strftime('%d.%m.%Y %H:%M')}\n" \
            "--------------------\n" \
            f"Адрес заведения: {adress}\n" \
            f"Телефон заведения: {number_phone}\n"
        return text
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


api_id = '278535'
api_key = 'test_W5YF4StOK5ZheXJWyIodZUAUJdhU7fYMm5DFRLQI7Ww'


async def create_pay(total_price: int, order_id: int):
    yookassa.Configuration.account_id = api_id
    yookassa.Configuration.secret_key = api_key

    payment = yookassa.Payment.create({
        "amount": {
            "value": total_price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": 'https://t.me/store_demo_envelope_app_bot'
        },
        "description": f"Оплата заказа №{order_id}",
        "capture": True
    })
    url = payment.confirmation.confirmation_url
    return url, payment


async def payment_callback(request):
    data = await request.json()
    # Обработка данных от YooKassa
    print("Получен обратный вызов от YooKassa:")
    print(data)
    return web.Response()


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
