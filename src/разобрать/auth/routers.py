from typing import Annotated
from fastapi import HTTPException, status, Response
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_async_session

from src.user.models import User
from .models import Token
from .schemas import UserAuth, TokenCreate
from src.secure import pwd_context, oauth2_scheme
import jwt
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth"])

SECRET_KEY = "your_secret_key_here"


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


@router.post("/", response_model=TokenCreate)
async def create_token(user_data: UserAuth, response: Response, session: Session = Depends(get_async_session)):
    user: User = await session.scalar(select(User).where(User.username == user_data.username))
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not pwd_context.verify(user_data.hashed_password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    token_data = {"sub": user_data.username}
    jwt_token = create_jwt_token(token_data)

    # Устанавливаем токен в куках с именем "access_token" и временем истечения в секундах
    response.set_cookie(key="access_token", value=jwt_token, expires=3600)

    return {"access_token": jwt_token}


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# @router.post("/", response_model=TokenCreate)
# async def create_token(user_data: UserAuth, session: Session = Depends(get_async_session)):
#     user: User = await session.scalar(select(User).where(
#         User.username == user_data.username))
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )

#     if not pwd_context.verify(user_data.hashed_password, user.hashed_password):
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password")

#     token: Token = Token(user_id=user.id, access_token=str(uuid4()))
#     session.add(token)
#     await session.commit()
#     return {"access_token": token.access_token}
