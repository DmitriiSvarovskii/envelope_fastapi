from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Product
from .schemas import *
from .crud import *
from ..user import User
from .controller import s3
from ..auth.routers import get_current_user_from_token
from src.config import BUCKET_NAME, ENDPOINT_URL
from PIL import Image
import io
import os

router = APIRouter(
    prefix="/api/v1/product",
    tags=["Product (admin)"])


@router.get("/", response_model=List[ProductList])
async def get_all_product(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    query = select(Product).options(selectinload(Product.category)).options(selectinload(Product.unit)).where(Product.deleted_flag != True).where(Product.store_id == store_id).order_by(
        Product.id).execution_options(schema_translate_map={None: str(current_user.id)})
    result = await session.execute(query)
    products = result.scalars().all()
    # return products
    product_dicts = [
        {
            "id": product.id,
            "category_id": product.category.id,
            "category_name": product.category.name,
            # "subcategory_id": product.subcategory.id,
            # "store_id":product.store.id,
            "name": product.name,
            "description": product.description,
            "image": product.image,
            "price": product.price,
            "wt": product.wt,
            "unit_id": product.unit.id,
            "kilocalories": product.kilocalories,
            "proteins": product.proteins,
            "fats": product.fats,
            "carbohydrates": product.carbohydrates,
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
async def create_new_product(store_id: int, data: ProductCreate, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_product = await crud_create_new_product(schema=str(current_user.id), store_id=store_id, user_id=current_user.id, data=data, session=session)
        return new_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# @router.post("/upload_photo/")
# async def upload_photo(file: UploadFile, store_id: int, current_user: User = Depends(get_current_user_from_token)):
#     current_datetime = datetime.now()
#     current_date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
#     object_key = f"{current_user.id}/{store_id}/{current_date_str}_{file.filename}"
#     s3.upload_fileobj(file.file, BUCKET_NAME, object_key)
#     object_url = f'{ENDPOINT_URL}/{BUCKET_NAME}/{object_key}'
#     return object_url
@router.post("/upload_photo/")
async def process_and_upload_photo(file: UploadFile, store_id: int, current_user: User = Depends(get_current_user_from_token)):
    try:
        image = Image.open(io.BytesIO(await file.read()))

        image.thumbnail((900, 900))

        with io.BytesIO() as output_buffer:
            image.save(output_buffer, format="WebP")
            output_buffer.seek(0)
            webp_image = Image.open(output_buffer)

        current_datetime = datetime.now()
        current_date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        object_key = f"{current_user.id}/{store_id}/{current_date_str}_{file.filename}"

        with io.BytesIO() as webp_output_buffer:
            webp_image.save(webp_output_buffer, format="WebP")
            webp_output_buffer.seek(0)
            s3.upload_fileobj(webp_output_buffer, BUCKET_NAME, object_key)

        object_url = f'{ENDPOINT_URL}/{BUCKET_NAME}/{object_key}'

        return object_url
    except Exception as e:
        return f"Error processing and uploading photo: {str(e)}"


@router.delete("/delete_photo/")
async def delete_photo(photo_name: str, store_id: int, current_user: User = Depends(get_current_user_from_token)):
    try:
        object_key = f"{current_user.id}/{store_id}/{photo_name}"
        s3.delete_object(Bucket=BUCKET_NAME, Key=object_key)
        return f'File {photo_name} successfully deleted'
    except Exception as e:
        return f'Error deleting file {photo_name}: {str(e)}'


@router.put("/", status_code=200)
async def update_product(product_id: int, data: ProductUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_product = await crud_update_product(schema=str(current_user.id), product_id=product_id, data=data, user_id=current_user.id, session=session)
        return up_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/checkbox/",)
async def update_product_field(product_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    # Параметры:
    #     - `product_id`: идентификатор продукта.
    #     - `checkbox`: имя поля, которое требуется изменить.
    #     Для продуктов доступны следующие значения: `availability`, `popular`
    """
    try:
        change_product = await crud_update_product_field(schema=str(current_user.id), user_id=current_user.id, product_id=product_id, checkbox=checkbox, session=session)
        return change_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/delete/")
async def change_delete_flag_product(product_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_product = await crud_change_delete_flag_product(schema=str(current_user.id), user_id=current_user.id, product_id=product_id, session=session)
        return change_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/")
async def delete_product(product_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_product = await crud_delete_product(schema=str(current_user.id), product_id=product_id, session=session)
        return change_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


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


# @router.get("/unit", response_model=List[UnitList], status_code=200)
# async def get_all_unit(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         categories = await crud_get_all_units(schema=str(current_user.id), session=session)
#         return categories
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.post("/unit", status_code=201)
# async def create_new_unit(data: UnitCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         new_unit = await crud_create_new_unit(schema=str(current_user.id), data=data, user_id=current_user.id, session=session)
#         return new_unit
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/unit", status_code=200)
# async def update_unit(unit_id: int, data: UnitUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         up_unit = await crud_update_unit(schema=str(current_user.id), unit_id=unit_id, data=data, user_id=current_user.id, session=session)
#         return up_unit
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.delete("/unit")
# async def delete_unit(unit_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         change_unit = await crud_delete_unit(schema=str(current_user.id), unit_id=unit_id, session=session)
#         return change_unit
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")
