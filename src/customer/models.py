import os

from datetime import datetime
from sqlalchemy import create_engine, Column, BIGINT, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from PIL import Image as PILImage

from src.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("users.id"))
    tg_user_id = Column(BIGINT, unique=True)
    first_name = Column(String, default=None)
    last_name = Column(String, default=None)
    username = Column(String, default=None)
    is_premium = Column(Boolean, default=False)
    query_id = Column(String)
    hash = Column(String)
    # last_order = Column(TIMESTAMP, default=datetime.utcnow)
