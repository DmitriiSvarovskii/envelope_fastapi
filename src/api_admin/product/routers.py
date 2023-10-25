from sqlalchemy import and_
from sqlalchemy.orm import selectinload
import jwt
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from urllib.parse import unquote
from hashlib import sha256
import re
import base64
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from .models import Product
from src.api_admin.category.models import Category
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Annotated
from src.secure import apikey_scheme
from fastapi import FastAPI, HTTPException
import hashlib
import hmac


router = APIRouter(
    prefix="/api/v1/product",
    tags=["Product"])


@router.get("/", summary="Получение списка продуктов", response_model=List[ProductList])
async def get_all_product(session: AsyncSession = Depends(get_async_session)):
    """
    Получение списка продуктов.

    Этот маршрут позволяет получить список всех доступных продуктов, исключая те, у которых `deleted_flag` равен `True`.

    Возвращает:
    - Список продуктов.
    """
    stmt = select(Product).options(selectinload(
        Product.category)).where(Product.deleted_flag != True).order_by(Product.id)
    result = await session.execute(stmt)
    products = result.scalars().all()
    product_dicts = [
        {
            "id": product.id,
            "category_id": product.category.name_rus,
            "name_rus": product.name_rus,
            "price": product.price,
            "availability": product.availability,
            "popular": product.popular,
            "delivery": product.delivery,
            "takeaway": product.takeaway,
            "dinein": product.dinein
        }
        for product in products
    ]
    return product_dicts


