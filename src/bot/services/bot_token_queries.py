from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_session
from src.api_admin.models import BotToken


async def get_info_store_token_all(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(BotToken)
        result = await session.execute(query)
        store = result.scalars().all()
        return store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


async def get_info_store_token(
    bot_token: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(BotToken).where(BotToken.token_bot == bot_token)
        result = await session.execute(query)
        store = result.scalar()
        return store
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
