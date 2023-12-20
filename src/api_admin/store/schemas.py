from datetime import datetime, time
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class StoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    # is_active: bool


class ListStoreInfoMini(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    link_bot: Optional[str] = None


class StoreAll(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    region: Optional[str | None]
    city: Optional[str | None]
    street: Optional[str | None]
    number_phone: Optional[int | None]
    mobile_phone: Optional[int | None]
    coordinates_1: Optional[int | None]
    coordinates_2: Optional[int | None]
    link_bot: Optional[str | None]
    delivery: Optional[bool | None]
    takeaway: Optional[bool | None]
    dinein: Optional[bool | None]
    time_zone: Optional[str | None]
    open_hours: Optional[time | None]
    close_hours: Optional[time | None]
    is_active: Optional[bool | None]


class StoreList(StoreBase):
    id: int
    # name: str


class StoreOrderTypeAssociations(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    is_active: bool
    order_type_id: int


class StoreCreate(StoreBase):
    link_bot: Optional[str] = None


class BotTokenCreate(BaseModel):
    token_bot: Optional[str] = None


class StoreDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class StoreUpdate(BaseModel):
    name: str
    # availability: bool


class StoreModel(StoreBase):
    id: int


# Схемы для работы с OrderType

class BaseOrderType(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    image: Optional[str] = None


class CreateOrderType(BaseOrderType):
    pass


class ListOrderType(BaseOrderType):
    id: int


# Схемы для работы с StoreOrderTypeAssociation

class BaseStoreOrderTypeAssociation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
    order_type_id: int
    is_active: bool


class CreateStoreOrderTypeAssociation(BaseStoreOrderTypeAssociation):
    pass


class ListStoreOrderTypeAssociation(BaseStoreOrderTypeAssociation):
    id: int


# Схемы для работы с StoreOrderTypeAssociation

class BaseStoreOrderTypeAssociation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
    order_type_id: int
    is_active: bool


class BaseWorkingDays(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    opening_time: time
    closing_time: time
    is_working: bool
    store_id: int
    day_of_week_id: int


class PostStoreInfo(BaseModel):
    name: str
    # is_active: bool
    adress: str
    number_phone: str
    mobile_phone: str
    latitude: float
    longitude: float
    link_bot: str
    time_zone: str
    format_unified: bool
    format_24_7: bool
    format_custom: bool
    open_hours_default: Optional[time] = None
    close_hours_default: Optional[time] = None
    store_id: int


class GetStoreInfo(BaseModel):
    id: int
    name: str
    # # is_active: str
    adress: Optional[str] = None
    number_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    link_bot: str
    time_zone: Optional[str] = None
    format_unified: bool
    format_24_7: bool
    format_custom: bool
    open_hours_default: Optional[time] = None
    close_hours_default: Optional[time] = None
    # custom_working_days: Optional[List[BaseWorkingDays]] = None
    # order_type: Optional[List[ListOrderType]] = None


class CreateDayOfWeek(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class TestManyToMany(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: Optional[int] = None
    store_name: Optional[str] = None
    order_type_name: Optional[str] = None
    order_type_id: Optional[int] = None
    is_active: Optional[bool] = None


class TestTest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: Optional[int] = None
    order_type_id: Optional[int] = None
    is_active: Optional[bool] = None


class TestDayOfWeek(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
    day_of_week_id: int
    opening_time: time
    closing_time: time
    is_working: bool


class WorkingHours(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    day_of_week_id: int
    day_of_week: str
    opening_time: Optional[time]
    closing_time: Optional[time]
    is_working: bool


class WorkingHoursList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    working_hours_list: List[WorkingHours]


class OneStoreInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    adress: Optional[str] = None
    number_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    link_bot: Optional[str] = None
    time_zone: Optional[str] = None
    format_unified: bool
    format_24_7: bool
    format_custom: bool
    open_hours_default: Optional[time] = None
    close_hours_default: Optional[time] = None


class InfoStoreSubscription(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    is_active: bool
    subscription_start_date: Optional[datetime] = None
    subscription_duration_months: Optional[int] = None
    paused_at: Optional[datetime] = None


class InfoStoreOrderType(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    image: Optional[str] = None


class StoreOrderType(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_type_id: int
    is_active: bool
    order_type: Optional[InfoStoreOrderType]


class OneStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    info: Optional[OneStoreInfo]
    subscriptions: Optional[InfoStoreSubscription]
    association: List[StoreOrderType]


class GetBotToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token_bot: str
    user_id: int
    store_id: int


class TypeOrderName(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: int
    image: Optional[str] = None


class ListTypeOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_type_id: int
    # store_id: int
    is_active: bool
    order_type: Optional[TypeOrderName]


class OneStoreTest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_info: Optional[OneStore]
    order_type_info: List[ListTypeOrder]


# class ListTypeOrder(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     order_type_id: int
#     order_type_name: str
#     is_active: bool
#     store_id: int


class ListStoreInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    info: Optional[ListStoreInfoMini]
    subscriptions: Optional[InfoStoreSubscription]
