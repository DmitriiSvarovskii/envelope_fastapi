from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo


web_app = WebAppInfo(url='https://envelope-app.ru/login/')


button_store: InlineKeyboardButton = InlineKeyboardButton(
    text='Онлайн-кафе',
    web_app=web_app)

keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

keyboard_store_builder.row(button_store)
keyboard_store = keyboard_store_builder.as_markup()
