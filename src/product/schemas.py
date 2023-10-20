from datetime import datetime
from pydantic import BaseModel
from typing import List


class ProductList(BaseModel):
    id: int
    # category_id: int
    category_id: str
    name_rus: str
    price: float
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool
    # shop_id: int
    # image: str
    # name_en: str = None
    # description_rus: str = None
    # description_en: str = None


class ProductOne(ProductList):
    # shop_id: int
    category_id: int
    name_rus: str
    # name_en: str = None
    description_rus: str = None
    # description_en: str = None
    price: float
    image: str = None
    wt: int = None
    unit: int = None
    kilocalories: int = None
    proteins: int = None
    fats: int = None
    carbohydrates: int = None
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool


class ProductCreate(ProductOne):
    pass
    # category_id: int
    # name_rus: str
    # # name_en: str = None
    # description_rus: str
    # # description_en: str = None
    # price: float
    # wt: int
    # # image: str = None
    # unit: int
    # availability: bool
    # popular: bool
    # delivery: bool
    # takeaway: bool
    # dinein: bool


class UnitCreate(BaseModel):
    name: str


class ProductUpdate(ProductCreate):
    pass


class ProductModel(ProductOne):
    id: int
    # created_at: datetime

    class Config:
        from_attributes = True


class UnitBase(BaseModel):
    id: int
    name: str


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    pass


class UnitModel(UnitBase):
    id: int

    class Config:
        from_attributes = True
