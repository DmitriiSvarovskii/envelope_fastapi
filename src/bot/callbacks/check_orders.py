from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CheckOrdersCallbackFactory(CallbackData, prefix='ord', sep='_'):
    order_id: int
    order_sum: int
    user_id: int
    order_status: str
    status: str
    message_id: Optional[int] = None
