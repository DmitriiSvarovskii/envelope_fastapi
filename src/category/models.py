import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from PIL import Image as PILImage


from src.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(primary_key=True, index=True)
    name_rus = Column(String, default=None)
    # name_rus: Mapped[str]
    # availability: Mapped[bool] = mapped_column(default=True)
    # name_en = Column(String, default=None)
    # shop_id = Column(Integer, ForeignKey("users.id"))
