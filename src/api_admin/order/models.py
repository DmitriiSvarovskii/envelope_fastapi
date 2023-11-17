from datetime import datetime
from sqlalchemy import Column, Integer, TIMESTAMP, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import *


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(
        ForeignKey("customers.tg_user_id", ondelete="CASCADE"))
    delivery_city: Mapped[str | None]
    delivery_address: Mapped[str | None]
    customer_name: Mapped[str | None]
    customer_phone: Mapped[str | None]
    customer_comment: Mapped[str | None]
    created_at: Mapped[created_at]

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class OrderDetail(Base):
    __tablename__ = "order_details"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    unit_price: Mapped[int]
    created_at: Mapped[created_at]

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
