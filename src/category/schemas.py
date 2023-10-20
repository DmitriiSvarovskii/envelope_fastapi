from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class CategoryBase1(BaseModel):
    name_rus: str
    availability: bool

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: int
    name_rus: str
    availability: bool

    class Config:
        from_attributes = True


# class CategoryBase(CategoryTest):

#     items: List[CategoryTest] = []

#     class Config:
#         from_attributes = True


# class CategoryBase(CategoryTest):

    # name_en: str = None
    # shop_id: int


class CategoryCreate(BaseModel):
    name_rus: str
    availability: bool = True

    class Config:
        from_attributes = True


class CategoryUpdate(CategoryBase):
    pass


class CategoryModel(CategoryBase):
    id: int

    class Config:
        from_attributes = True
