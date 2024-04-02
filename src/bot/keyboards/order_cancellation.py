from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.bot.callbacks import CheckOrdersCallbackFactory


def create_order_cancellation_keyboard(
    order_id: int,
    message_id: int,
    user_id: int,
    order_status: str,
    order_sum: int
):
    button_cancel: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить заказ',
        callback_data=CheckOrdersCallbackFactory(
            order_id=order_id,
            message_id=message_id,
            user_id=user_id,
            order_status=order_status,
            order_sum=order_sum,
            status='cancel'
        ).pack())
    keyboard_new_order_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_new_order_builder.row(button_cancel, width=1)
    keyboard_new_order = keyboard_new_order_builder.as_markup()
    return keyboard_new_order
