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
    adress: Optional[str] = None
    number_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    link_bot: Optional[str] = None
    time_zone: Optional[str] = None


class BaseLegalInformation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_organization_name: Optional[str] = None
    legal_adress: Optional[str] = None
    legal_number_phone: Optional[str] = None
    inn: Optional[int] = None
    ogrn: Optional[int] = None
    postal_code: Optional[int] = None


class UpdateLegalInformation(BaseLegalInformation):
    pass


class GetLegalInformation(BaseLegalInformation):
    store_id: int


class BaseServiceTextAndChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: Optional[str] = None
    welcome_message_bot: Optional[str] = None
    welcome_image: Optional[str] = None
    tg_id_group: Optional[int] = None
    delivery_chat: Optional[int] = None
    order_chat: Optional[int] = None
    completed_orders_chat: Optional[int] = None
    canceled_orders_chat: Optional[int] = None


class UpdateServiceTextAndChat(BaseServiceTextAndChat):
    pass


class GetServiceTextAndChat(BaseServiceTextAndChat):
    store_id: int


class BaseStorePayment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cash: bool
    card: bool
    min_delivery_amount: Optional[int] = None
    min_order_amount_for_free_delivery: Optional[int] = None


class UpdateStorePayment(BaseStorePayment):
    pass


class GetStorePayment(BaseStorePayment):
    store_id: int


class BaseDeliveryDistance(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_price: Optional[int] = None
    price_per_km: Optional[int] = None
    min_price: Optional[int] = None


class UpdateDeliveryDistance(BaseDeliveryDistance):
    pass


class GetDeliveryDistance(BaseDeliveryDistance):
    store_id: Optional[int] = None


class BaseDeliveryFix(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    price: Optional[int] = None


class UpdateDeliveryFix(BaseDeliveryFix):
    pass


class GetDeliveryFix(BaseDeliveryFix):
    store_id: Optional[int] = None


class BaseDeliveryDistrict(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    price: Optional[int] = None


class UpdateDeliveryDistrict(BaseDeliveryDistrict):
    pass


class GetDeliveryDistrict(BaseDeliveryDistrict):
    id: int
    store_id: Optional[int] = None


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


class BaseDayOfWeek(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    is_working: bool


class UpdaneDayOfWeek(BaseDayOfWeek):
    pass


class GetDayOfWeek(BaseDayOfWeek):
    store_id: int
    day_of_week_id: int


class WorkingHours(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    day_of_week_id: int
    day_of_week: str
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
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


class InfoStoreDayOfWeek(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    day_of_week: str
    number_day: int


class StoreWorkingDay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    day_of_week_id: int
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    is_working: bool
    days_of_week: Optional[InfoStoreDayOfWeek]


class OneStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    info: Optional[OneStoreInfo]
    subscriptions: Optional[InfoStoreSubscription]
    association: List[StoreOrderType]
    working_days: List[StoreWorkingDay]
    payments: Optional[GetStorePayment]
    delivery_distance: Optional[GetDeliveryDistance] = None
    delivery_fix: Optional[GetDeliveryFix] = None
    delivery_district: Optional[GetDeliveryDistrict] = None
    service_text_and_chats: Optional[GetServiceTextAndChat]
    legal_information: Optional[GetLegalInformation]


class GetBotToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token_bot: str
    user_id: int
    store_id: int


class GetAllBotToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token_bot: str


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
