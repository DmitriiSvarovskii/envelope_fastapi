from aiogram import Router  # , F
from aiogram.filters import Command, CommandStart  # noqa: F401
from ..callbacks import (
    CheckOrdersCallbackFactory,
    CheckOrderCashCallbackFactory,
)
from .payment_cash import press_payment_cash
from .start import process_start_command
from .check_order import order_processing
from .message import (  # noqa: F401
    new_order_mess_text_customer,
    new_order_mess_text_order_chat
)


def register_user_commands(router: Router) -> None:
    router.message.register(process_start_command, CommandStart())
    router.callback_query.register(
        order_processing, CheckOrdersCallbackFactory.filter())
    router.callback_query.register(
        press_payment_cash, CheckOrderCashCallbackFactory.filter())
