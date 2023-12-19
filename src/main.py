from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api_admin.routers import routers
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
TOKEN = '5895760296:AAF2hSRl3TAIrZGHD6M5sSDdtdYkQPr9sUc'


app = FastAPI(
    title="Envelope-app",
    version="1.0.0a",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

WEBHOOK_HOST = 'https://envelope-app.ru'
# WEBHOOK_HOST = 'https://fd9f-103-157-162-242.ngrok.io'
WEBHOOK_PATH = '/api/v1/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    update_data = await request.json()
    print("Полученные данные обновления:", update_data)
    update = Update(**update_data)
    await dp.feed_update(bot, update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@dp.message(Command(commands=['start']))
async def start(message: types.Message):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Store", web_app=WebAppInfo(
            url='https://store.envelope-app.ru/schema=1/store_id=1/')),
    )

    await bot.send_message(chat_id=message.chat.id, text=f"Привет! Я ваш бот. Мой токен {message.bot.token}")


ORIGINS = [
    "http://localhost",
    "http://localhost:5173",
    "https://envelope-app.ru",
    "https://www.envelope-app.ru",
    "https://store.envelope-app.ru",
    "https://api.telegram.org",
]


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


for router in routers:
    app.include_router(router)
