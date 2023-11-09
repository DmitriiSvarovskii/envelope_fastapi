from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Product
from .schemas import *
from .crud import *
from ..user import User
from ..auth.routers import get_current_user_from_token


router = APIRouter(
    prefix="/api/v1/unit",
    tags=["Unit (admin)"])



@router.get("/", response_model=List[UnitList], status_code=200)
async def get_all_unit(current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        categories = await crud_get_all_units(schema=current_user.username, session=session)
        return categories
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", status_code=201)
async def create_new_unit(data: UnitCreate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        new_unit = await crud_create_new_unit(schema=current_user.username, data=data, user_id=current_user.id, session=session)
        return new_unit
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/", status_code=200)
async def update_unit(unit_id: int, data: UnitUpdate,  current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        up_unit = await crud_update_unit(schema=current_user.username, unit_id=unit_id, data=data, user_id=current_user.id, session=session)
        return up_unit
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/")
async def delete_unit(unit_id: int, current_user: User = Depends(get_current_user_from_token), session: AsyncSession = Depends(get_async_session)):
    try:
        change_unit = await crud_delete_unit(schema=current_user.username, unit_id=unit_id, session=session)
        return change_unit
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
