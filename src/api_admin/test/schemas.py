from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class RolesCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = 'user'


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = '1'
    hashed_password: str = '1'
    # username: str = 'envelope@gmail.com'
    # hashed_password: str = '123456qwe!Q'


class CreateStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = 'Envelope Demo'
    link_bot: str = 'https://t.me/dmitrii_test_bot'


class CreateBotToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token_bot: str = '5895760296:AAF2hSRl3TAIrZGHD6M5sSDdtdYkQPr9sUc'


class CreateUnitList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class DeliveryTypeList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    delivery_name: str


class CreateOrderTypeList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class CreateDayOfWeekList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    day_of_week: str
    number_day: int


class CreateOrderStatusList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status_name: str


class CreateUnit(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data_unit: List[CreateUnitList] = [
        {'name': 'шт'},
        {'name': 'порц'},
        {'name': 'мл'},
        {'name': 'л'}
    ]


class DeliveryTypeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data_delivery_type: List[DeliveryTypeList] = [
        {'delivery_name': 'фиксированная цена'},
        {'delivery_name': 'по районам'},
        {'delivery_name': 'по км'},
    ]


class CreateOrderStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data_order_status: List[CreateOrderStatusList] = [
        {'status_name': 'Новый'},
        {'status_name': 'Принят'},
        {'status_name': 'Готовится'},
        {'status_name': 'Доставляется'},
        {'status_name': 'Доставлен'},
        {'status_name': 'Отменен'},
        {'status_name': 'Возврат'},
        {'status_name': 'Завершен'},
    ]


class CreateDayOfWeek(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data_day_of_week: List[CreateDayOfWeekList] = [
        {'day_of_week': 'ПН', 'number_day': 1},
        {'day_of_week': 'ВТ', 'number_day': 2},
        {'day_of_week': 'СР', 'number_day': 3},
        {'day_of_week': 'ЧТ', 'number_day': 4},
        {'day_of_week': 'ПТ', 'number_day': 5},
        {'day_of_week': 'СБ', 'number_day': 6},
        {'day_of_week': 'ВС', 'number_day': 7}
    ]


class CreateOrderType(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data_order_type: List[CreateOrderTypeList] = [
        {'name': 'Доставка'},
        {'name': 'Самовывоз'},
        {'name': 'В зале'}
    ]


class CategoryCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = ' category'
    availability: bool = True


class ProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_id: int = 1
    name: str = ' product'
    description: str = ' decription product'
    image: str = 'https://storage.yandexcloud.net/envelope-app/1/1/2023-11-28_09-13-12_cesare-chiken.jpeg'
    price: float = 150.0
    unit_id: int = 1
    wt: int = 1
    kilocalories: int = 15
    proteins: int = 2
    fats: int = 4
    carbohydrates: int = 3
    availability: bool = True
    popular: bool = True
    delivery: bool = True
    takeaway: bool = False
    dinein: bool = False
