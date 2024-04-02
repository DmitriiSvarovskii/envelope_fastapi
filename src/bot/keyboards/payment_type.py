from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..callbacks import CheckOrderCashCallbackFactory


def create_payment_type_keyboard(
    url: int,
    order_id: int,
    message_id: int,
    order_sum: int,
    user_id: int,
    order_status: str
):
    button_store: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата наличными',
        callback_data=CheckOrderCashCallbackFactory(
            message_id=message_id,
            order_id=order_id,
            order_sum=order_sum,
            user_id=user_id,
            order_status=order_status,
            status='done'
        ).pack()
    )

    button_store2: InlineKeyboardButton = InlineKeyboardButton(
        text='Оплата картой',
        url=url)
    keyboard_store_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_store_builder.row(button_store2, button_store, width=1)
    keyboard_store = keyboard_store_builder.as_markup()
    return keyboard_store
