from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Time, Enum
from sqlalchemy.orm import relationship
from src.database import *
from sqlalchemy import create_engine, Column, func, DateTime, Integer, BIGINT
from typing import List, TYPE_CHECKING
import datetime
if TYPE_CHECKING:
    from ..category import Category
    from ..user import User
    from ..product import Product


class Store(Base):
    __tablename__ = 'stores'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    region: Mapped[str_64 | None]
    city: Mapped[str_64 | None]
    street: Mapped[str_256 | None]
    number_phone: Mapped[int | None] = mapped_column(BIGINT)
    mobile_phone: Mapped[int | None] = mapped_column(BIGINT)
    coordinates_1: Mapped[int | None] = mapped_column(BIGINT)
    coordinates_2: Mapped[int | None] = mapped_column(BIGINT)
    link_bot: Mapped[str_256 | None]
    delivery: Mapped[bool | None]
    takeaway: Mapped[bool | None]
    dinein: Mapped[bool | None]
    time_zone: Mapped[str_64 | None]
    open_hours: Mapped[datetime.datetime | None]
    close_hours: Mapped[datetime.datetime | None]
    is_active: Mapped[bool | None]
    subscription_start_date: Mapped[datetime.datetime | None]
    subscription_duration_months: Mapped[int | None]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
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

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class BotToken(Base):
    __tablename__ = 'bot_tokens'
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    token_bot: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    store_id: Mapped[int]


class PaymentAndDelivery(Base):
    __tablename__ = 'payment_and_deliverys'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    cash: Mapped[bool]
    card: Mapped[bool]
    sbp: Mapped[bool]
    min_order_amount_for_free_delivery: Mapped[int | None]
    min_delivery_amount: Mapped[int | None]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class ServiceChat(Base):
    __tablename__ = 'service_chats'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    welcome_message_bot: Mapped[str_4048 | None]
    welcome_image: Mapped[str | None]
    tg_id_group: Mapped[int | None] = mapped_column(BIGINT)
    delivery_chat: Mapped[int | None] = mapped_column(BIGINT)
    order_chat: Mapped[int | None] = mapped_column(BIGINT)
    completed_orders_chat: Mapped[int | None] = mapped_column(BIGINT)
    canceled_orders_chat: Mapped[int | None] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class LegalInformation(Base):
    __tablename__ = 'legal_informations'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    full_organization_name: Mapped[str_4048 | None]
    legal_address: Mapped[str | None]
    legal_phone: Mapped[int | None] = mapped_column(BIGINT)
    inn: Mapped[int | None] = mapped_column(BIGINT)
    ogrn: Mapped[int | None] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
