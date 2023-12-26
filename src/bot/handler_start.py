from aiogram import types, Bot
from fastapi import Depends
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.bot.bot_get_info import get_info_store_token
from src.api_admin.customer.schemas import CustomerCreate
from src.api_admin.models import *


async def start(message: types.Message, bot: Bot):
    async for session in get_async_session():
        bot_token_obj = await get_info_store_token(bot_token=message.bot.token, session=session)
        welcome_message_text = 'text'
        if bot_token_obj:
            user_id = bot_token_obj.user_id
            store_id = bot_token_obj.store_id
            if message.text.strip() == "/start":
                resourse = None
            else:
                resourse = message.text.replace("/start", "").strip()
            query = select(ServiceTextAndChat.welcome_message_bot).where(
                ServiceTextAndChat.store_id == store_id).execution_options(schema_translate_map={None: str(store_id)})
            result = await session.execute(query)
            welcome_message_text = result.scalar()
            query = select(StoreInfo).where(
                StoreInfo.store_id == store_id).execution_options(schema_translate_map={None: str(store_id)})
            result = await session.execute(query)
            locations = result.scalar()
            latitude = locations.latitude
            longitude = locations.longitude
            new_customer_data = (
                CustomerCreate(
                    store_id=store_id,
                    tg_user_id=message.from_user.id,
                    resourse=resourse,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    username=message.from_user.username,
                    is_premium=message.from_user.is_premium,
                )
            )
            await add_tg_user(schema=str(user_id), data=new_customer_data, session=session)
            url = f"https://store.envelope-app.ru/schema={user_id}/store_id={store_id}/"
            await bot.set_chat_menu_button(
                chat_id=message.chat.id,
                menu_button=types.MenuButtonWebApp(text="Store", web_app=types.WebAppInfo(
                    url=url)),
            )
        break

    await bot.send_message(chat_id=message.chat.id, text=welcome_message_text)
    if latitude and longitude:
        await bot.send_location(chat_id=message.chat.id, latitude=latitude, longitude=longitude)


def compare_customer_data(customer: Customer, data: CustomerCreate) -> bool:
    if customer is None:
        return False
    if customer.first_name != data.first_name:
        return False
    if customer.last_name != data.last_name:
        return False
    if customer.username != data.username:
        return False
    if customer.is_premium != data.is_premium:
        return False
    if customer.resourse != data.resourse:
        return False
    return True


async def add_tg_user(schema: str, data: CustomerCreate, session: AsyncSession = Depends(get_async_session)):
    if data.is_premium is None:
        data.is_premium = False
    query = select(Customer).filter(
        Customer.tg_user_id == data.tg_user_id,
        Customer.store_id == data.store_id
    ).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    customer = result.scalar()
    if customer:
        if not compare_customer_data(customer, data):
            update_data = data.dict(exclude_unset=True)
            await session.execute(
                update(Customer).where(
                    Customer.tg_user_id == data.tg_user_id,
                    Customer.store_id == data.store_id
                ).values(**update_data).execution_options(schema_translate_map={None: schema})
            )
            await session.commit()
            return {"status": 200, "message": "User updated", "data": update_data}
    else:
        stmt = insert(Customer).values(
            **data.dict()).execution_options(schema_translate_map={None: schema})
        await session.execute(stmt)
        await session.commit()
        return {"status": 201, "message": "User created", "data": data}
