from datetime import datetime
from sqlalchemy import Column, Integer, TIMESTAMP, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("users.id"))
    tg_user_id = Column(Integer, ForeignKey("customers.tg_user_id"))
    order_date = Column(TIMESTAMP, default=datetime.utcnow)
    delivery_city = Column(String)
    delivery_address = Column(String)
    customer_name = Column(String)
    customer_phone = Column(String)
    customer_comment = Column(String)

    customer = relationship(
        "Customer", primaryjoin="and_(Order.tg_user_id==Customer.tg_user_id, Order.shop_id==Customer.shop_id)")


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    order_date = Column(TIMESTAMP, default=datetime.utcnow)
    shop_id = Column(Integer, ForeignKey("users.id"))
