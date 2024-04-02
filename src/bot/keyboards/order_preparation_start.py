from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_order_preparation_start_keyboard(url: int):
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
