from datetime import datetime
from pydantic import BaseModel
from typing import List


class CartBase(BaseModel):
    product_id: int
    quantity: int


class CartCreate(CartBase):
    tg_user_id: int
    shop_id: int

    class Config:
        orm_mode = True


class CartItem(BaseModel):
    id: int
    name_rus: str
    description_rus: str
    quantity: int
    unit_price: float
