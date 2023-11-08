# import os

# from datetime import datetime
# from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
# from sqlalchemy.orm import relationship, Mapped, mapped_column
# from PIL import Image as PILImage
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import expression

# from src.database import Base


# class Category(Base):
#     __tablename__ = 'categories'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, default=None)
#     availability = Column(Boolean, default=True)
#     position = Column(Integer, nullable=True)
#     created_at = Column(DateTime, default=func.now(), nullable=True)
#     created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
#     updated_at = Column(DateTime, default=func.now(),
#                         onupdate=func.now(), nullable=True)
#     updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
#     deleted_flag = Column(Boolean, default=False)
#     deleted_at = Column(DateTime, nullable=True)

#     created_by_user = relationship('User', foreign_keys=[created_by])
#     updated_by_user = relationship('User', foreign_keys=[updated_by])

#     subcategories = relationship(
#         "Subcategory", back_populates="parent_category")
#     products = relationship("Product", back_populates="category")

#     def __init__(self, *args, **kwargs):
#         if 'position' not in kwargs:
#             kwargs['position'] = self.id
#         super().__init__(*args, **kwargs)


# class Subcategory(Base):
#     __tablename__ = 'subcategories'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     parent_category_id = Column(Integer, ForeignKey('categories.id'))

#     parent_category = relationship("Category", back_populates="subcategories")
#     products = relationship("Product", back_populates="subcategory")

#     # name: Mapped[str]
#     # name_en = Column(String, default=None)
#     # shop_id = Column(Integer, ForeignKey("users.id"))
