from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import (
    Base, intpk, str_64,
    created_at, updated_at,
    deleted_flag, deleted_at
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..category import Category
    from ..product import Product
    from ..store import Store


class Subcategory(Base):
    __tablename__ = 'subcategories'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    availability: Mapped[bool]
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"))
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

    parent_category: Mapped['Category'] = relationship(
        back_populates="subcategories")
    store: Mapped['Store'] = relationship(back_populates="subcategories")
    products: Mapped['Product'] = relationship(
        back_populates="subcategory")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
