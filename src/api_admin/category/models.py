from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import *

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..subcategory import Subcategory
    from ..product import Product
    from ..store import Store


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
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

    store: Mapped['Store'] = relationship(back_populates="categories")
    subcategories: Mapped['Subcategory'] = relationship(
        back_populates="parent_category")
    products: Mapped['Product'] = relationship(back_populates="category")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
