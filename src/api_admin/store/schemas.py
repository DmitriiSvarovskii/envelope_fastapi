from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class StoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    # availability: bool
    # position: int


class StoreAll(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    region: Optional[str | None]
    city: Optional[str | None]
    street: Optional[str | None]
    number_phone: Optional[int | None]
    mobile_phone: Optional[int | None]
    coordinates_1: Optional[int | None]
    coordinates_2: Optional[int | None]
    link_bot: Optional[str | None]
    delivery: Optional[bool | None]
    takeaway: Optional[bool | None]
    dinein: Optional[bool | None]
    time_zone: Optional[str | None]
    open_hours: Optional[datetime | None]
    close_hours: Optional[datetime | None]
    is_active: Optional[bool | None]


class StoreList(StoreBase):
    id: int
    name: str


class StoreTgGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_id_group: int
    # availability: bool
    # position: int


class StoreCreate(StoreBase):
    link_bot: Optional[str] = None


class BotTokenCreate(BaseModel):
    token_bot: Optional[str] = None


class StoreDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class StoreUpdate(BaseModel):
    name: str
    # availability: bool


class StoreModel(StoreBase):
    id: int
