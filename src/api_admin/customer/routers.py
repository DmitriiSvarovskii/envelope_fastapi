from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import insert, select, delete, update

from src.database import get_async_session


from .models import Customer
from .schemas import CustomerBase, CustomerCreate, CustomerUpdate
from ..auth.routers import get_current_user_from_token
from ..user import User

router = APIRouter(
    prefix="/api/v1/customer",
    tags=["Customer (store)"])


@router.get("/")
async def get_all_customer(
    store_id: int,
    current_user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session)
) -> List[CustomerBase]:
    query = (
        select(Customer).
        where(Customer.store_id == store_id).
        order_by(Customer.id.desc()).
        execution_options(schema_translate_map={None: str(current_user.id)})
    )
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/")
async def create_new_customer(
    schema: str,
    new_customer: CustomerCreate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        insert(Customer).
        values(**new_customer.model_dump()).
        execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/")
async def update_customer(
    schema: str,
    customer_id: int,
    new_date: CustomerUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        update(Customer).
        where(Customer.id == customer_id).
        values(**new_date.model_dump()).
        execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/")
async def delete_customer(
    schema: str,
    customer_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        delete(Customer).
        where(Customer.id == customer_id).
        execution_options(schema_translate_map={None: schema})
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
