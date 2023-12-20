from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.database import *
from sqlalchemy import BIGINT
from typing import List, TYPE_CHECKING
from sqlalchemy import Time

import datetime
if TYPE_CHECKING:
    from ..models import *
    # from ..category import Category
    # from ..user import User
    # from ..product import Product
from sqlalchemy.ext.associationproxy import association_proxy


class Store(Base):
    __tablename__ = 'stores'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
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

    association: Mapped[List['StoreOrderTypeAssociation']
                        ] = relationship(back_populates="store")
    subcategories: Mapped['Subcategory'] = relationship(back_populates="store")

    carts: Mapped[List['Cart']] = relationship(
        back_populates="store")
    categories: Mapped[List['Category']] = relationship(
        back_populates="store")
    customers: Mapped[List['Customer']] = relationship(
        back_populates="store")
    mails: Mapped[List['Mail']] = relationship(
        back_populates="store")

    orders: Mapped[List['Order']] = relationship(
        back_populates="store")
    order_details: Mapped[List['OrderDetail']] = relationship(
        back_populates="store")
    order_customer_info: Mapped[List['OrderCustomerInfo']] = relationship(
        back_populates="store")
    products: Mapped[List['Product']] = relationship(
        back_populates="store")
    subscriptions: Mapped['StoreSubscription'] = relationship(
        back_populates="store")
    payments: Mapped[List['StorePayment']] = relationship(
        back_populates="store")
    info: Mapped['StoreInfo'] = relationship(
        back_populates="store")
    subscriptions_history: Mapped[List['SubscriptionHistory']] = relationship(
        back_populates="store")
    working_days: Mapped[List['WorkingDay']] = relationship(
        back_populates="store")
    service_text_and_chats: Mapped['ServiceTextAndChat'] = relationship(
        back_populates="store")
    legal_information: Mapped['LegalInformation'] = relationship(
        back_populates="store", uselist=False)
    delivery_distance: Mapped['DeliveryDistance'] = relationship(
        back_populates="store", uselist=False)
    delivery_fix: Mapped['DeliveryFix'] = relationship(
        back_populates="store", uselist=False)
    delivery_district: Mapped['DeliveryDistrict'] = relationship(
        back_populates="store", uselist=False)


    # order_typed: Mapped[List['OrderType']] = relationship(
    #     back_populates='store_order_types',
    #     secondary='store_order_types_association'
    # )
    
        # user: Mapped['User'] = relationship(
    #     back_populates="store",
    #     foreign_keys=['user_id', 'created_by', 'updated_by', 'deleted_by']
    # )
    
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

    user: Mapped['User'] = relationship(
        back_populates="bot_token")


class OrderType(Base):
    __tablename__ = "order_types"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    name: Mapped[str_64]
    image: Mapped[str | None]

    orders: Mapped['Order'] = relationship(back_populates="order_type")
    association: Mapped[List['StoreOrderTypeAssociation']
                        ] = relationship(back_populates="order_type")
    # store_order_types: Mapped[List['Store']] = relationship(
    #     back_populates='order_typed',
    #     secondary='store_order_types_association'
    # )


