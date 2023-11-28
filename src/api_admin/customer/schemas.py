from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tg_user_id: int
    first_name: str
    last_name: str
    username: str
    is_premium: bool
    # query_id: str
    # hash: str


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
