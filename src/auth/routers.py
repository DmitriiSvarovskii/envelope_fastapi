from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_async_session

from src.user.models import User
from .models import Token
from .schemas import UserAuth, TokenCreate
from src.secure import pwd_context


router = APIRouter(
    prefix="/auth",
    tags=["Auth"])


@router.post("/", response_model=TokenCreate)
async def create_token(user_data: UserAuth, session: Session = Depends(get_async_session)):
    user: User = await session.scalar(select(User).where(
        User.username == user_data.username))
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not pwd_context.verify(user_data.hashed_password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    token: Token = Token(user_id=user.id, access_token=str(uuid4()))
    session.add(token)
    await session.commit()
    return {"access_token": token.access_token}
