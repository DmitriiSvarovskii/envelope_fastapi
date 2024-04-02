# from yookassa import Configuration, Webhook
import yookassa
from aiohttp import web
# from fastapi import Request, APIRouter
# from src.config import WEBHOOK_HOST


# router = APIRouter(
#     prefix="/api/v1/payment",
#     tags=["Payment"])

api_id = '278535'
api_key = 'test_W5YF4StOK5ZheXJWyIodZUAUJdhU7fYMm5DFRLQI7Ww'


async def create_pay(total_price: int, order_id: int):
    print("Получен обратный вызов от YooKassa:")

    yookassa.Configuration.account_id = api_id
    yookassa.Configuration.secret_key = api_key

    payment = yookassa.Payment.create({
        "amount": {
            "value": total_price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": 'https://t.me/store_demo_envelope_app_bot'
        },
        "description": f"Оплата заказа №{order_id}",
        "capture": True
    })
    url = payment.confirmation.confirmation_url
    return url, payment


async def payment_callback(request):
    data = await request.json()
    print("Получен обратный вызов от YooKassa:")
    print(data)
    return web.Response()


# @router.post("/notification_url")
# async def yookassa_notification(request: Request):
#     data = await request.json()
#     # Обрабатываем уведомление
#     if data['event'] == 'payment.succeeded':
#         # Логика обработки успешного платежа
#         payment_info = data['object']
#         print(f"Платеж {payment_info['id']} успешно совершен.")
#         # Дополнительная логика обработки...
#     return {"status": "OK"}
#     # url, payment_id = await create_pay(
#     #     total_price=order_sum,
#     #     order_id=order_id
#     # )


# Configuration.configure_auth_token('<Bearer Token>')

# response = Webhook.add({
#     "event": "payment.succeeded",
#     "url": f"{WEBHOOK_HOST}/notification_url",
# })
