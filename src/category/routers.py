from .crud import get_all_categories
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete, update
from .models import Category
from .schemas import CategoryModel, CategoryCreate, CategoryUpdate, CategoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List, Annotated
from src.secure import apikey_scheme
from typing import List


router = APIRouter(
    prefix="/api/v1/category",
    tags=["Category"])


# @router.post("/your_endpoint")
# async def process_data(data: CategoryBase = Form(...)):
#     # Теперь вы можете использовать данные в объекте 'data'
#     name_rus = data.name_rus
#     name_en = data.name_en
#     availability = data.availability
#     shop_id = data.shop_id

#     # Ваш код обработки данных здесь

#     return {"name_rus": name_rus, "name_en": name_en, "availability": availability, "shop_id": shop_id}


# @router.get("/categories/{shop_id}/")
# async def get_all_categories(shop_id: int, session: AsyncSession = Depends(get_async_session)) -> List[CategoryModel]:
#     query = select(Category).where(Category.shop_id ==
#                                    shop_id).order_by(Category.id.desc())
#     result = await session.execute(query)
#     return result.scalars().all()

@router.get('/test', response_model=list[CategoryBase])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    return await get_all_categories(session=session)


@router.get("/", response_model=list[CategoryBase])
async def get_alcategories(session: AsyncSession = Depends(get_async_session)):
    try:
        categories = await get_all_categories(session)
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")

# @router.get("/", response_model=list[CategoryBase])
# async def get_all_categories(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
#     try:
#         categories = await get_categories(session, skip=skip, limit=limit)
#         return categories

    # query = select(Category).order_by(Category.id.desc())
    # print(query)
    # result = await session.execute(query)
    # print(type(result))
    # print(result)
    # for row in result:
    #     print(row)
    # # list_of_dicts = [dict(row) for row in result]
    # # return list_of_dicts

    # result = await session.execute(query)
    # categories = result.scalars().all()
    # category_dicts = [category.__dict__ for category in categories]
    # return category_dicts
    # except Exception as e:
    #     await session.rollback()
    #     raise HTTPException(
    #         status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/")
async def create_new_category(new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Category).values(**new_category.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": 200, 'date': new_category}


@router.put("/")
async def update_category(category_id: int, new_date: CategoryUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Category).where(
        Category.id == category_id).values(**new_date.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/")
async def delete_category(category_id: int, session: Session = Depends(get_async_session)):
    try:
        stmt = delete(Category).where(Category.id == category_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{category_id}/checkbox/")
async def update_product_field(category_id: int, checkbox: str, session: AsyncSession = Depends(get_async_session)):
    product = await session.get(Category, category_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    if not hasattr(product, checkbox):
        raise HTTPException(status_code=400, detail="Поле не существует")
    setattr(product, checkbox, not getattr(product, checkbox))
    await session.commit()
    return {"status": "success"}


# @router.get("/categories/{shop_id}/{category_id}")
# async def get_one_category(shop_id: int, category_id: int, session: AsyncSession = Depends(get_async_session)) -> List[CategoryModel]:
#     query = select(Category).where(Category.shop_id ==
#                                    shop_id).where(Category.id == category_id)
#     result = await session.execute(query)
#     return result.scalars().all()


# @router.post("/categories/")
# async def create_new_category(access_token: Annotated[str, Depends(apikey_scheme)], new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(Category).values(**new_category.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}


# @router.put("/categories/")
# async def update_category(access_token: Annotated[str, Depends(apikey_scheme)], category_id: int, new_date: CategoryUpdate, session: AsyncSession = Depends(get_async_session)):
#     stmt = update(Category).where(
#         Category.id == category_id).values(**new_date.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}


# @router.delete("/categories/")
# async def delete_category(access_token: Annotated[str, Depends(apikey_scheme)], category_id: int, shop_id: int, session: Session = Depends(get_async_session)):
#     try:
#         await session.execute(Category.__table__.delete().where(Category.shop_id == shop_id).where(Category.id == category_id))
#         await session.commit()
#         return {"status": "success", "message": f"Категория, c id {category_id}, успешно удалена."}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")
