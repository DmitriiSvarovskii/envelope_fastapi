from aiogram.types import CallbackQuery
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from src.api_admin.payment.payment_handlers import create_pay
from ..callbacks import CheckOrdersCallbackFactory
from ..keyboards import create_payment_cash_keyboard


async def press_payment_cash(
    call: CallbackQuery,
    callback_data: CheckOrdersCallbackFactory,
    bot: Bot
):
    try:
        text = (
            "--------------------\n"
            f"Обновление заказа №{callback_data.order_id}.\n"
            "Выбран тип оплаты: наличные.\n"
        )
        customer_text = text + (
            "При необходимости Вы можете оплатить заказ онлайн.\n"
            "--------------------"
        )

        url, payment_id = await create_pay(
            total_price=callback_data.order_sum,
            order_id=callback_data.order_id
        )

        keyboard = create_payment_cash_keyboard(url=url)

        await call.message.edit_text(
            text=customer_text,
            reply_markup=keyboard
        )
        # await bot.send_message(
        #         chat_id=user_id,
        #         text=text,
        #         reply_markup=None
        #     )
        await bot.send_message(
            chat_id=-1002144078281,
            text='❗️'+text+'❗️'
        )

    except TelegramBadRequest:
        pass
