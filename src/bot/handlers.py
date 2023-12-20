from aiogram import types
from aiogram.filters import Command
from src.database import get_async_session
from src.api_admin.store.routers import crud_get_info_store_token
from src.api_admin.cart.routers import add_tg_user
from src.api_admin.customer.schemas import CustomerCreate
# from src.main import dp, bot
from aiogram import Bot

# @dp.message(Command(commands=['start']))
async def start(message: types.Message, bot: Bot):
    async for session in get_async_session():
        bot_token_obj = await crud_get_info_store_token(bot_token=message.bot.token, session=session)
        if bot_token_obj:
            user_id = bot_token_obj.user_id
            store_id = bot_token_obj.store_id
            if message.text.strip() == "/start":
                resourse = None
            else:
                resourse = message.text.replace("/start", "").strip()
            new_customer_data = CustomerCreate(
                store_id=store_id,
                tg_user_id=message.from_user.id,
                resourse=resourse,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                is_premium=message.from_user.is_premium,
            )
            await add_tg_user(schema=str(user_id), data=new_customer_data, session=session)
            url = f"https://store.envelope-app.ru/schema={user_id}/store_id={store_id}/"
            await bot.set_chat_menu_button(
                chat_id=message.chat.id,
                menu_button=types.MenuButtonWebApp(text="Store", web_app=types.WebAppInfo(
                    url=url)),
            )
        break

    await bot.send_message(chat_id=message.chat.id, text=f"Привет! Я ваш бот")
