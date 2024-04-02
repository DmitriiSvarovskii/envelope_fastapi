import logging
from fastapi import HTTPException, Request, APIRouter
from aiogram.types import Update

from src.database import get_async_session
from src.config import WEBHOOK_PATH, WEBHOOK_HOST

from src.bot.services import (  # noqa: F401
    dispatchers_by_webhook_url,
    bots,
    create_bot,
    setup_webhook_for_bot
)
from src.bot.services import get_info_store_token_all


router = APIRouter(
    prefix=f"{WEBHOOK_PATH}",
    tags=["Webhook (telegram_bot)"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/{token}")
async def bot_webhook(request: Request, token: str):
    # Логируем получение обновления
    update_data = await request.json()
    logger.info(f"Received update for token {token}: {update_data}")

    # Создание объекта Update
    update = Update(**update_data)

    # Построение URL вебхука и поиск пары bot, dp
    webhook_url = f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"
    pair = dispatchers_by_webhook_url.get(webhook_url)

    # Логирование в случае, если бот не найден
    if not pair:
        logger.error(f"Bot not found for webhook URL: {webhook_url}")
        raise HTTPException(status_code=404, detail="Bot not found")

    # Получение бота и диспетчера, отправка обновления диспетчеру
    bot, dp = pair
    await dp.feed_update(bot, update)
    logger.info(f"Update for token {token} fed to dispatcher")


@router.on_event("startup")
async def on_startup_bot():
    logger.info("Starting up bots")
    global bots
    tokens = []

    async for session in get_async_session():
        try:
            store = await get_info_store_token_all(session)
            tokens.extend([{"token_bot": bot.token_bot} for bot in store])
            logger.info(f"Found {len(tokens)} bots in the database")
        except Exception as e:
            logger.error(f"Error in getting tokens from database: {e}")
            continue

    for token_info in tokens:
        token = token_info["token_bot"]
        try:
            bot, dp = await create_bot(token)
            bots.append(bot)
            webhook_url = f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"
            dispatchers_by_webhook_url[webhook_url] = (bot, dp)
            await setup_webhook_for_bot(bot, webhook_url)
            logger.info(f"Bot with token {token} started and webhook set")
        except Exception as e:
            logger.error(f"Error in creating bot with token {token}: {e}")


@router.on_event("shutdown")
async def on_shutdown_bot():
    global bots
    for bot in bots:
        if bot.session:
            try:
                await bot.session.close()
            except Exception as e:
                print(f"Ошибка при закрытии сессии бота: {e}")
