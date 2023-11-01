from sqlalchemy import Column, func, DateTime, Integer, BIGINT, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from src.database import *
from typing import List

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..category import Category, Subcategory
    from ..user import User
    from ..product import Product


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    first_name: Mapped[str_64]
    last_name: Mapped[str_64]
    number_phone: Mapped[int] = mapped_column(unique=True, nullable=True)
    tg_user_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    is_active: Mapped[is_active]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]

    user_employee: Mapped[List['User']] = relationship(
        back_populates="employee")

    # def __init__(self, schema):
    #     super().__init__()
    #     self.__table_args__ = {'schema': schema}

    # user_employee = relationship(
    #     "users", back_populates="employee")

    # user_employee: Mapped[List['User']] = relationship(
    #     back_populates="employee")
