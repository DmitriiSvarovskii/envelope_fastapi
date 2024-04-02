from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_payment_cash_keyboard(
    url: int,
):
    button_store: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата картой',
        url=url)
    keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_store_builder.row(button_store, width=1)
    keyboard_store = keyboard_store_builder.as_markup()
    return keyboard_store
