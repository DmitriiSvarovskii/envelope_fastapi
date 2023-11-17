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


class CartItemsOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
    unit_price: int


class CreateOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_user_id: int
    store_id: int
    # cart_items: List[CartItemsOrder]
    delivery_city: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_comment: Optional[str] = None
