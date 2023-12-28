from enum import Enum
from datetime import datetime
from sqlalchemy import BIGINT, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import *
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from ..models import *


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(BIGINT)
    order_type_id: Mapped[int] = mapped_column(
        ForeignKey("public.order_types.id", ondelete="CASCADE"))
    order_status_id: Mapped[int] = mapped_column(
        ForeignKey("public.order_status.id", ondelete="CASCADE"), server_default=text("1"))
    created_at: Mapped[created_at]

    store: Mapped['Store'] = relationship(back_populates="orders")
    order_customer_info: Mapped[List['OrderCustomerInfo']] = relationship(
        back_populates="orders")
    # customer: Mapped['Customer'] = relationship(back_populates="orders")
    order_type: Mapped['OrderType'] = relationship(back_populates="orders")
    order_status: Mapped['OrderStatus'] = relationship(back_populates="orders")
    order_details: Mapped['OrderDetail'] = relationship(
        back_populates="orders")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}

    __table_args__ = (
        ForeignKeyConstraint(['store_id', 'tg_user_id'], [
                             'customers.store_id', 'customers.tg_user_id'], ondelete="CASCADE"),
    )


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
    unit_price: Mapped[float]
    created_at: Mapped[created_at]

    store: Mapped['Store'] = relationship(back_populates="order_details")
    orders: Mapped['Order'] = relationship(back_populates="order_details")
    product: Mapped['Product'] = relationship(back_populates="order_details")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class OrderStatus(Base):
    __tablename__ = "order_status"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    status_name: Mapped[str_64]
    orders: Mapped['Order'] = relationship(back_populates="order_status")


class OrderCustomerInfo(Base):
    __tablename__ = "order_customer_info"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(BIGINT)
    tg_user_name: Mapped[str | None]
    table_number: Mapped[str | None]
    delivery_city: Mapped[str | None]
    delivery_address: Mapped[str | None]
    customer_name: Mapped[str | None]
    customer_phone: Mapped[str | None]
    customer_comment: Mapped[str | None]

    store: Mapped['Store'] = relationship(back_populates="order_customer_info")
    orders: Mapped['Order'] = relationship(
        back_populates="order_customer_info")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}

    __table_args__ = (
        ForeignKeyConstraint(['store_id', 'tg_user_id'], [
                             'customers.store_id', 'customers.tg_user_id'], ondelete="CASCADE"),
    )
