from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete, update
from .models import Employee
from .schemas import EmployeeBase, EmployeeCreate, EmployeeUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List, Annotated
from src.secure import apikey_scheme
from ..user.models import User

router = APIRouter(
    prefix="/employee",
    tags=["Employee"])


# Получение списка всех категорий
@router.get("/")
async def get_all_employee(access_token: Annotated[str, Depends(apikey_scheme)], session: AsyncSession = Depends(get_async_session)) -> List[EmployeeBase]:
    query = select(Employee).order_by(Employee.id.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/token_all")
async def get_all_token_bots(session: AsyncSession = Depends(get_async_session)) -> List[str]:
    query = select(User.token_bot)
    result = await session.execute(query)
    token_bots = [row for row in result.scalars().all()]
    return token_bots


@router.post("/add_empl/")
async def create_new_employee(access_token: Annotated[str, Depends(apikey_scheme)], new_employee: EmployeeCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Employee).values(**new_employee.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/upd_empl/")
async def update_employee(access_token: Annotated[str, Depends(apikey_scheme)], employee_id: int, new_date: EmployeeUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Employee).where(
        Employee.id == employee_id).values(**new_date.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/del_empl/")
async def delete_employee(access_token: Annotated[str, Depends(apikey_scheme)], employee_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Employee).where(
        Employee.id == employee_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
