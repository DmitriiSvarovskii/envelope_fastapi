from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("users.id"))
    tg_user_id = Column(Integer, ForeignKey("customers.tg_user_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
