from sqlalchemy import BIGINT, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import *


class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(BIGINT)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]

    store: Mapped['Store'] = relationship(
        back_populates="carts")
    product: Mapped['Product'] = relationship(
        back_populates="carts")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}

    __table_args__ = (
        ForeignKeyConstraint(['store_id', 'tg_user_id'], [
                             'customers.store_id', 'customers.tg_user_id'], ondelete="CASCADE"),
    )
