import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from PIL import Image as PILImage
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import *

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..category import Category
    from ..subcategory import Subcategory
    from ..user import User
    from ..product import Product
    from ..store import Store


class Mail(Base):
    __tablename__ = 'mails'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    # store_id: Mapped[int] = mapped_column(
    #     ForeignKey("stores.id", ondelete="CASCADE"))
    title: Mapped[str_256]
    mail_text: Mapped[str_4048]
    image: Mapped[str | None]
    created_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))

    # mail_store: Mapped[List['Store']
    #                    ] = relationship(back_populates="mail")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
