from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo


web_app = WebAppInfo(url='https://store.envelope-app.ru/schema=10/store_id=1/')


button_store: InlineKeyboardButton = InlineKeyboardButton(
    text='Онлайн-кафе',
    web_app=web_app)


keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

keyboard_store_builder.row(button_store)
keyboard_store = keyboard_store_builder
