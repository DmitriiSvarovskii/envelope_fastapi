from typing import List
from datetime import datetime
from sqlalchemy import create_engine, Column, func, DateTime, Integer, BIGINT, TIMESTAMP, String, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import *
from sqlalchemy.orm import Mapped, mapped_column

import sqlalchemy
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import *


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    username: Mapped[str_64] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str_64 | None]
    user_tg_id: Mapped[int | None] = mapped_column(BIGINT)
    number_phone: Mapped[int] = mapped_column(unique=True, nullable=True)
    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("public.employees.id", ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(
        ForeignKey("public.roles.id", ondelete="CASCADE"), server_default=text("1"))
    is_active: Mapped[is_active]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]

    role: Mapped['Role'] = relationship(back_populates="users")
    token: Mapped['Token'] = relationship(back_populates="user")
    bot_token: Mapped['BotToken'] = relationship(
        back_populates="user")
    # store: Mapped['Store'] = relationship(
    #     back_populates="user")
    # back_populates="user_product")

    # def __init__(self, schema):
    #     super().__init__()
    #     self.__table_args__ = {'schema': schema}
