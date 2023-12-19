from sqlalchemy.orm import Session
from sqlalchemy.event import listens_for
import os
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped, mapped_column
from src.database import *

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey, func, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from PIL import Image as PILImage
from src.database import Base, get_async_session
import enum

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import *


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    name: Mapped[str_64] = mapped_column(unique=True)

    products: Mapped[List['Product']
                     ] = relationship(back_populates="unit")


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"))
    subcategory_id: Mapped[int | None] = mapped_column(
        ForeignKey("subcategories.id", ondelete="CASCADE"))
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    name: Mapped[str_64]
    description: Mapped[str_256 | None]
    image: Mapped[str | None]
    price: Mapped[float]
    wt: Mapped[int | None]
    unit_id: Mapped[int] = mapped_column(
        ForeignKey("public.units.id", ondelete="CASCADE"))
    kilocalories: Mapped[int | None]
    proteins: Mapped[int | None]
    fats: Mapped[int | None]
    carbohydrates: Mapped[int | None]
    availability: Mapped[bool]
    popular: Mapped[bool]
    delivery: Mapped[bool]
    takeaway: Mapped[bool]
    dinein: Mapped[bool]
    # position: Mapped[int] = mapped_column(Integer, nullable=True)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))

    category: Mapped['Category'] = relationship(back_populates="products")
    subcategory: Mapped['Subcategory'] = relationship(
        back_populates="products")
    store: Mapped['Store'] = relationship(back_populates="products")
    unit: Mapped['Unit'] = relationship(back_populates="products")
    carts: Mapped['Cart'] = relationship(
        back_populates="product")
    order_details: Mapped['OrderDetail'] = relationship(back_populates="product")

    # user_product: Mapped[List['User']] = relationship(
    #     back_populates="product")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


# @event.listens_for(Category.availability, 'set')
# async def on_category_availability_set(target, value, oldvalue, initiator):
#     # Обновление availability продуктов внутри сессии
#     async with get_async_session() as session:
#         products = session.query(Product).filter_by(category=target).all()
#         for product in products:
#             if product.availability != value:
#                 product.availability = value
#         await session.commit()

    # image = Column(
    #     String, nullable=False, default="/var/www/envelope_fastapi/media/caprese-salad.webp")
    # shop_id = Column(Integer, ForeignKey("users.id"))
    # name_en = Column(String, default=None)
    # description_en = Column(String, default=None)

    # def save_image(self, image_path):
    #     """
    #     Обработка и сохранение изображения в формате webp.
    #     """
    #     media_directory = f"src/media/{self.shop_id}/"

    #     os.makedirs(media_directory, exist_ok=True)

    #     image = PILImage.open(image_path)

    #     max_size = (800, 800)
    #     image.thumbnail(max_size, PILImage.LANCZOS)

    #     webp_path = os.path.splitext(image_path)[0] + ".webp"
    #     webp_full_path = os.path.join(media_directory, webp_path)
    #     image.save(webp_full_path, "WEBP")

    #     webp_relative_path = os.path.join('', webp_path)
    #     self.image = webp_relative_path
