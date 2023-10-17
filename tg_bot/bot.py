from aiogram import Dispatcher, Bot, types
from config import TELEGRAM_BOT_TOKEN
from random import shuffle

predict = ['Вижу на канал ты подпишешься!',
           'Сегодня тебя ждёт успех!',
           'Сегодня ты научишься пользоваться хуками!']

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    shuffle(predict)
    await message.answer(f"{message.from_user.full_name}, {predict[0]}. Приходи ещё!")
