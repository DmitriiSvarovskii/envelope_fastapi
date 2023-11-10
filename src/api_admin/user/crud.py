from sqlalchemy.schema import CreateSchema, CreateTable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete, text
from src.api_admin.models import User, Product, Category, Subcategory, Unit
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Annotated
from src.secure import pwd_context


async def crud_get_all_users(session: AsyncSession = Depends(get_async_session)) -> List[UserList]:
    query = select(User).order_by(User.id.desc())
    result = await session.execute(query)
    users = result.scalars().all()
    return users


async def crud_register_new_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(User).values([{'username': user_data.username,
                                 'hashed_password': pwd_context.hash(user_data.hashed_password)}]
                               ).execution_options(schema_translate_map={None: 'public'}).returning(User.username, User.id)
    result = await session.execute(stmt)
    created_user = result.fetchone()
    await session.commit()
    return {'username': created_user[0], 'user_id': created_user[1]}
    # return users

    # await session.commit()
    # return {"status_code": 201,
    #         "username": user_data.username,
    #         "schema_name": user_data.username,
    #         }


# async def crud_get_all_roles(session: AsyncSession = Depends(get_async_session)) -> List[RolesList]:
#     query = select(Role).order_by(Role.id.desc())
#     result = await session.execute(query)
#     roles = result.scalars().all()
#     return roles


# async def crud_create_new_role(date: RolesCreate, session: AsyncSession = Depends(get_async_session)) -> List[RolesCreate]:
#     stmt = insert(Role).values(date.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": 201, 'date': date}


# async def crud_update_role(role_id: int, new_data: RolesCreate, session: AsyncSession = Depends(get_async_session)) -> List[RolesUpdate]:
#     stmt = update(Role).where(Role.id == role_id).values(new_data.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": 201, 'new_data': new_data}


# async def crud_deleted_role(role_id: int, session: AsyncSession = Depends(get_async_session)):
#     stmt = delete(Role).where(Role.id == role_id)
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": 201, 'message': f"Роль, c id {role_id}, успешно удалена."}
