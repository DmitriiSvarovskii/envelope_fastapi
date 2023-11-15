from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import *


class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(ForeignKey("customers.tg_user_id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]

    def __init__(self, schema):
            super().__init__()
            self.__table_args__ = {'schema': schema}


    # def __init__(self, schema, product_id, quantity, tg_user_id):
    #         super().__init__()
    #         self.__table_args__ = {'schema': schema}
    #         self.product_id = product_id
    #         self.quantity = quantity
    #         self.tg_user_id = tg_user_id
 
            