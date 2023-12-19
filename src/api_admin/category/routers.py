from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_async_session

from .crud import *
from .schemas import CategoryCreate, CategoryUpdate
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/category",
    tags=["Category (admin)"])


@router.get("/", response_model=List[CategoryList], status_code=200)
async def get_all_category(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token
    """
    try:
        categories = await crud_get_all_categories(schema=str(current_user.id), store_id=store_id, session=session)
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", status_code=201)
async def create_new_category(store_id: int, data: CategoryCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token
    """
    try:
        new_category = await crud_create_new_category(schema=current_user.store_id, store_id=store_id,  data=data, user_id=current_user.id, session=session)
        return new_category
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/", status_code=200)
async def update_category(category_id: int, data: CategoryUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token
    """
    try:
        up_category = await crud_update_category(schema=str(current_user.id), category_id=category_id, data=data, user_id=current_user.id, session=session)
        return up_category
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/delete/")
async def change_delete_flag_category(category_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token
    """
    try:
        change_category = await crud_change_delete_flag_category(schema=str(current_user.id), user_id=current_user.id, category_id=category_id, session=session)
        return change_category
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/checkbox/",)
async def update_category_field(category_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token;

    - `checkbox`: имя поля, которое требуется изменить. Для категории доступно только: `availability`.
   """
    try:
        change_category = await crud_update_category_field(schema=str(current_user.id), user_id=current_user.id, category_id=category_id, checkbox=checkbox, session=session)
        return change_category
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/")
async def delete_category(category_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    """
    Ожидается jwt-token
    """
    try:
        change_category = await crud_delete_category(schema=str(current_user.id), category_id=category_id, session=session)
        return change_category
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# @router.get("/subcategory", response_model=List[SubcategoryList], status_code=200)
# async def get_all_subcategory(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         categories = await crud_get_all_subcategories(schema=str(current_user.id), store_id=store_id, session=session)
#         return categories
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.post("/subcategory", status_code=201)
# async def create_new_subcategory(data: SubcategoryCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         new_subcategory = await crud_create_new_subcategory(schema=str(current_user.id), data=data, user_id=current_user.id, session=session)
#         return new_subcategory
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/subcategory", status_code=200)
# async def update_subcategory(subcategory_id: int, data: SubcategoryUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         up_subcategory = await crud_update_subcategory(schema=str(current_user.id), subcategory_id=subcategory_id, data=data, user_id=current_user.id, session=session)
#         return up_subcategory
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/delete/subcategory")
# async def change_delete_flag_subcategory(subcategory_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         change_subcategory = await crud_change_delete_flag_subcategory(schema=str(current_user.id), user_id=current_user.id, subcategory_id=subcategory_id, session=session)
#         return change_subcategory
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/{subcategory_id}/checkbox/", summary="Изменение поля категории")
# async def update_subcategory_field(subcategory_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     """
#     Параметры:

#     - `subcategory_id`: идентификатор категории.
#     - `checkbox`: имя поля, которое требуется изменить. Для категории доступно только: `availability`.
#    """
#     try:
#         change_subcategory = await crud_update_subcategory_field(schema=str(current_user.id), user_id=current_user.id, subcategory_id=subcategory_id, checkbox=checkbox, session=session)
#         return change_subcategory
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


# @router.delete("/subcategory")
# async def delete_subcategory(subcategory_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         change_subcategory = await crud_delete_subcategory(schema=str(current_user.id), subcategory_id=subcategory_id, session=session)
#         return change_subcategory
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")
