from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, update, delete
from .models import Customer
from .schemas import CustomerBase, CustomerCreate, CustomerUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List


router = APIRouter(
    prefix="/customer",
    tags=["Customer"])


@router.get("/")
async def get_all_customer(session: AsyncSession = Depends(get_async_session)) -> List[CustomerBase]:
    query = select(Customer).order_by(Customer.id.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/add_cust/")
async def create_new_customer(new_customer: CustomerCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Customer).values(**new_customer.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/upd_cust/")
async def update_customer(customer_id: int, new_date: CustomerUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Customer).where(
        Customer.id == customer_id).values(**new_date.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/del_cust/")
async def delete_customer(customer_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Customer).where(
        Customer.id == customer_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
