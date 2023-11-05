from keyboards import keyboard_store
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router
from aiogram.methods.answer_web_app_query import AnswerWebAppQuery


router: Router = Router()


@router.message(CommandStart())
async def start(message: Message):
    # await message.answer_sticker(r'CAACAgIAAxkBAAEKO7lk-E08zJ0kc9UCUgkAAXVolbuDvd0AAmIJAAJ5XOIJioxy4DY9M7gwBA')
    await message.answer(text=f'Привет, {message.chat.first_name}!\n'
                         'Для заказа в нашем кафе воспользуйся онлайн-сервисом)',
                         reply_markup=keyboard_store)
    await message.delete()
