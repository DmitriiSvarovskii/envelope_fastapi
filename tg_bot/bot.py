from aiogram import Dispatcher, Bot
from aiogram.types import Message

from tg_bot.config import TELEGRAM_BOT_TOKEN
from random import shuffle
from aiogram.filters import Command
predict = ['Вижу на канал ты подпишешься!',
           'Сегодня тебя ждёт успех!',
           'Сегодня ты научишься пользоваться хуками!']

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands="start"))
async def start(message: Message):
    shuffle(predict)
    await message.answer(f"{message.from_user.full_name}, {predict[0]}. Приходи ещё!")
