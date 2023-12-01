from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class UnitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: str
    category_id: int
    # subcategory_id: Optional[int] = None
    # store_id: int
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    price: float
    wt: Optional[int] = None
    unit_id: int
    kilocalories: Optional[int] = None
    proteins: Optional[int] = None
    fats: Optional[int] = None
    carbohydrates: Optional[int] = None
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool


class ProductListStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # category_name: str
    category_id: int
    # subcategory_id: Optional[int] = None
    # store_id: int
    name: str
    # description: Optional[str] = None
    image: Optional[str] = None
    price: float
    # wt: Optional[int] = None
    # unit_id: int
    # kilocalories: Optional[int] = None
    # proteins: Optional[int] = None
    # fats: Optional[int] = None
    # carbohydrates: Optional[int] = None
    # availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool
    # position


class ProductOne(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # category_id: int
    name: str
    description: str
    price: float
    image: Optional[str] = None
    wt: int
    kilocalories: int
    proteins: int
    fats: int
    carbohydrates: int
    unit: Optional[UnitBase]
    # availability: bool
    # popular: bool
    # delivery: bool
    # takeaway: bool
    # dinein: bool


class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: str | None
    image: Optional[str] = None
    price: float
    wt: int
    kilocalories: int | None
    proteins: int | None
    fats: int | None
    carbohydrates: int | None
    unit_id: int
    availability: bool
    popular: bool
    delivery: bool
    takeaway: bool
    dinein: bool
    # created_by: int
    # updated_by: int


class ProductUpdate(BaseModel):
    category_id: int
    name: str
    description: str | None
    image: Optional[str] = None
    price: float
    wt: int
    kilocalories: int | None
    proteins: int | None
    fats: int | None
    carbohydrates: int | None
    unit_id: int


class ProductModel(ProductOne):
    id: int

    class Config:
        from_attributes = True


class UnitCreate(BaseModel):
    name: str


class UnitUpdate(UnitCreate):
    pass


class UnitList(UnitBase):
    model_config = ConfigDict(from_attributes=True)
    pass
