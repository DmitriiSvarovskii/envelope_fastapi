from aiogram import exceptions as tg_exceptions
from sqlalchemy import select, union_all
from sqlalchemy.orm import aliased
from aiohttp import web
import yookassa
from datetime import datetime, timedelta
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Dict, List, Union
from aiogram.types import Message

from sqlalchemy import insert, select, label, join, update, delete
from ..user import User

from ..auth.routers import get_current_user_from_token
from ..customer.schemas import CustomerCreate
from .schemas import TextMail
from ..customer.schemas import CustomerCreate
from ..customer.routers import get_all_customer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Dict, Optional
from src.api_admin.product.schemas import *
from src.api_admin.product.crud import *
from src.api_admin.category.schemas import *
from src.api_admin.category.crud import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.config import BOT_TOKEN


router = APIRouter(
    prefix="/api/v1/mail",
    tags=["Mail (bot)"])


bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@router.post("/send_message/")
async def send_message(data: TextMail, store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        customers = await get_all_customer(store_id=store_id, current_user=current_user, session=session)
        for customer in customers:
            tg_user_id = customer.tg_user_id
            try:
                await bot.send_message(tg_user_id, f"{data.mail_text}", parse_mode=ParseMode.HTML)
            except tg_exceptions.TelegramBadRequest as e:
                print(
                    f"Ошибка при отправке сообщения пользователю {tg_user_id}: {e}")
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")
