import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from PIL import Image as PILImage
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import *

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..category import Category, Subcategory
    from ..user import User
    from ..product import Product


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool]
    # position: Mapped[int] = mapped_column(Integer, nullable=True)
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

    product_category: Mapped[List['Product']
                             ] = relationship(back_populates="category")
    category_subcategory: Mapped[List['Subcategory']
                                 ] = relationship(back_populates="subcategory_category")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class Subcategory(Base):
    __tablename__ = 'subcategories'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool]
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"))
    # position: Mapped[int] = mapped_column(Integer, nullable=True)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))

    product_subcategory: Mapped[List['Product']
                                ] = relationship(back_populates="subcategory")
    subcategory_category: Mapped['Category'] = relationship(
        back_populates="category_subcategory")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
