from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Product
from .schemas import *
from .crud import *
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/product",
    tags=["Product (admin)"])


@router.get("/", response_model=List[ProductList])
async def get_all_product(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    query = select(Product).options(selectinload(Product.category)).where(Product.deleted_flag != True).order_by(
        Product.id).execution_options(schema_translate_map={None: current_user.username})
    print(query)
    result = await session.execute(query)
    products = result.scalars().all()
    # return products
    product_dicts = [
        {
            "id": product.id,
            "category_id": product.category.id,
            "category_name": product.category.name,
            "name": product.name,
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


# @router.get("/", response_model=List[ProductList])
# async def get_all_product(schema: str, session: AsyncSession = Depends(get_async_session)):
#     query = select(Product).order_by(Product.id).execution_options(
#         schema_translate_map={None: schema})
#     result = await session.execute(query)
#     products = result.scalars().all()
#     return products


@router.post("/")
async def create_new_product(data: ProductCreate, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_product = await crud_create_new_product(schema=current_user.username, user_id=current_user.id, data=data, session=session)
        return new_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/", status_code=200)
async def update_product(product_id: int, data: ProductUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_product = await crud_update_product(schema=current_user.username, product_id=product_id, data=data, user_id=current_user.id, session=session)
        return up_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/{product_id}/checkbox/",)
async def update_product_field(product_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Параметры:
    #     - `product_id`: идентификатор продукта.
    #     - `checkbox`: имя поля, которое требуется изменить.
    #     Для продуктов доступны следующие значения: `availability`, `popular`, `delivery`, `takeaway`, `dinein`
    """
    try:
        change_product = await crud_update_product_field(schema=current_user.username, user_id=current_user.id, product_id=product_id, checkbox=checkbox, session=session)
        return change_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/delete/")
async def change_delete_flag_product(product_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_product = await crud_change_delete_flag_product(schema=current_user.username, user_id=current_user.id, product_id=product_id, session=session)
        return change_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/")
async def delete_product(product_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_product = await crud_delete_product(schema=current_user.username, product_id=product_id, session=session)
        return change_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# # @router.get("/{product_id}/", response_model=List[ProductOne])
# # async def get_one_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
# #     query = select(Product).where(Product.id == product_id)
# #     result = await session.execute(query)
# #     products = result.scalars().all()
# #     product_dicts = [product.__dict__ for product in products]
# #     return product_dicts


# # @router.get("/products/{shop_id}/")
# # async def get_all_products(shop_id: int, user_data=Depends(verify_token), session: AsyncSession = Depends(get_async_session)) -> List[ProductList]:
# #     print(shop_id)
# #     print(user_data)
# #     # Проверка, что пользователь имеет доступ к магазину shop_id
# #     # user_data может содержать идентификатор пользователя или другую информацию, которая помогает в этой проверке

# #     # Пример проверки доступа, предполагая, что user_data содержит идентификатор пользователя
# #     user_id = user_data.get("user_id")
# #     if user_id is not None:
# #         # Здесь вы можете выполнить проверку, имеет ли пользователь доступ к магазину shop_id
# #         # Например, проверить, что пользователь имеет права доступа к этому магазину

# #         # Если пользователь имеет доступ, выполните запрос к базе данных
# #         query = select(Product).where(Product.shop_id ==
# #                                       shop_id).where(Product.availability == True)
# #         result = await session.execute(query)
# #         return result.scalars().all()
# #     else:
# #         raise HTTPException(status_code=403, detail="Access denied")


# # @router.get("/", response_model=List[ProductList])
# # async def get_all_product(session: AsyncSession = Depends(get_async_session)):
# #     # query = select(Product).order_by(Product.id)
# #     # result = await session.execute(query)
# #     # products = result.scalars().all()
# #     # Выберите все поля из таблицы Product и связанное поле product
# #     stmt = select(Product).options(selectinload(
# #         Product.category)).order_by(Product.id)

# #     result = await session.execute(stmt)
# #     products = result.scalars().all()
# #     product_dicts = [product.__dict__ for product in products]
# #     return product_dicts


# # BOT_TOKEN = '6141111072:AAH8CBhf7iQUVNFCjR_STaBf9h_mYHSggvo'


# # c_str = "WebAppData"


# # def is_valid_data(init_data_hash: str, init_data: str) -> bool:
# #     init_data = unquote(init_data)
# #     init_data = sorted([chunk.split("=")
# #                         for chunk in unquote(init_data).split("&")
# #                         if chunk[:len("hash=")] != "hash="],
# #                        key=lambda x: x[0])
# #     init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])
# #     print(unquote(init_data))
# #     print(init_data)

# #     secret_key = hmac.new(c_str.encode(), BOT_TOKEN.encode(),
# #                           hashlib.sha256).digest()
# #     data_check = hmac.new(secret_key, init_data.encode(),
# #                           hashlib.sha256)
# #     print(data_check.hexdigest())
# #     print(init_data_hash)
# #     return data_check.hexdigest() == init_data_hash


# # # b0c8bb03576e9ecf85171fe151bee2f996dec619353ce4a2bce72d6337f24678
# # # query_id%3DAAGVbSskAAAAAJVtKyQX6XyE&user%3D%257B%2522id%2522%253A606825877%252C%2522first_name%2522%253A%2522%25D0%2594%25D0%25BC%25D0%25B8%25D1%2582%25D1%2580%25D0%25B8%25D0%25B9%2522%252C%2522last_name%2522%253A%2522%25D0%25A1%25D0%25B2%25D0%25B0%25D1%2580%25D0%25BE%25D0%25B2%25D1%2581%25D0%25BA%25D0%25B8%25D0%25B9%2522%252C%2522username%2522%253A%2522swarovskidima%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522is_premium%2522%253Atrue%252C%2522allows_write_to_pm%2522%253Atrue%257D&auth_date%3D1696961678&hash%3Db0c8bb03576e9ecf85171fe151bee2f996dec619353ce4a2bce72d6337f24678


# # @router.post("/validate_data/")
# # async def validate_data(init_data_hash: str, data_check_string: str):
# #     if is_valid_data(init_data_hash, data_check_string):
# #         expiration_time = datetime.utcnow() + timedelta(hours=2)
# #         payload = {"user_id": 123, "exp": expiration_time}
# #         jwt_token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')
# #         return {"access_token": jwt_token}
# #     else:
# #         raise HTTPException(status_code=400, detail="Data is not valid")


# # # Функция для извлечения JWT-токена из заголовка запроса
# # def get_token(authorization: str = Header(None)):
# #     print(1, '', authorization)
# #     if not authorization:
# #         raise HTTPException(
# #             status_code=401, detail="Authorization header is missing")
# #     token_type, token = authorization.split(" ")
# #     print(2, '', token)
# #     print(3, '', token_type)
# #     if token_type != "Bearer":
# #         raise HTTPException(status_code=401, detail="Invalid token type")
# #     return token


# # def verify_token(token: str = Depends(get_token)):
# #     print(token)
# #     try:
# #         decoded_payload = jwt.decode(
# #             token, 'your-secret-key', algorithms=['HS256'])
# #         # Здесь вы можете проверить, что токен действителен и содержит нужную информацию о пользователе
# #         return decoded_payload
# #     except jwt.ExpiredSignatureError:
# #         raise HTTPException(status_code=401, detail="Token has expired")
# #     except jwt.InvalidTokenError:
# #         raise HTTPException(status_code=401, detail="Invalid token")


# # @router.post("/validate_data/")
# # async def validate_data(init_data_hash: str, data_check_string: str):
# #     if is_valid_data(init_data_hash, data_check_string):
# #         return {"message": "Data is from Telegram"}
# #     else:
# #         raise HTTPException(status_code=400, detail="Data is not valid")


# # @router.get("/products/{shop_id}/")
# # async def get_all_products(shop_id: int, session: AsyncSession = Depends(get_async_session)) -> List[ProductList]:
# #     query = select(Product).where(Product.shop_id ==
# #                                   shop_id).where(Product.availability == True)
# #     result = await session.execute(query)
# #     return result.scalars().all()
