from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing import List

from .product import ProductBase, UnitBase
from .category import CategoryBase, SubcategoryBase


# class Product(ProductBase):
#     __tablename__ = 'products'
#     __table_args__ = {'schema': None}

#     unit: Mapped['Unit'] = relationship(
#         back_populates="product_unit")
#     category: Mapped['Category'] = relationship(
#         back_populates="product_category")
#     subcategory: Mapped['Subcategory'] = relationship(
#         back_populates="product_subcategory")

#     def __init__(self, schema):
#         super().__init__()
#         self.__table_args__ = {'schema': schema}


# class Unit(UnitBase):
#     __tablename__ = "units"
#     __table_args__ = {'schema': None}

#     product_unit: Mapped[List['Product']
#                          ] = relationship(back_populates="unit")

#     def __init__(self, schema):
#         super().__init__()
#         self.__table_args__ = {'schema': schema}


# class Category(CategoryBase):
#     __tablename__ = 'categories'
#     __table_args__ = {'schema': None}

#     product_category: Mapped[List['Product']
#                              ] = relationship(back_populates="category")
#     category_subcategory: Mapped[List['Subcategory']
#                                  ] = relationship(back_populates="subcategory_category")

#     def __init__(self, schema):
#         super().__init__()
#         self.__table_args__ = {'schema': schema}


# class Subcategory(SubcategoryBase):
#     __tablename__ = 'subcategories'
#     __table_args__ = {'schema': None}

#     product_subcategory: Mapped[List['Product']
#                                 ] = relationship(back_populates="subcategory")
#     subcategory_category: Mapped['Category'] = relationship(
#         back_populates="category_subcategory")
#     # product_subcategory: Mapped[List['Product']
#     #                             ] = relationship(back_populates="subcategory")

#     def __init__(self, schema):
#         super().__init__()
#         self.__table_args__ = {'schema': schema}
