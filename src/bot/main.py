# from aiogram.filters import BaseFilter
# from aiogram import Bot, Dispatcher
# from aiogram.filters import Command

# from src.config import BOT_TOKEN
# from aiogram.types import Message
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram import types, Router, F
# from aiogram.filters import CommandStart

# stroge = MemoryStorage()


# class IsPrivate(BaseFilter):
#     async def __call__(self, message: Message):
#         return message.chat.type == 'private'


# bot = Bot(token=BOT_TOKEN, parse_mode='html')
# dp = Dispatcher(storage=stroge)

# private_router = Router()
# private_router.message.filter(IsPrivate())


# @private_router.message(CommandStart())
# async def start(message: Message):
#     await message.answer(text='Работает')


# # @dp.message(Command(commands=['/start']))
# # async def start(message: Message):
# #     await message.answer(text='Работает')
