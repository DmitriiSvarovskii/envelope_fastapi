# from typing import AsyncGenerator

# from fastapi import Depends
# from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# from sqlalchemy.orm import DeclarativeBase
# from src.database import Base, get_async_session, intpk, str_64, created_at, updated_at, deleted_at
# from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey, func, DateTime, Integer, String, Boolean
# from sqlalchemy.orm import Mapped, mapped_column


# class Role(Base):
#     __tablename__ = "roles"

#     id: Mapped[intpk]
#     name: Mapped[str_64] = mapped_column(unique=True)
#     # permissions: Mapped[json]
#     is_active: Mapped[bool] = Column(Boolean, server_default="true")
#     created_at: Mapped[created_at]
#     updated_at: Mapped[updated_at]
#     deleted_flag: Mapped[bool] = Column(Boolean, server_default="false")
#     deleted_at: Mapped[deleted_at]


# class User(SQLAlchemyBaseUserTable[int], Base):
#     __tablename__ = "users"

#     id: Mapped[intpk]
#     username: Mapped[str_64] = mapped_column(unique=True)
#     email: Mapped[str] = mapped_column(
#         String(length=320), unique=True, index=True, nullable=False
#     )
#     hashed_password: Mapped[str] = mapped_column(
#         String(length=1024), nullable=False
#     )
#     role_id: Mapped[int] = Column(Integer,
#                                   ForeignKey("roles.id", ondelete="CASCADE"), server_default="1")
#     name: Mapped[str_64 | None]
#     number_phone: Mapped[int] = mapped_column(unique=True, nullable=True)
#     is_active: Mapped[bool] = Column(
#         Boolean, server_default="true", nullable=False)
#     is_superuser: Mapped[bool] = Column(
#         Boolean, server_default="false", nullable=False)
#     is_verified: Mapped[bool] = Column(
#         Boolean, server_default="false", nullable=False)
#     created_at: Mapped[created_at]
#     updated_at: Mapped[updated_at]
#     deleted_flag: Mapped[bool] = Column(Boolean, server_default="false")
#     deleted_at: Mapped[deleted_at]


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
