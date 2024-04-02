import io
from datetime import datetime
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot, Dispatcher, exceptions as tg_exceptions
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.enums import ParseMode

from src.database import get_async_session
from src.config import settings
from .schemas import TextMail
from ..user import User
from ..auth.routers import get_current_user_from_token
from ..customer.routers import get_all_customer
from ..user.routers import get_one_user
from ..store.routers import get_one_store
from ..product.controller import s3


web_app = WebAppInfo(url='https://store.envelope-app.ru/schema=1/store_id=1/')


button_store: InlineKeyboardButton = InlineKeyboardButton(
    text='Онлайн-кафе',
    web_app=web_app)


keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

keyboard_store_builder.row(button_store)
keyboard_store = keyboard_store_builder.as_markup()


router = APIRouter(
    prefix="/api/v1/mail",
    tags=["Mail (admin)"])


bot = Bot(token=settings.BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@router.post("/send_message/")
async def send_message(
    data: TextMail,
    store_id: int,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        customers = await get_all_customer(
            store_id=store_id,
            current_user=current_user,
            session=session
        )
        for customer in customers:
            tg_user_id = customer.tg_user_id
            try:
                if data.photo_url:
                    await bot.send_photo(
                        chat_id=tg_user_id,
                        photo=data.photo_url,
                        caption=f"{data.mail_text}",
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                else:
                    await bot.send_message(
                        chat_id=tg_user_id,
                        text=f"{data.mail_text}",
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
            except tg_exceptions.TelegramBadRequest as e:
                print(
                    "Ошибка при отправке сообщения пользователю "
                    f"{tg_user_id}: {e}")
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


@router.post("/send_message_self/")
async def send_message_self(
    data: TextMail,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        tg_id = await get_one_user(current_user=current_user, session=session)
        if data.photo_url:
            await bot.send_photo(
                chat_id=tg_id.user_tg_id,
                photo=data.photo_url,
                caption=f"{data.mail_text}",
                parse_mode=ParseMode.MARKDOWN_V2
            )
        else:
            await bot.send_message(
                chat_id=tg_id.user_tg_id,
                text=f"{data.mail_text}",
                parse_mode=ParseMode.MARKDOWN_V2
            )
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except tg_exceptions.TelegramBadRequest as e:
        print(
            f"Ошибка при отправке сообщения в чат {tg_id.user_tg_id}: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


@router.post("/send_message_group/")
async def send_message_group(
    data: TextMail,
    store_id: int,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        tg_group = await get_one_store(
            store_id=store_id,
            current_user=current_user,
            session=session
        )
        if data.photo_url:
            await bot.send_photo(
                chat_id=tg_group.tg_id_group,
                photo=data.photo_url,
                caption=f"{data.mail_text}",
                parse_mode=ParseMode.MARKDOWN_V2
            )
        else:
            await bot.send_message(
                chat_id=tg_group.tg_id_group,
                text=f"{data.mail_text}",
                parse_mode=ParseMode.MARKDOWN_V2
            )
        return {"status": "success", "message": "Сообщение успешно отправлено"}
    except tg_exceptions.TelegramBadRequest as e:
        print(
            f"Ошибка при отправке сообщения в чат {tg_group.tg_id_group}: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


@router.post("/upload_photo/")
async def process_and_upload_photo(
    file: UploadFile,
    store_id: int,
    current_user: User = Depends(get_current_user_from_token)
):
    try:
        image = Image.open(io.BytesIO(await file.read()))

        image.thumbnail((900, 900))

        with io.BytesIO() as output_buffer:
            image.save(output_buffer, format="WebP")
            output_buffer.seek(0)
            webp_image = Image.open(output_buffer)

        current_datetime = datetime.now()
        current_date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        object_key = (
            f"{current_user.id}/{store_id}/"
            f"mail/{current_date_str}_{file.filename}"
        )
        with io.BytesIO() as webp_output_buffer:
            webp_image.save(webp_output_buffer, format="WebP")
            webp_output_buffer.seek(0)
            s3.upload_fileobj(webp_output_buffer,
                              settings.BUCKET_NAME, object_key)

        object_url = (
            f'{settings.ENDPOINT_URL}/{settings.BUCKET_NAME}/{object_key}'
        )

        return object_url
    except Exception as e:
        return f"Error processing and uploading photo: {str(e)}"