@router.post("/", summary="Создание нового продукта", response_model=dict)
async def create_new_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Создание нового продукта.

    Этот маршрут позволяет создать новый продукт.

    Параметры:
    - `new_product`: данные для создания нового продукта.

    Возвращает:
    - Сообщение о успешном создании.
    """
    try:
        stmt = insert(Product).values(**new_product.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": 201, 'date': new_product}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/", summary="Обновление продукта", response_model=dict)
async def update_product(product_id: int, new_data: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Обновление продукта.

    Этот маршрут позволяет обновить данные о существующем продукте.

    Параметры:
    - `product_id`: идентификатор продукта.
    - `new_data`: данные для обновления.

    Возвращает:
    - Сообщение о успешном обновлении.
    """
    stmt = update(Product).where(
        Product.id == product_id).values(**new_data.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/{product_id}/checkbox/", summary="Изменение поля продукта", response_model=dict)
async def update_product_field(product_id: int, checkbox: str, session: AsyncSession = Depends(get_async_session)):
    """
    Изменение поля продукта.

    Этот маршрут позволяет изменить определенное поле продукта.

    Параметры:
    - `product_id`: идентификатор продукта.
    - `checkbox`: имя поля, которое требуется изменить.
    Для продуктов доступны следующие значения: `availability`, `popular`, `delivery`, `takeaway`, `dinein`

    Возвращает:
    - Сообщение о успешном изменении или ошибку, если продукт не найден или поле не существует.
    """
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    if not hasattr(product, checkbox):
        raise HTTPException(status_code=400, detail="Поле не существует")
    setattr(product, checkbox, not getattr(product, checkbox))
    await session.commit()
    return {"status": "success"}


@router.put("/delete/", summary="Удаление/восстановление продукта", response_model=dict)
async def delete_product(product_id: int, session: Session = Depends(get_async_session)):
    """
    Удаление/восстановление продукта.

    Этот маршрут позволяет удалить или восстановить продукт.

    Параметры:
    - `product_id`: идентификатор продукта.

    Возвращает:
    - Сообщение о успешном удалении/восстановлении продукта.
    """
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    product.deleted_flag = not product.deleted_flag
    product.deleted_at = datetime.now()
    await session.commit()

    return {"message": "Продукт успешно перенесён в удалённые"}


@router.delete("/", summary="Удаление продукта", response_model=dict)
async def delete_product(product_id: int, session: Session = Depends(get_async_session)):
    """
    Удаление продукта.

    Этот маршрут позволяет удалить продукт.

    Параметры:
    - `product_id`: идентификатор продукта.

    Возвращает:
    - Сообщение о успешном удалении или ошибке, если удаление не удалось.
    """
    try:
        stmt = delete(Product).where(Product.id == product_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": f"Продукт, c id {product_id}, успешно удален."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# @router.get("/{product_id}/", response_model=List[ProductOne])
# async def get_one_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = select(Product).where(Product.id == product_id)
#     result = await session.execute(query)
#     products = result.scalars().all()
#     product_dicts = [product.__dict__ for product in products]
#     return product_dicts


# @router.get("/products/{shop_id}/")
# async def get_all_products(shop_id: int, user_data=Depends(verify_token), session: AsyncSession = Depends(get_async_session)) -> List[ProductList]:
#     print(shop_id)
#     print(user_data)
#     # Проверка, что пользователь имеет доступ к магазину shop_id
#     # user_data может содержать идентификатор пользователя или другую информацию, которая помогает в этой проверке

#     # Пример проверки доступа, предполагая, что user_data содержит идентификатор пользователя
#     user_id = user_data.get("user_id")
#     if user_id is not None:
#         # Здесь вы можете выполнить проверку, имеет ли пользователь доступ к магазину shop_id
#         # Например, проверить, что пользователь имеет права доступа к этому магазину

#         # Если пользователь имеет доступ, выполните запрос к базе данных
#         query = select(Product).where(Product.shop_id ==
#                                       shop_id).where(Product.availability == True)
#         result = await session.execute(query)
#         return result.scalars().all()
#     else:
#         raise HTTPException(status_code=403, detail="Access denied")


# @router.get("/", response_model=List[ProductList])
# async def get_all_product(session: AsyncSession = Depends(get_async_session)):
#     # query = select(Product).order_by(Product.id)
#     # result = await session.execute(query)
#     # products = result.scalars().all()
#     # Выберите все поля из таблицы Product и связанное поле category
#     stmt = select(Product).options(selectinload(
#         Product.category)).order_by(Product.id)

#     result = await session.execute(stmt)
#     products = result.scalars().all()
#     product_dicts = [product.__dict__ for product in products]
#     return product_dicts


# BOT_TOKEN = '6141111072:AAH8CBhf7iQUVNFCjR_STaBf9h_mYHSggvo'


# c_str = "WebAppData"


# def is_valid_data(init_data_hash: str, init_data: str) -> bool:
#     init_data = unquote(init_data)
#     init_data = sorted([chunk.split("=")
#                         for chunk in unquote(init_data).split("&")
#                         if chunk[:len("hash=")] != "hash="],
#                        key=lambda x: x[0])
#     init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])
#     print(unquote(init_data))
#     print(init_data)

#     secret_key = hmac.new(c_str.encode(), BOT_TOKEN.encode(),
#                           hashlib.sha256).digest()
#     data_check = hmac.new(secret_key, init_data.encode(),
#                           hashlib.sha256)
#     print(data_check.hexdigest())
#     print(init_data_hash)
#     return data_check.hexdigest() == init_data_hash


# # b0c8bb03576e9ecf85171fe151bee2f996dec619353ce4a2bce72d6337f24678
# # query_id%3DAAGVbSskAAAAAJVtKyQX6XyE&user%3D%257B%2522id%2522%253A606825877%252C%2522first_name%2522%253A%2522%25D0%2594%25D0%25BC%25D0%25B8%25D1%2582%25D1%2580%25D0%25B8%25D0%25B9%2522%252C%2522last_name%2522%253A%2522%25D0%25A1%25D0%25B2%25D0%25B0%25D1%2580%25D0%25BE%25D0%25B2%25D1%2581%25D0%25BA%25D0%25B8%25D0%25B9%2522%252C%2522username%2522%253A%2522swarovskidima%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522is_premium%2522%253Atrue%252C%2522allows_write_to_pm%2522%253Atrue%257D&auth_date%3D1696961678&hash%3Db0c8bb03576e9ecf85171fe151bee2f996dec619353ce4a2bce72d6337f24678


# @router.post("/validate_data/")
# async def validate_data(init_data_hash: str, data_check_string: str):
#     if is_valid_data(init_data_hash, data_check_string):
#         expiration_time = datetime.utcnow() + timedelta(hours=2)
#         payload = {"user_id": 123, "exp": expiration_time}
#         jwt_token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')
#         return {"access_token": jwt_token}
#     else:
#         raise HTTPException(status_code=400, detail="Data is not valid")


# # Функция для извлечения JWT-токена из заголовка запроса
# def get_token(authorization: str = Header(None)):
#     print(1, '', authorization)
#     if not authorization:
#         raise HTTPException(
#             status_code=401, detail="Authorization header is missing")
#     token_type, token = authorization.split(" ")
#     print(2, '', token)
#     print(3, '', token_type)
#     if token_type != "Bearer":
#         raise HTTPException(status_code=401, detail="Invalid token type")
#     return token


# def verify_token(token: str = Depends(get_token)):
#     print(token)
#     try:
#         decoded_payload = jwt.decode(
#             token, 'your-secret-key', algorithms=['HS256'])
#         # Здесь вы можете проверить, что токен действителен и содержит нужную информацию о пользователе
#         return decoded_payload
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# @router.post("/validate_data/")
# async def validate_data(init_data_hash: str, data_check_string: str):
#     if is_valid_data(init_data_hash, data_check_string):
#         return {"message": "Data is from Telegram"}
#     else:
#         raise HTTPException(status_code=400, detail="Data is not valid")


# @router.get("/products/{shop_id}/")
# async def get_all_products(shop_id: int, session: AsyncSession = Depends(get_async_session)) -> List[ProductList]:
#     query = select(Product).where(Product.shop_id ==
#                                   shop_id).where(Product.availability == True)
#     result = await session.execute(query)
#     return result.scalars().all()
