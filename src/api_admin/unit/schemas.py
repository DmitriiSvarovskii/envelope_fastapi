from datetime import datetime
from pydantic import BaseModel
from typing import List


class UnitCreate(BaseModel):
    name: str


class UnitBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UnitCreate(BaseModel):
    name: str


class UnitUpdate(UnitCreate):
    pass


class UnitModel(UnitBase):
    class Config:
        from_attributes = True
