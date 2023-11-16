from keyboards import keyboard_store
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router
from aiogram.methods.answer_web_app_query import AnswerWebAppQuery
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from ..api_admin.models import Customer, Store
from sqlalchemy import insert, select, delete, update
from src.config import BOT_TOKEN

router: Router = Router()


@router.message(CommandStart())
async def start(message: Message, session: AsyncSession = Depends(get_async_session)):
    await message.answer(text=f'Привет, {message.chat.first_name}!\n'
                         'Для заказа в нашем кафе воспользуйся онлайн-сервисом)\n\n'
                         f'{message.chat.first_name}, твой user_id телеграм - {message.chat.id}')
    query = select(Customer).where(
        Customer.tg_user_id == message.chat.id).where(Store.token_bot == BOT_TOKEN).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories
    # if not await db.user_exists(message.chat.id):
    #     await db.add_users(message.chat.id, message.chat.first_name, message.chat.username)
    await message.delete()