class StoreOrderTypeAssociation(Base):
    __tablename__ = "store_order_types_association"
    __table_args__ = {'schema': None}

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"),
        primary_key=True)
    order_type_id: Mapped[int] = mapped_column(
        ForeignKey("public.order_types.id", ondelete="CASCADE"),
        primary_key=True)
    is_active: Mapped[bool]

    order_type: Mapped['OrderType'] = relationship(
        back_populates="association")
    store: Mapped['Store'] = relationship(back_populates="association")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class StoreInfo(Base):
    __tablename__ = 'stores_info'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str_64]
    adress: Mapped[str | None]
    number_phone: Mapped[str | None]
    mobile_phone: Mapped[str | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    link_bot: Mapped[str_256 | None]
    time_zone: Mapped[str_64 | None] = mapped_column(
        server_default=text("'Europe/Moscow'"))
    format_unified: Mapped[bool] = mapped_column(server_default=text("false"))
    format_24_7: Mapped[bool] = mapped_column(server_default=text("false"))
    format_custom: Mapped[bool] = mapped_column(server_default=text("false"))
    open_hours_default: Mapped[datetime.time | None]
    close_hours_default: Mapped[datetime.time | None]

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    store: Mapped['Store'] = relationship(
        back_populates="info")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class StoreSubscription(Base):
    __tablename__ = 'store_subscriptions'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    is_active: Mapped[bool] = mapped_column(server_default=text("false"))
    subscription_start_date: Mapped[datetime.datetime | None]
    subscription_duration_months: Mapped[int | None]
    paused_at: Mapped[datetime.datetime | None]

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    store: Mapped['Store'] = relationship(
        back_populates="subscriptions")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class SubscriptionHistory(Base):
    __tablename__ = 'subscription_history'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    subscription_start_date: Mapped[datetime.datetime]
    paused_at: Mapped[datetime.datetime | None]
    resumed_at: Mapped[datetime.datetime | None]
    payment_date: Mapped[datetime.datetime | None]
    payment_duration_days: Mapped[int | None]

    store: Mapped['Store'] = relationship(
        back_populates="subscriptions_history")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class DayOfWeek(Base):
    __tablename__ = 'days_of_week'
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    day_of_week: Mapped[str_64] = mapped_column(unique=True, index=True)
    number_day: Mapped[int] = mapped_column(unique=True, index=True)
    # one_working_days: Mapped['WorkingDay'] = relationship(
    #     back_populates='days_of_week',
    # )


class WorkingDay(Base):
    __tablename__ = 'working_days'
    __table_args__ = {'schema': None}

    # id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"), primary_key=True)
    day_of_week_id: Mapped[int] = mapped_column(
        ForeignKey("public.days_of_week.id", ondelete="CASCADE"), primary_key=True)
    opening_time: Mapped[datetime.time | None]
    closing_time: Mapped[datetime.time | None]
    is_working: Mapped[bool] = mapped_column(server_default=text("false"))
    store: Mapped['Store'] = relationship(back_populates="working_days")
    # day_of_week: Mapped['DayOfWeek'] = relationship(
    #     back_populates="working_days")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class StorePayment(Base):
    __tablename__ = 'store_payments'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    cash: Mapped[bool] = mapped_column(server_default=text("false"))
    card: Mapped[bool] = mapped_column(server_default=text("false"))
    min_delivery_amount: Mapped[int | None]
    min_order_amount_for_free_delivery: Mapped[int | None]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    store: Mapped['Store'] = relationship(
        back_populates="payments")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class ServiceTextAndChat(Base):
    __tablename__ = 'service_text_and_chats'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    email: Mapped[str | None]
    welcome_message_bot: Mapped[str_4048 | None]
    welcome_image: Mapped[str | None]
    tg_id_group: Mapped[int | None] = mapped_column(BIGINT)
    delivery_chat: Mapped[int | None] = mapped_column(BIGINT)
    order_chat: Mapped[int | None] = mapped_column(BIGINT)
    completed_orders_chat: Mapped[int | None] = mapped_column(BIGINT)
    canceled_orders_chat: Mapped[int | None] = mapped_column(BIGINT)
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    store: Mapped['Store'] = relationship(
        back_populates="service_text_and_chats")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class LegalInformation(Base):
    __tablename__ = 'legal_informations'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    full_organization_name: Mapped[str | None]
    legal_country: Mapped[str_64 | None]
    legal_region: Mapped[str_64 | None]
    legal_city: Mapped[str_64 | None]
    legal_street: Mapped[str | None]
    legal_number_phone: Mapped[int | None] = mapped_column(BIGINT)
    inn: Mapped[int | None] = mapped_column(BIGINT)
    ogrn: Mapped[int | None] = mapped_column(BIGINT)
    postal_code: Mapped[int | None] = mapped_column(BIGINT)
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    store: Mapped['Store'] = relationship(
        back_populates="legal_information", uselist=False)

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class DeliveryDistance(Base):
    __tablename__ = 'delivery_distance'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    start_price: Mapped[int]
    price_per_km: Mapped[int]
    min_price: Mapped[int]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    store: Mapped['Store'] = relationship(back_populates="delivery_distance")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class DeliveryFix(Base):
    __tablename__ = 'delivery_fix'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    price: Mapped[str]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    store: Mapped['Store'] = relationship(back_populates="delivery_fix")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class DeliveryDistrict(Base):
    __tablename__ = 'stodelivery_districts'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[int]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    store: Mapped['Store'] = relationship(back_populates="delivery_district")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class PaymentYookassa(Base):
    __tablename__ = 'payments_yookassa'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    api_id: Mapped[int] = mapped_column(BIGINT)
    api_key: Mapped[str]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
