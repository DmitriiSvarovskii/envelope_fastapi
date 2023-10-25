# from alembic import command
# from alembic.config import Config
# from src.admin_apps.product.models import Product
# from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy.orm import joinedload
# from .crud import get_all_categories
# from fastapi import APIRouter, Depends, HTTPException, Form
# from sqlalchemy.exc import IntegrityError

# from sqlalchemy.orm import Session
# from sqlalchemy import insert, select, delete, update
# from .models import Category
# from .schemas import CategoryModel, CategoryCreate, CategoryDeleted, CategoryUpdate, CategoryBase
# from sqlalchemy.ext.asyncio import AsyncSession
# from ..database import get_async_session
# from typing import List, Annotated
# from src.secure import apikey_scheme
# from typing import List
# # from src.product.models import on_category_availability_set


# router = APIRouter(
#     prefix="/api/v1/category",
#     tags=["Category"])


# @router.get("/", response_model=list[CategoryBase], status_code=200)
# async def get_alcategories(session: AsyncSession = Depends(get_async_session)):
#     try:
#         categories = await get_all_categories(session)
#         return categories
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.post("/", status_code=201)
# async def create_new_category(new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
#     try:
#         stmt = insert(Category).values(**new_category.dict())
#         await session.execute(stmt)
#         await session.commit()
#         return {"status": 201, 'date': new_category}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/", status_code=200)
# async def update_category(category_id: int, new_date: CategoryUpdate, session: AsyncSession = Depends(get_async_session)):
#     try:
#         stmt = update(Category).where(
#             Category.id == category_id).values(**new_date.dict())
#         await session.execute(stmt)
#         await session.commit()
#         return {"status": "success"}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/deleted/", response_model=CategoryDeleted)
# async def update_delete_flag_category(category_id: int, deleted_flag: bool, session: AsyncSession = Depends(get_async_session)):
#     category = await session.get(Category, category_id)
#     if category is None:
#         raise HTTPException(status_code=404, detail="Категория не найдена")
#     if not hasattr(category, deleted_flag):
#         raise HTTPException(status_code=400, detail="Поле не существует")
#     setattr(category, deleted_flag, not getattr(category, deleted_flag))
#     await session.commit()
#     return {"status": "success"}

# # @router.put("/deleted/", status_code=204)
# # async def delete_category(category_id: int, session: Session = Depends(get_async_session)):
# #     try:
# #         stmt = delete(Category).where(Category.id == category_id)
# #         await session.execute(stmt)
# #         await session.commit()
# #         return {"status": "success"}
# #     except IntegrityError as e:
# #         await session.rollback()
# #         raise HTTPException(
# #             status_code=400,
# #             detail=f"Удаление невозможно, данная категория имеет связь с товарами."
# #             f"Для удаления категори необходимо сначала оборвать связь с товарами"
# #         )
# #     except Exception as e:
# #         await session.rollback()
# #         raise HTTPException(
# #             status_code=500,
# #             detail=f"An error occurred: {str(e)}")


# @router.put("/{category_id}/checkbox/")
# async def update_product_field(category_id: int, checkbox: str, session: AsyncSession = Depends(get_async_session)):
#     category = await session.get(Category, category_id)
#     if category is None:
#         raise HTTPException(status_code=404, detail="Категория не найдена")
#     if not hasattr(category, checkbox):
#         raise HTTPException(status_code=400, detail="Поле не существует")
#     setattr(category, checkbox, not getattr(category, checkbox))
#     new_value = getattr(category, checkbox)

#     query = update(Product).where(Product.category_id ==
#                                   category_id).values(deleted_flag=new_value)
#     await session.execute(query)
#     await session.commit()
#     return {"status": "success"}


# # @router.get("/categories/{shop_id}/{category_id}")
# # async def get_one_category(shop_id: int, category_id: int, session: AsyncSession = Depends(get_async_session)) -> List[CategoryModel]:
# #     query = select(Category).where(Category.shop_id ==
# #                                    shop_id).where(Category.id == category_id)
# #     result = await session.execute(query)
# #     return result.scalars().all()


# # @router.post("/categories/")
# # async def create_new_category(access_token: Annotated[str, Depends(apikey_scheme)], new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
# #     stmt = insert(Category).values(**new_category.dict())
# #     await session.execute(stmt)
# #     await session.commit()
# #     return {"status": "success"}


# # @router.put("/categories/")
# # async def update_category(access_token: Annotated[str, Depends(apikey_scheme)], category_id: int, new_date: CategoryUpdate, session: AsyncSession = Depends(get_async_session)):
# #     stmt = update(Category).where(
# #         Category.id == category_id).values(**new_date.dict())
# #     await session.execute(stmt)
# #     await session.commit()
# #     return {"status": "success"}


# # @router.delete("/categories/")
# # async def delete_category(access_token: Annotated[str, Depends(apikey_scheme)], category_id: int, shop_id: int, session: Session = Depends(get_async_session)):
# #     try:
# #         await session.execute(Category.__table__.delete().where(Category.shop_id == shop_id).where(Category.id == category_id))
# #         await session.commit()
# #         return {"status": "success", "message": f"Категория, c id {category_id}, успешно удалена."}
# #     except Exception as e:
# #         await session.rollback()
# #         raise HTTPException(
# #             status_code=500, detail=f"An error occurred: {str(e)}")
