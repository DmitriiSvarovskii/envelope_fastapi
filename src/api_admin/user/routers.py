import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from .models import *
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Annotated
from src.secure import apikey_scheme
from .controller import register
from fastapi.encoders import jsonable_encoder
from src.secure import pwd_context
from migrations.alembic import run_alembic_migrations


router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"])


@router.get("/", summary="Получение списка пользователей", status_code=201)
async def get_all_users(session: AsyncSession = Depends(get_async_session)) -> List[UserList]:
    """
    Получение списка пользователей.

    Этот маршрут позволяет получить список всех пользователей.

    Возвращает:
    - Список пользователей.
    """
    query = select(UserData).order_by(UserData.id.desc())
    result = await session.execute(query)
    users = result.scalars().all()
    user_dicts = [user.__dict__ for user in users]
    return user_dicts


@router.post("/", summary="Регистрация нового пользователя")
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Регистрация нового пользователя.

    Этот маршрут позволяет зарегистрировать нового пользователя.

    Параметры:
    - `user_data`: данные для регистрации нового пользователя.

    Возвращает:
    - Сообщение о успешной регистрации или ошибку, если пользователь с таким именем пользователя уже существует.
    """
    query = select(UserData).where(UserData.username == user_data.username)
    result = await session.execute(query)
    existing_user_data = result.scalar()
    if existing_user_data:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем пользователя уже существует!"
        )
    new_user = User(is_active=True)
    session.add(new_user)
    await session.commit()
    new_user_data = UserData(
        username=user_data.username,
        hashed_password=pwd_context.hash(user_data.hashed_password),
        user_id=new_user.id
    )
    session.add(new_user_data)
    await session.commit()
    return jsonable_encoder({
        "username": new_user_data.username,
    })


@router.put("/data/", summary="Обновление информации о пользователе, кроме пароля")
async def update_user_data(user_id: int, new_date: UserUpdateData, session: AsyncSession = Depends(get_async_session)):
    """
    Обновление информации о пользователе, кроме пароля.

    Этот маршрут позволяет обновить информацию о пользователе, за исключением пароля.

    Параметры:
    - `user_id`: идентификатор пользователя.
    - `new_date`: данные для обновления информации о пользователе.

    Возвращает:
    - Сообщение о успешном обновлении.
    """
    stmt = update(UserData).where(
        UserData.user_id == user_id).values(**new_date.dict())
    await session.execute(stmt)
    stmt_updated_at = select(User).where(User.id == user_id)
    result = await session.execute(stmt_updated_at)
    user = result.scalars().all()
    user[0].updated_at = datetime.now()
    await session.commit()
    return {"status": "success"}


@router.put("/update_password/", summary="Обновление пароля")
async def update_user_password(user_id: int, password_data: UserUpdatePassword, session: AsyncSession = Depends(get_async_session)):
    """
    Обновление пароля пользователя.

    Этот маршрут позволяет обновить пароль пользователя.

    Параметры:
    - `user_id`: идентификатор пользователя.
    - `password_data`: данные для обновления пароля.

    Возвращает:
    - Сообщение о успешном обновлении пароля или ошибку, если старый пароль введен неверно или новый пароль совпадает с текущим.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    query = select(UserData).where(UserData.user_id == user_id)
    user_data = await session.execute(query)
    user_data = user_data.scalar()

    if not user_data:
        raise HTTPException(
            status_code=404, detail="Данные пользователя не найдены")

    if not pwd_context.verify(password_data.old_password, user_data.hashed_password):
        raise HTTPException(
            status_code=400, detail="Старый пароль введен неверно")

    if pwd_context.verify(password_data.hashed_password, user_data.hashed_password):
        raise HTTPException(
            status_code=400, detail="Новый пароль совпадает с текущим паролем")

    user_data.hashed_password = pwd_context.hash(password_data.hashed_password)
    await session.commit()

    return {"status": "success", "message": "Пароль пользователя успешно обновлен"}


@router.delete("/", summary="Удаление пользователя, без возможности восстановить")
async def delete_user(user_id: int, session: Session = Depends(get_async_session)):
    """
    Удаление пользователя.

    Этот маршрут предназначен для удаления существующих пользователей по идентификатору.

    Параметры:

    - `user_id`: Идентификатор пользователя, которого необходимо удалить.

    Возвращает:

    - Сообщение об успешном выполнении операции или сообщение об ошибке в случае возникновения проблем.

    # P.s. Удаление пользователя невозможно, если у пользователя есть хотя бы один магазин.

    # P.s.s. Для выполнения функции временного удаления используйте эндпоинт с изменением флага "deleted_flag"


    """
    try:
        stmt = delete(UserData).where(UserData.user_id == user_id)
        await session.execute(stmt)

        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)

        await session.commit()
        return {"status": "success", "message": f"Пользователь, c id {user_id}, успешно удалена."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
