import jwt
from typing import List
from jose import JWTError
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.secure import pwd_context, oauth2_scheme
from src.config import SECRET_KEY_JWT, ALGORITHM
from src.database import get_async_session
from ..models import User
from .schemas import *


router = APIRouter(
    prefix="/api/v1/login",
    tags=["Login (admin)"])


SECRET_KEY = SECRET_KEY_JWT
ALGORITHM = ALGORITHM


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/", response_model=TokenCreate)
async def create_token(response: Response, user_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user: User = await session.scalar(select(User).where(User.username == user_data.username))
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    token_data = {"sub": user_data.username}
    jwt_token = create_jwt_token(token_data)
    response.set_cookie(key="access_token", value=jwt_token, expires=3600)
    return {"access_token": jwt_token, "data": {'username': user.username, 'user_id': user.id}}


async def get_user(username: str, session: AsyncSession = Depends(get_async_session)) -> List[UserAuth]:
    query = select(User).where(
        User.username == username)
    result = await session.execute(query)
    user = result.scalars().all()
    return user


async def get_current_user_from_token(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username=username, session=session)
    if user is None:
        raise credentials_exception
    user_response = UserAuth(id=user[0].id,
                             username=user[0].username,
                             name=user[0].name,
                             number_phone=user[0].number_phone,
                             role_id=user[0].role_id)
    return user_response


@router.get("/test/",)
async def read_items(current_user: User = Depends(get_current_user_from_token)):
    return {"token": current_user}
