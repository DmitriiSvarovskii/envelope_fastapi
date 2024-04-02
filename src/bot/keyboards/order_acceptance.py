from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.bot.callbacks import CheckOrdersCallbackFactory


def create_order_acceptance_keyboard(
    order_id: int,
    message_id: int,
    order_sum: int,
    user_id: int,
    order_status: str
):
    button_done: InlineKeyboardButton = InlineKeyboardButton(
        text='Принять',
        callback_data=CheckOrdersCallbackFactory(
            message_id=message_id,
            order_id=order_id,
            order_sum=order_sum,
            user_id=user_id,
            order_status=order_status,
            status='done'
        ).pack())
    button_cancel: InlineKeyboardButton = InlineKeyboardButton(
        text='Отклонить',
        callback_data=CheckOrdersCallbackFactory(
            message_id=message_id,
            order_id=order_id,
            order_sum=order_sum,
            user_id=user_id,
            order_status=order_status,
            status='cancel'
        ).pack())
    keyboard_new_order_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_new_order_builder.row(button_done, button_cancel, width=2)
    keyboard_new_order = keyboard_new_order_builder.as_markup()
    return keyboard_new_order
