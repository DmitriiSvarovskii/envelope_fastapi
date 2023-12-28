import yookassa
from aiohttp import web

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func

from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from typing import List
from src.api_admin.product.schemas import *
from src.api_admin.product.crud import *
from src.api_admin.category.schemas import *
from src.api_admin.category.crud import *
from src.database import get_async_session
from src.bot.massage_handlers import new_order_mess_text_customer
from src.bot.callback_factory import *


def create_keyboard_order(url: int):
    button_store: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата наличными',
        callback_data='payment_cash')
    button_store2: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата картой',
        url=url)
    keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_store_builder.row(button_store2, button_store, width=1)
    keyboard_store = keyboard_store_builder.as_markup()
    return keyboard_store


        # callback_data="CheckOrdersCallbackFactory")
        # callback_data="CheckOrdersCallbackFactory")


def create_keyboard_order_admin_chat(order_id: int,user_id: int, status: str):
    button_done: InlineKeyboardButton = InlineKeyboardButton(
        text='Принять',
        callback_data=CheckOrdersCallbackFactory(
            order_id=order_id,
            user_id=user_id,
            status=status
        ).pack())
    button_cancel: InlineKeyboardButton = InlineKeyboardButton(
        text='Отклонить',
        callback_data=CheckOrdersCallbackFactory(
            order_id=order_id,
            user_id=user_id,
            status=status
        ).pack())
    keyboard_new_order_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_new_order_builder.row(button_done, button_cancel, width=2)
    keyboard_new_order = keyboard_new_order_builder.as_markup()
    return keyboard_new_order
