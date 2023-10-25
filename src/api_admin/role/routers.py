from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from .models import Role
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Annotated
from src.secure import apikey_scheme
from fastapi.encoders import jsonable_encoder
from src.secure import pwd_context
from migrations.alembic import run_alembic_migrations


router = APIRouter(
    prefix="/api/v1/role",
    tags=["Role (for User)"]
)


@router.get("/", summary="Получение списка ролей", response_model=List[RoleBase])
async def get_all_role(session: AsyncSession = Depends(get_async_session)):
    """
    Получение списка ролей.

    Этот маршрут позволяет получить список всех доступных ролей.

    Возвращает:
    - Список ролей.
    """
    query = select(Role).order_by(Role.id)
    result = await session.execute(query)
    roles = result.scalars().all()
    roles_dict = [role.__dict__ for role in roles]
    return roles_dict


@router.post("/", summary="Создание новой роли")
async def create_new_role(new_role: RoleCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Создание новой роли.

    Этот маршрут позволяет создать новую роль.

    Параметры:

    - `new_role`: имя роли, например: User, Admin и тп.

    Возвращает:
    - Сообщение о успешном выполнении операции.

    """
    stmt = insert(Role).values(**new_role.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/", summary="Обновление названия роли")
async def update_role(role_id: int, new_date: RoleUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Обновление роли

    Описание:

    Этот маршрут позволяет обновить существующую роль, указав идентификатор роли и новые данные для обновления.

    Параметры:

    - `role_id`: Идентификатор роли, которую необходимо обновить.

    - `new_date`: Новое название для роли.

    Возвращает:

    - Сообщение о успешном выполнении операции.
    """
    stmt = update(Role).where(
        Role.id == role_id).values(**new_date.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/", summary="Удаление роли")
async def delete_role(role_id: int, session: Session = Depends(get_async_session)):
    """
    Удаление роли.

    Этот маршрут предназначен для удаления существующей роли по её идентификатору.

    Параметры:

    - `role_id`: Идентификатор роли, которую необходимо удалить.

    Возвращает:

    - Сообщение об успешном выполнении операции или сообщение об ошибке в случае возникновения проблем.

    P.s. Удаление роли невозможно, если роль используется хотя бы для одного пользователя.
    """
    try:
        stmt = delete(Role).where(Role.id == role_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": f"Роль, c id {role_id}, успешно удалена."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
