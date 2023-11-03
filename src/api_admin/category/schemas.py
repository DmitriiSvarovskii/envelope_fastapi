from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    availability: bool

    # position: int


class CategoryList(CategoryBase):
    id: int
    name: str
    availability: bool
    # position: int


class CategoryCreate(CategoryBase):
    pass
    # updated_by: int
    # deleted_by: int


# class CategoryBase(CategoryTest):

#     items: List[CategoryTest] = []

#     class Config:
#         from_attributes = True


class CategoryDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


# class CategoryDeletedFlag(BaseModel):
#     deleted_flag: bool


class CategoryUpdate(BaseModel):
    name: str
    availability: bool
    # updated_by: int


class CategoryModel(CategoryBase):
    id: int

    class Config:
        from_attributes = True
