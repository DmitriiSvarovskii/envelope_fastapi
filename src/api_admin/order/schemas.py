from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
    tg_user_id: int
    delivery_city: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_comment: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_date: datetime
    # customer: "Customer"



class OrderDetailBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
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
