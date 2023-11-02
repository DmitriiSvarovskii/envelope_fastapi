from sqlalchemy.orm import Session
from .schemas import *
from src.api_admin.models import Category, Subcategory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from sqlalchemy.engine import Result
from json import dumps
from dataclasses import asdict
from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi import APIRouter, Depends
from ..user import User
from ..auth.routers import get_current_user_from_token


async def crud_get_all_categories(schema: str, session: AsyncSession = Depends(get_async_session)) -> List[CategoryList]:
    query = select(Category).where(
        Category.deleted_flag != True).order_by(Category.id.desc()).execution_options(schema_translate_map={None: schema})
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories


async def crud_create_new_category(schema: str, data: CategoryCreate, user_id: int, session: AsyncSession = Depends(get_async_session)) -> List[CategoryCreate]:
    category_data = data.dict()
    # Устанавливаем created_by из текущего пользователя
    category_data["created_by"] = user_id
    stmt = insert(Category).values(**data.dict()
                                   ).execution_options(schema_translate_map={None: schema})
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'date': data}
