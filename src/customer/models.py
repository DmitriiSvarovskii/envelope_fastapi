import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from PIL import Image as PILImage

from src.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("users.id"))
    tg_user_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    is_premium = Column(Boolean)
    query_id = Column(String)
    hash = Column(String)
    # last_order = Column(TIMESTAMP, default=datetime.utcnow)
