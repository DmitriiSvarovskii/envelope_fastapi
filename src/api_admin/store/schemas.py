from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class StoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    # availability: bool
    # position: int


class StoreList(StoreBase):
    id: int
    name: str
    # availability: bool
    # position: int


class StoreCreate(StoreBase):
    token_bot: str


class StoreDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class StoreUpdate(BaseModel):
    name: str
    # availability: bool


class StoreModel(StoreBase):
    id: int
