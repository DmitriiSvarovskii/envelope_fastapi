import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Subcategory
from .schemas import (
    SubcategoryCreate,
    SubcategoryList,
    SubcategoryUpdate,
    CategoryUpdate
)
from typing import List


async def crud_get_all_subcategories(
    schema: str,
    session: AsyncSession = Depends(get_async_session)
) -> List[SubcategoryList]:
    query = (
        select(Subcategory).
        where(
            not Subcategory.deleted_flag
        ).
        order_by(Subcategory.id.desc()).
        execution_options(schema_translate_map={None: schema})
    )
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories


async def crud_create_new_subcategory(
    schema: str,
    data: SubcategoryCreate,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> List[SubcategoryCreate]:
    category_data = data.model_dump()
    # Устанавливаем created_by из текущего пользователя
    category_data["created_by"] = user_id
    stmt = (
        insert(Subcategory).
        values(**data.model_dump(), created_by=user_id).
        execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'date': data}


async def crud_update_subcategory(
    schema: str,
    user_id: int,
    subcategory_id: int,
    data: SubcategoryUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> List[CategoryUpdate]:
    stmt = (
        update(Subcategory).
        where(Subcategory.id == subcategory_id).
        values(**data.model_dump(), updated_by=user_id).
        execution_options(
            schema_translate_map={None: schema}
        )
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", 'date': data}


async def crud_change_delete_flag_subcategory(
    schema: str,
    user_id: int,
    subcategory_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        update(Subcategory).
        where(Subcategory.id == subcategory_id).
        values(
            deleted_flag=~Subcategory.deleted_flag,
            deleted_at=datetime.now(),
            deleted_by=user_id).
        execution_options(
            schema_translate_map={None: schema})
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "message": "Статус для deleted_flag изменен"
    }


async def crud_update_subcategory_field(
    schema: str,
    subcategory_id: int,
    user_id: int,
    checkbox: str,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        update(Subcategory).
        where(Subcategory.id == subcategory_id).
        values(
            availability=~Subcategory.availability,
            updated_at=datetime.now(),
            updated_by=user_id).
        execution_options(
            schema_translate_map={None: schema}
        )
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": f"Статус для {checkbox} изменен"}


async def crud_delete_subcategory(
    schema: str,
    subcategory_id: int,
    session: Session = Depends(get_async_session)
):
    try:
        stmt = (
            delete(Subcategory).
            where(Subcategory.id == subcategory_id).
            execution_options(
                schema_translate_map={None: schema}
            )
        )
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "message": f"Субкатегория, c id {subcategory_id}, успешно удалена."
        }
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=(
                "Удаление этой субкатегории невозможно, "
                "так как на нее ссылаются продукты."
            )
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
