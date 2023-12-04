from aiogram import Bot, types
import io
import requests
from aiogram.types import InputFile
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
from aiogram import Bot, Dispatcher
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
from ..product.controller import s3
from ..auth.routers import get_current_user_from_token
from src.config import BUCKET_NAME, ENDPOINT_URL
from PIL import Image
import io
import os

router = APIRouter(
    prefix="/api/v1/mail",
    tags=["Mail (bot)"])


bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()


photo_url = 'https://storage.yandexcloud.net/envelope-app/13/2/california-rolls.jpeg'


@router.post("/send_message/")
async def send_message(data: TextMail, store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        customers = await get_all_customer(store_id=store_id, current_user=current_user, session=session)
        for customer in customers:
            tg_user_id = customer.tg_user_id
            try:
                if data.photo_url:
                    await bot.send_photo(chat_id=tg_user_id, photo=photo_url, caption=f"{data.mail_text}", parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    await bot.send_message(chat_id=tg_user_id, text=f"{data.mail_text}", parse_mode=ParseMode.MARKDOWN_V2)
            except tg_exceptions.TelegramBadRequest as e:
                print(
                    f"Ошибка при отправке сообщения пользователю {tg_user_id}: {e}")
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


@router.post("/send_message_group/")
async def send_message(data: TextMail, store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        customers = await get_all_customer(store_id=store_id, current_user=current_user, session=session)
        for customer in customers:
            tg_user_id = customer.tg_user_id
            try:
                if data.photo_url:
                    await bot.send_photo(chat_id=tg_user_id, photo=photo_url, caption=f"{data.mail_text}", parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    await bot.send_message(chat_id=tg_user_id, text=f"{data.mail_text}", parse_mode=ParseMode.MARKDOWN_V2)
            except tg_exceptions.TelegramBadRequest as e:
                print(
                    f"Ошибка при отправке сообщения пользователю {tg_user_id}: {e}")
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


@router.post("/upload_photo/")
async def process_and_upload_photo(file: UploadFile, store_id: int, current_user: User = Depends(get_current_user_from_token)):
    try:
        image = Image.open(io.BytesIO(await file.read()))

        image.thumbnail((900, 900))

        with io.BytesIO() as output_buffer:
            image.save(output_buffer, format="WebP")
            output_buffer.seek(0)
            webp_image = Image.open(output_buffer)

        current_datetime = datetime.now()
        current_date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        object_key = f"{current_user.id}/{store_id}/mail/{current_date_str}_{file.filename}"

        with io.BytesIO() as webp_output_buffer:
            webp_image.save(webp_output_buffer, format="WebP")
            webp_output_buffer.seek(0)
            s3.upload_fileobj(webp_output_buffer, BUCKET_NAME, object_key)

        object_url = f'{ENDPOINT_URL}/{BUCKET_NAME}/{object_key}'

        return object_url
    except Exception as e:
        return f"Error processing and uploading photo: {str(e)}"
