from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderBase(BaseModel):
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
    id: int
    order_date: datetime
    # customer: "Customer"

    class Config:
        orm_mode = True


class OrderDetailBase(BaseModel):
    shop_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetail(OrderDetailBase):
    id: int
    order_date: datetime
    shop_id: int

    class Config:
        orm_mode = True
