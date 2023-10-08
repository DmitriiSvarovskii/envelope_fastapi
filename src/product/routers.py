from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from .models import Product
from .schemas import ProductModel, ProductCreate, ProductUpdate, ProductList, ProductOne
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from typing import List, Dict


router = APIRouter(
    prefix="/menu",
    tags=["Menu. Product"])


@router.get("/products/{shop_id}/")
async def get_all_products(shop_id: int, session: AsyncSession = Depends(get_async_session)) -> List[ProductList]:
    query = select(Product).where(Product.shop_id ==
                                  shop_id).where(Product.availability == True)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/products/{shop_id}/{product_id}")
async def get_one_product(shop_id: int, product_id: int, session: AsyncSession = Depends(get_async_session)) -> List[ProductOne]:
    query = select(Product).where(Product.shop_id ==
                                  shop_id).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/products/")
async def create_new_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Product).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/products/")
async def update_product(product_id: int, new_date: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(Product).where(
        Product.id == product_id).values(**new_date.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/products/")
async def delete_product(shop_id: int, product_id: int, session: Session = Depends(get_async_session)):
    try:
        stmt = delete(Product).where(Product.shop_id ==
                                     shop_id).where(Product.id == product_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": f"Продукт, c id {product_id}, успешно удалена."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
