# from datetime import datetime
# from pydantic import BaseModel, ConfigDict
# from typing import List, Optional


# # class CategoryBase1(BaseModel):
# #     name: str
# #     # availability: bool

# #     class Config:
# #         from_attributes = True


# class CategoryBase(BaseModel):
#     id: int
#     name: str
#     availability: bool
#     # position: int

#     class Config:
#         from_attributes = True


# # class CategoryBase(CategoryTest):

# #     items: List[CategoryTest] = []

# #     class Config:
# #         from_attributes = True


# class CategoryDeleted(BaseModel):
#     deleted_at: bool


# class CategoryCreate(BaseModel):
#     name: str
#     availability: bool
#     # created_at: datetime
#     created_by: int

#     class Config:
#         from_attributes = True


# class CategoryUpdate(BaseModel):
#     name: str
#     availability: bool
#     # updated_at: datetime
#     updated_by: int


# class CategoryModel(CategoryBase):
#     id: int

#     class Config:
#         from_attributes = True
