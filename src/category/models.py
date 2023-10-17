import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from PIL import Image as PILImage


from src.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name_rus = Column(String)
    # name_en = Column(String, default=None)
    # availability = Column(Boolean, default=True)
    # shop_id = Column(Integer, ForeignKey("users.id"))
