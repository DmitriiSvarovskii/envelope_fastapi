from sqlalchemy import and_
from sqlalchemy.orm import selectinload
import jwt
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from urllib.parse import unquote
from hashlib import sha256
import re
import base64
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from .models import Unit
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from typing import List, Annotated
from fastapi import FastAPI, HTTPException
import hashlib
import hmac


router = APIRouter(
    prefix="/api/v1/unit",
    tags=["Unit (for Product)"])


@router.get("/", summary="Получение списка единиц измерения", response_model=List[UnitBase])
async def get_all_unit(session: AsyncSession = Depends(get_async_session)):
    """
    Получение списка единиц измерения.

    Этот маршрут позволяет получить список всех доступных единиц измерения.

    Возвращает:
    - Список единиц измерения.
    """
    query = select(Unit).order_by(Unit.id)
    result = await session.execute(query)
    units = result.scalars().all()
    unit_dicts = [unit.__dict__ for unit in units]
    return unit_dicts


@router.post("/", summary="Создание новой единицы измерения", response_model=dict)
async def create_new_unit(new_unit: UnitCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Создание новой единицы измерения.

    Этот маршрут позволяет создать новую единицу измерения.

    Параметры:
    - `new_unit`: данные для создания новой единицы измерения.

    Возвращает:
    - Сообщение о успешном создании.
    """
    stmt = insert(Unit).values(**new_unit.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/", summary="Обновление единицы измерения", response_model=dict)
async def update_unit(unit_id: int, new_data: UnitUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Обновление единицы измерения.

    Этот маршрут позволяет обновить данные о существующей единице измерения.

    Параметры:
    - `unit_id`: идентификатор единицы измерения.
    - `new_data`: данные для обновления.

    Возвращает:
    - Сообщение о успешном обновлении.
    """
    stmt = update(Unit).where(Unit.id == unit_id).values(**new_data.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/", summary="Удаление единицы измерения", response_model=dict)
async def delete_unit(unit_id: int, session: Session = Depends(get_async_session)):
    """
    Удаление единицы измерения.

    Этот маршрут позволяет удалить единицу измерения по идентификатору.

    Параметры:
    - `unit_id`: идентификатор единицы измерения.

    Возвращает:
    - Сообщение об успешном удалении или сообщение об ошибке.
    """
    try:
        stmt = delete(Unit).where(Unit.id == unit_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": f"Единица измерения с id {unit_id} успешно удалена."}
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка: {str(e)}")
