from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class CartBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    # quantity: int


class CartCreate(CartBase):
    model_config = ConfigDict(from_attributes=True)

    tg_user_id: int
    store_id: int


class CartGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_user_id: int
    store_id: int


class CartItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image: Optional[str] = None

    quantity: int
    unit_price: float


class CartResponse(BaseModel):
    cart_items: List[CartItem]
    total_price: float


class CartItemTotal(CartItem):
    model_config = ConfigDict(from_attributes=True)

    # tg_user_id: int
    total_price: int
