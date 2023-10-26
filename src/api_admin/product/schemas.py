from datetime import datetime
from pydantic import BaseModel
from typing import List


class ProductList(BaseModel):
    id: int
    category_id: int
    category_name: str
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
    description_rus: str
    # description_en: str = None
    price: float
    # image: str
    wt: int
    # unit: int = None
    kilocalories: int
    proteins: int
    fats: int
    carbohydrates: int
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool


class ProductCreate(BaseModel):
    category_id: int
    name_rus: str
    description_rus: str
    price: float
    wt: int
    kilocalories: int
    proteins: int
    fats: int
    carbohydrates: int
    unit_id: int
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool
    created_by: int


class ProductUpdate(BaseModel):
    category_id: int
    name_rus: str
    description_rus: str
    price: float
    wt: int
    kilocalories: int
    proteins: int
    fats: int
    carbohydrates: int
    unit_id: int
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool
    updated_by: int


class ProductModel(ProductOne):
    id: int

    class Config:
        from_attributes = True


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
