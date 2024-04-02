from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import Optional


async def new_order_mess_text_customer(
        order_id: int,
        tg_user_id: int,
        order_text: str,
        order_sum: int,
        adress: str,
        number_phone: str,
        customer_comment: str
):
    try:
        current_time = datetime.now()
        coocking_time = timedelta(minutes=45)
        order_time = current_time + coocking_time

        text = f"Заказ №{order_id} от {current_time.strftime('%d.%m.%Y')}" \
            f"в {current_time.strftime('%H:%M')}\n" \
            f"Код клиента: {tg_user_id}\n" \
            "--------------------\n" \
            "Ваш выбор:\n\n" \
            f"{order_text}" \
            f"\nСумма: {order_sum} руб.\n" \
            "--------------------\n" \
            f"Статус: Новый\n" \
            f"Дата и время выдачи: {order_time.strftime('%d.%m.%Y %H:%M')}\n" \
            "--------------------\n" \
            f"Адрес заведения: {adress}\n" \
            f"Телефон заведения: {number_phone}\n" \
            f"Комментарий к заказу: {customer_comment}"
        return text
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")


async def new_order_mess_text_order_chat(
        order_id: int,
        tg_user_id: int,
        order_text: str,
        order_sum: int,
        customer_name: str,
        customer_phone: str,
        tg_user_name:  Optional[str] = None,
        customer_comment: Optional[str] = None,
        table_number: Optional[str] = None,
        delivery_address: Optional[str] = None
):
    try:
        current_time = datetime.now()
        coocking_time = timedelta(minutes=45)
        order_time = current_time + coocking_time

        text = (
            f"❗️ НОВЫЙ ЗАКАЗ №{order_id} от "
            f"{current_time.strftime('%d.%m.%Y')} в "
            f"{current_time.strftime('%H:%M')}\n"
            "--------------------\n"
            "Информация о клиенте:\n"
            f"Код клиента: {tg_user_id}\n"
            f"Стол №: {table_number}\n"
            f"Имя клиента: {customer_name}\n"
            f"Телефон: {customer_phone}\n"
            f"Ссылка tg: @{tg_user_name}\n"
            f"Адрес доставки: {delivery_address}\n"
            "--------------------\n"
            "Заказ:\n\n"
            f"{order_text}"
            f"\nКомментарий к заказу: {customer_comment}\n"
            f"\nСумма: {order_sum} руб.\n"
            "--------------------\n"
            "Статус заказа: Новый\n"
            f"Дата и время выдачи: {order_time.strftime('%d.%m.%Y %H:%M')}\n"
            "--------------------\n"
        )

        return text
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отправке сообщения: {str(e)}")
