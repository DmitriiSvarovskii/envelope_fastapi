from fastapi import Depends
from sqlalchemy import insert, select, update, delete
from .models import Role
from .schemas import RolesCreate, RolesList, RolesUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List


async def crud_get_all_roles(
    session: AsyncSession = Depends(get_async_session)
) -> List[RolesList]:
    query = select(Role).order_by(Role.id.desc())
    result = await session.execute(query)
    roles = result.scalars().all()
    return roles


async def crud_create_new_role(
    date: RolesCreate,
    session: AsyncSession = Depends(get_async_session)
) -> List[RolesCreate]:
    stmt = insert(Role).values(date.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'date': date}


async def crud_update_role(
    role_id: int,
    new_data: RolesCreate,
    session: AsyncSession = Depends(get_async_session)
) -> List[RolesUpdate]:
    stmt = update(Role).where(Role.id == role_id).values(new_data.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": 201, 'new_data': new_data}


async def crud_deleted_role(
    role_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(Role).where(Role.id == role_id)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": 201,
        'message': f"Роль, c id {role_id}, успешно удалена."
    }
