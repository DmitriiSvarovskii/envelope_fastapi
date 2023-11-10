from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List


class CartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int


class CartCreate(CartBase):
    model_config = ConfigDict(from_attributes=True)

    tg_user_id: int
    # store_id: int


class CartItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    name: str
    quantity: int
    unit_price: float
