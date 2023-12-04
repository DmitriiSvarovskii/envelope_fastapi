from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.database import *
from sqlalchemy import create_engine, Column, func, DateTime, Integer, BIGINT
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..category import Category, Subcategory
    from ..user import User
    from ..product import Product


class Store(Base):
    __tablename__ = 'stores'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    # is_active: Mapped[bool]
    token_bot: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    tg_id_group: Mapped[int | None] = mapped_column(BIGINT)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))

    # product_category: Mapped[List['Product']
    #                          ] = relationship(back_populates="category")
    # category_category: Mapped[List['Category']
    #                              ] = relationship(back_populates="subcategory_category")
    # category_subcategory: Mapped[List['Subcategory']
    #                              ] = relationship(back_populates="subcategory_category")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
