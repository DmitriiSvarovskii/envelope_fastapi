from aiogram import Bot, Dispatcher
from typing import List, Dict, Tuple
from aiogram.filters import Command

from src.bot.handlers import start
from src.config import WEBHOOK_PATH, WEBHOOK_HOST


dispatchers_by_webhook_url: Dict[str, Tuple[Bot, Dispatcher]] = {}
bots: List[Bot] = []


def register_handlers(dp: Dispatcher):
    dp.message.register(start, Command('start'))


async def create_bot(token: str) -> Tuple[Bot, Dispatcher]:
    bot = Bot(token)
    dp = Dispatcher()
    register_handlers(dp)
    dispatchers_by_webhook_url[f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"] = (
        bot, dp)
    await setup_webhook_for_bot(bot, f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}")
    return bot, dp


async def add_new_bot(token: str):
    bot, dp = await create_bot(token)
    bots.append(bot)


async def init_multibots(tokens: List[Dict[str, str]]):
    for token_info in tokens:
        token = token_info["token_bot"]
        bot, dp = await create_bot(token)
        dispatchers_by_webhook_url[f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}"] = (
            bot, dp)
        await setup_webhook_for_bot(bot, f"{WEBHOOK_HOST}{WEBHOOK_PATH}/{token}")


async def setup_webhook_for_bot(bot: Bot, webhook_url: str):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != webhook_url:
        await bot.set_webhook(url=webhook_url)
