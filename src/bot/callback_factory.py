from aiogram.filters.callback_data import CallbackData


class CheckOrdersCallbackFactory(CallbackData, prefix='chkord', sep='_'):
    order_id: int
    user_id: int
    status: str
