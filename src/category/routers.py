from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from .models import Category
from .schemas import CategoryModel, CategoryCreate, CategoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List


router = APIRouter(
    prefix="/menu",
    tags=["Menu. Category"])


@router.get("/categories/{shop_id}/")
async def get_all_categories(shop_id: int, session: AsyncSession = Depends(get_async_session)) -> List[CategoryModel]:
    query = select(Category).where(Category.shop_id ==
                                   shop_id).order_by(Category.id.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/categories/{shop_id}/{category_id}")
async def get_one_category(shop_id: int, category_id: int, session: AsyncSession = Depends(get_async_session)) -> List[CategoryModel]:
    query = select(Category).where(Category.shop_id ==
                                   shop_id).where(Category.id == category_id)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/categories/")
async def create_new_category(new_category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Category).values(**new_category.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/categories/")
async def update_category(category_id: int, new_date: CategoryUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Category).where(
        Category.id == category_id).values(**new_date.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/categories/")
async def delete_category(category_id: int, shop_id: int, session: Session = Depends(get_async_session)):
    try:
        await session.execute(Category.__table__.delete().where(Category.shop_id == shop_id).where(Category.id == category_id))
        await session.commit()
        return {"status": "success", "message": f"Категория, c id {category_id}, успешно удалена."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
