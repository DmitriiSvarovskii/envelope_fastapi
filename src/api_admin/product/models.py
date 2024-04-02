from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.database import (
    Base, intpk, str_64,
    str_256, created_at, updated_at,
    deleted_at, deleted_flag
)


from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import (
        Category,
        Subcategory,
        Store,
        Cart,
        OrderDetail,

    )


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    name: Mapped[str_64] = mapped_column(unique=True)

    products: Mapped[List['Product']
                     ] = relationship(back_populates="unit")


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"))
    subcategory_id: Mapped[int | None] = mapped_column(
        ForeignKey("subcategories.id", ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    name: Mapped[str_64]
    description: Mapped[str_256 | None]
    image: Mapped[str | None]
    price: Mapped[float]
    wt: Mapped[int | None]
    unit_id: Mapped[int] = mapped_column(
        ForeignKey("public.units.id", ondelete="CASCADE"))
    kilocalories: Mapped[int | None]
    proteins: Mapped[int | None]
    fats: Mapped[int | None]
    carbohydrates: Mapped[int | None]
    availability: Mapped[bool]
    popular: Mapped[bool]
    delivery: Mapped[bool]
    takeaway: Mapped[bool]
    dinein: Mapped[bool]
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

    category: Mapped['Category'] = relationship(back_populates="products")
    subcategory: Mapped['Subcategory'] = relationship(
        back_populates="products")
    store: Mapped['Store'] = relationship(back_populates="products")
    unit: Mapped['Unit'] = relationship(back_populates="products")
    carts: Mapped['Cart'] = relationship(
        back_populates="product")
    order_details: Mapped['OrderDetail'] = relationship(
        back_populates="product")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
