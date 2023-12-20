from fastapi import HTTPException, Request, APIRouter
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from typing import List, Dict, Tuple

from src.database import get_async_session
from src.config import WEBHOOK_PATH, WEBHOOK_HOST

from src.bot.bot_management import dispatchers_by_webhook_url, create_bot, setup_webhook_for_bot, bots
from src.bot.bot_get_info import get_info_store_token_all


router = APIRouter(
    prefix=f"{WEBHOOK_PATH}",
    tags=["Webhook (telegram_bot)"])


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
        store = await get_info_store_token_all(session)
        tokens = [{"token_bot": bot.token_bot} for bot in store]
    for token_info in tokens:
        token = token_info["token_bot"]
        bot, dp = await create_bot(token)
        bots.append(bot)
        dispatchers_by_webhook_url[f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"] = (
            bot, dp)
        await setup_webhook_for_bot(bot, f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}")


@router.on_event("shutdown")
async def on_shutdown_bot():
    global bots
    for bot in bots:
        await bot.session.close()
