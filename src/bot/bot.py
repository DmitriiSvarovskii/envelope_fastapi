from fastapi import Request, APIRouter
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update
from typing import List

from src.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_HOST
from src.bot.handlers import start


TOKEN = BOT_TOKEN
WEBHOOK_HOST = WEBHOOK_HOST
WEBHOOK_PATH = WEBHOOK_PATH
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

router = APIRouter(
    prefix=f"{WEBHOOK_PATH}",
    tags=["Webhook (telegram_bot)"])

bot = Bot(token=TOKEN)
dp = Dispatcher()


def register_handlers(dp: Dispatcher):
    dp.message.register(start, (Command('start')))


@router.post('')
async def bot_webhook(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot, update)


@router.on_event("startup")
async def on_startup_bot():
    register_handlers(dp)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@router.on_event("shutdown")
async def on_shutdown_bot():
    await bot.session.close()
