from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tg_user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_premium: Optional[bool] = None


class ReportCustomer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_premium: bool
    total_sales: Optional[float] = None
    last_order_date: Optional[str] = None


class CustomerCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    tg_user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_premium: Optional[bool] = None
    # query_id: str
    # hash: str


class CustomerUpdate(CustomerCreate):
    pass
