import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete, text
from src.api_admin.models import User, Product, Category, Subcategory, Unit
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session, metadata
from typing import List, Annotated
from src.secure import apikey_scheme
from fastapi.encoders import jsonable_encoder
from src.secure import pwd_context
from .db_schema import *
from src.database import Base
from .crud import *
from .controller import check_duplication, create_new_schema_and_table, create_new_unit


router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"])


@router.get("/", status_code=201)
async def get_all_users_list(session: AsyncSession = Depends(get_async_session)) -> List[UserList]:
    users = await crud_get_all_users(session)
    return users


@router.post("/register/", status_code=201)
async def register_new_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    await check_duplication(user_data=user_data, session=session)
    create_user = await crud_register_new_user(user_data=user_data, session=session)
    await create_new_schema_and_table(user_data=user_data, session=session)
    await create_new_unit(schema=user_data.username, session=session)
    return create_user


@router.put("/", summary="Обновление информации о пользователе, кроме пароля")
async def update_user_data(user_id: int, new_date: UserUpdateData, session: AsyncSession = Depends(get_async_session)):
    pass


@router.put("/update_password/", summary="Обновление пароля")
async def update_user_password(user_id: int, password_data: UserUpdatePassword, session: AsyncSession = Depends(get_async_session)):
    pass


@router.delete("/", summary="Удаление пользователя, без возможности восстановить")
async def delete_user(user_id: int, session: Session = Depends(get_async_session)):
    pass


@router.get("/roles/", status_code=201)
async def get_all_roles_list(session: AsyncSession = Depends(get_async_session)) -> List[RolesList]:
    roles = await crud_get_all_roles(session)
    return roles


@router.post("/roles/", status_code=201)
async def create_new_role(date: RolesCreate, session: AsyncSession = Depends(get_async_session)):
    new_roles = await crud_create_new_role(date=date, session=session)
    return new_roles


@router.put("/roles/")
async def update_role(role_id: int, new_data: RolesUpdate, session: AsyncSession = Depends(get_async_session)):
    update_role = await crud_update_role(role_id=role_id, new_data=new_data, session=session)
    return update_role


@router.delete("/roles/")
async def deleted_role(role_id: int, session: AsyncSession = Depends(get_async_session)):
    deleted_role = await crud_deleted_role(role_id=role_id, session=session)
    return deleted_role

# @router.put("/data/", summary="Обновление информации о пользователе, кроме пароля")
# async def update_user_data(user_id: int, new_date: UserUpdateData, session: AsyncSession = Depends(get_async_session)):
#     """
#     Обновление информации о пользователе, кроме пароля.

#     Этот маршрут позволяет обновить информацию о пользователе, за исключением пароля.

#     Параметры:
#     - `user_id`: идентификатор пользователя.
#     - `new_date`: данные для обновления информации о пользователе.

#     Возвращает:
#     - Сообщение о успешном обновлении.
#     """
#     stmt = update(UserData).where(
#         UserData.user_id == user_id).values(**new_date.dict())
#     await session.execute(stmt)
#     stmt_updated_at = select(User).where(User.id == user_id)
#     result = await session.execute(stmt_updated_at)
#     user = result.scalars().all()
#     user[0].updated_at = datetime.now()

#     await session.commit()
#     return {"status": "success"}


# @router.put("/update_password/", summary="Обновление пароля")
# async def update_user_password(user_id: int, password_data: UserUpdatePassword, session: AsyncSession = Depends(get_async_session)):
#     """
#     Обновление пароля пользователя.

#     Этот маршрут позволяет обновить пароль пользователя.

#     Параметры:
#     - `user_id`: идентификатор пользователя.
#     - `password_data`: данные для обновления пароля.

#     Возвращает:
#     - Сообщение о успешном обновлении пароля или ошибку, если старый пароль введен неверно или новый пароль совпадает с текущим.
#     """
#     user = await session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="Пользователь не найден")

#     query = select(UserData).where(UserData.user_id == user_id)
#     user_data = await session.execute(query)
#     user_data = user_data.scalar()

#     if not user_data:
#         raise HTTPException(
#             status_code=404, detail="Данные пользователя не найдены")

#     if not pwd_context.verify(password_data.old_password, user_data.hashed_password):
#         raise HTTPException(
#             status_code=400, detail="Старый пароль введен неверно")

#     if pwd_context.verify(password_data.hashed_password, user_data.hashed_password):
#         raise HTTPException(
#             status_code=400, detail="Новый пароль совпадает с текущим паролем")

#     user_data.hashed_password = pwd_context.hash(password_data.hashed_password)
#     await session.commit()

#     return {"status": "success", "message": "Пароль пользователя успешно обновлен"}


# @router.delete("/", summary="Удаление пользователя, без возможности восстановить")
# async def delete_user(user_id: int, session: Session = Depends(get_async_session)):
#     """
#     Удаление пользователя.

#     Этот маршрут предназначен для удаления существующих пользователей по идентификатору.

#     Параметры:

#     - `user_id`: Идентификатор пользователя, которого необходимо удалить.

#     Возвращает:

#     - Сообщение об успешном выполнении операции или сообщение об ошибке в случае возникновения проблем.

#     # P.s. Удаление пользователя невозможно, если у пользователя есть хотя бы один магазин.

#     # P.s.s. Для выполнения функции временного удаления используйте эндпоинт с изменением флага "deleted_flag"


#     """
#     try:
#         stmt = delete(UserData).where(UserData.user_id == user_id)
#         await session.execute(stmt)

#         stmt = delete(User).where(User.id == user_id)
#         await session.execute(stmt)

#         await session.commit()
#         return {"status": "success", "message": f"Пользователь, c id {user_id}, успешно удалена."}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(
#             status_code=500, detail=f"An error occurred: {str(e)}")
