from src.database import get_async_session
from src.api_admin.store.crud import crud_get_info_store_token_all
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi import Request, APIRouter
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Update
from typing import List, Dict, Tuple

from src.config import WEBHOOK_PATH, WEBHOOK_HOST
from src.bot.handlers import start

dispatchers_by_webhook_url: Dict[str, Tuple[Bot, Dispatcher]] = {}
bots: List[Bot] = []

router = APIRouter(
    prefix=f"{WEBHOOK_PATH}",
    tags=["Webhook (telegram_bot)"])


def register_handlers(dp: Dispatcher):
    dp.message.register(start, Command('start'))


async def create_bot(token: str) -> Tuple[Bot, Dispatcher]:
    bot = Bot(token)
    dp = Dispatcher()
    register_handlers(dp)
    return bot, dp


async def init_multibots(tokens: List[Dict[str, str]]):
    for token_info in tokens:
        token = token_info["token_bot"]
        bot, dp = await create_bot(token)
        dispatchers_by_webhook_url[f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"] = (
            bot, dp)
        await setup_webhook_for_bot(bot, f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}")


@router.post("/{token}")
async def bot_webhook(request: Request, token: str):
    update_data = await request.json()
    update = Update(**update_data)
    webhook_url = f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"
    pair = dispatchers_by_webhook_url.get(webhook_url)
    if not pair:
        raise HTTPException(status_code=404, detail="Bot not found")
    bot, dp = pair
    await dp.feed_update(bot, update)


@router.on_event("startup")
async def on_startup_bot():
    global bots
    async for session in get_async_session():
        store = await crud_get_info_store_token_all(session)
        tokens = [{"token_bot": bot.token_bot} for bot in store]
    for token_info in tokens:
        token = token_info["token_bot"]
        bot, dp = await create_bot(token)
        bots.append(bot)
        dispatchers_by_webhook_url[f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"] = (
            bot, dp)
        await setup_webhook_for_bot(bot, f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}")


async def setup_webhook_for_bot(bot: Bot, webhook_url: str):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != webhook_url:
        await bot.set_webhook(url=webhook_url)


@router.on_event("shutdown")
async def on_shutdown_bot():
    global bots
    for bot in bots:
        await bot.session.close()
