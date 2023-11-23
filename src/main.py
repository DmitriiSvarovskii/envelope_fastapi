from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from aiogram import Bot, Dispatcher
# from aiogram.types import Update, Message

from src.api_admin.routers import routers
# from src.config import BOT_TOKEN, URL_NGROK
# from src.bot.main import bot, dp


app = FastAPI(
    title="Envelope-app",
    version="1.0.0a",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)
# WEBHOOK_PATH = f'/bot{BOT_TOKEN}'
# WEBHOOK_URL = f'{URL_NGROK}{WEBHOOK_PATH}'


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


# @app.on_event("startup")
# async def on_startup():
#     webhook_info = await bot.get_webhook_info()
#     print(webhook_info)
#     if webhook_info != WEBHOOK_URL:
#         await bot.set_webhook(
#             url=WEBHOOK_URL
#         )


# @app.post("/")
# async def start(message: Message):
#     await message.answer(text='Работает')
# # async def bot_webook(update: dict):
# #     telegram_update = Update(**update)
# #     print(telegram_update)
# #     await dp.feed_update(bot=bot, update=telegram_update)


for router in routers:
    app.include_router(router)


# @app.on_event("shutdown")
# async def on_shutdown():
#     await bot.session.close()
