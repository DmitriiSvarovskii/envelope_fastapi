from aiogram.types import CallbackQuery
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from ..callbacks import CheckOrdersCallbackFactory
from ..keyboards import (
    create_order_cancellation_keyboard,
    create_payment_type_keyboard
)
from src.api_admin.payment.payment_handlers import create_pay


async def order_processing(
    call: CallbackQuery,
    callback_data: CheckOrdersCallbackFactory,
    bot: Bot
):
    try:
        order_id = callback_data.order_id
        user_id = callback_data.user_id
        order_sum = callback_data.order_sum
        message_id = callback_data.message_id
        order_status = callback_data.order_status

        keyboard_order_done = create_order_cancellation_keyboard(
            order_id=order_id,
            order_sum=order_sum,
            user_id=user_id,
            order_status='Подтверждён',
            message_id=message_id
        )
        if callback_data.status == 'cancel':
            text = f'Заказ №{order_id} отменён.'
            await call.answer(text=text, show_alert=True)
            await bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=None
            )
            await bot.send_message(
                chat_id=-1002144078281,
                text='❗️'+text+'❗️'
            )
            await call.message.edit_reply_markup(reply_markup=None)
            if message_id:
                await bot.edit_message_reply_markup(
                    chat_id=-1002144078281,
                    message_id=message_id,
                    reply_markup=None
                )
        else:
            text = (
                "--------------------\n"
                f"Заказ №{order_id} подтверждён.\n"
                "--------------------\n"
            )
            text_customer = text + "Пожалуйста выберите способ оплаты"

            url, payment_id = await create_pay(
                total_price=order_sum,
                order_id=order_id
            )

            keyboard_payment = create_payment_type_keyboard(
                url=url,
                order_id=order_id,
                message_id=message_id,
                order_sum=order_sum,
                user_id=user_id,
                order_status=order_status,
            )

            await call.answer(
                text=text,
                show_alert=True
            )

            await bot.send_message(
                chat_id=user_id,
                text=text_customer,
                reply_markup=keyboard_payment
            )

            await call.message.edit_reply_markup(
                reply_markup=keyboard_order_done
            )

    except TelegramBadRequest:
        pass
