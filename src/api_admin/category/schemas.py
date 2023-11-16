from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    availability: bool


class CategoryBaseStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    # position: int


class CategoryList(CategoryBase):
    id: int
    name: str
    availability: bool
    # position: int


class CategoryCreate(CategoryBase):
    pass


class CategoryDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class CategoryUpdate(BaseModel):
    name: str
    # availability: bool


class CategoryModel(CategoryBase):
    id: int


class SubcategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    availability: bool
    parent_category_id: int

    # position: int


class SubcategoryList(SubcategoryBase):
    id: int
    name: str
    availability: bool
    parent_category_id: int
    # position: int


class SubcategoryCreate(SubcategoryBase):
    pass


class SubcategoryDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class SubcategoryUpdate(BaseModel):
    name: str
    availability: bool
    parent_category_id: int


class SubcategoryModel(SubcategoryBase):
    id: int
