from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shop_id: int
    tg_user_id: int
    delivery_city: str
    delivery_address: str
    customer_name: str
    customer_phone: str
    customer_comment: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_date: datetime
    # customer: "Customer"



class OrderDetailBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shop_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetail(OrderDetailBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_date: datetime
    shop_id: int
