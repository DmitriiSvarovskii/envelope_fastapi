from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_async_session

from .crud import *
from .schemas import StoreCreate
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/store",
    tags=["Store (admin)"])


@router.get("/", response_model=List[StoreList], status_code=200)
async def get_all_store(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        categories = await crud_get_all_stores(schema=str(current_user.id), session=session)
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/one/", response_model=Optional[StoreTgGroup], status_code=200)
async def get_one_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        store = await crud_get_one_stores(store_id=store_id, schema=str(current_user.id), session=session)
        return store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# @router.post("/", status_code=201)
# async def create_new_store(data: StoreCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     try:
#         new_store = await crud_create_new_store(schema=str(current_user.id), data=data, user_id=current_user.id, session=session)
#         return new_store
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", status_code=201)
async def create_new_store(data: StoreCreate, token_bot: BotTokenCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_store = await crud_create_new_store_and_bot(schema=str(current_user.id), data=data, token_bot=token_bot, user_id=current_user.id, session=session)
        return new_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/", status_code=200)
async def update_store(store_id: int, data: StoreUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_store = await crud_update_store(schema=str(current_user.id), store_id=store_id, data=data, user_id=current_user.id, session=session)
        return up_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/delete/")
async def change_delete_flag_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_store = await crud_change_delete_flag_store(schema=str(current_user.id), user_id=current_user.id, store_id=store_id, session=session)
        return change_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


# @router.put("/checkbox/",)
# async def update_store_field(store_id: int, checkbox: str, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
#     """
#     Параметры:

#     - `store_id`: идентификатор категории.
#     - `checkbox`: имя поля, которое требуется изменить. Для категории доступно только: `availability`.
#    """
#     try:
#         change_store = await crud_update_store_field(schema=str(current_user.id), user_id=current_user.id, store_id=store_id, checkbox=checkbox, session=session)
#         return change_store
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/")
async def delete_store(store_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_store = await crud_delete_store(schema=str(current_user.id), store_id=store_id, session=session)
        return change_store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
