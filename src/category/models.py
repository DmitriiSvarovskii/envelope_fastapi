import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from PIL import Image as PILImage


from src.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name_rus = Column(String, default=None)
    availability = Column(Boolean, default=True)

    subcategories = relationship(
        "Subcategory", back_populates="parent_category")
    products = relationship("Product", back_populates="category")


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_category_id = Column(Integer, ForeignKey('categories.id'))

    parent_category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")

    # name_rus: Mapped[str]
    # name_en = Column(String, default=None)
    # shop_id = Column(Integer, ForeignKey("users.id"))
