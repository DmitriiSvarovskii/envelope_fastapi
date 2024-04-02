from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from ..auth.routers import get_current_user_from_token
from ..user.models import User
from .schemas import RolesList, RolesUpdate, RolesCreate
from .crud import (
    crud_get_all_roles, crud_create_new_role,
    crud_update_role, crud_deleted_role
)


router = APIRouter(
    prefix="/api/v1/role",
    tags=["Role (admin)"])


@router.get("/", status_code=201)
async def get_all_roles_list(
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
) -> List[RolesList]:
    roles = await crud_get_all_roles(session)
    return roles


@router.post("/", status_code=201)
async def create_new_role(
    date: RolesCreate,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    new_roles = await crud_create_new_role(date=date, session=session)
    return new_roles


@router.put("/")
async def update_role(
    role_id: int,
    new_data: RolesUpdate,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    update_role = await crud_update_role(
        role_id=role_id,
        new_data=new_data,
        session=session
    )
    return update_role


@router.delete("/")
async def deleted_role(
    role_id: int,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    deleted_role = await crud_deleted_role(role_id=role_id, session=session)
    return deleted_role
