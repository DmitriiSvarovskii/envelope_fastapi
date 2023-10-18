import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from PIL import Image as PILImage


from src.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    # shop_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name_rus = Column(String, nullable=True)
    # name_en = Column(String, default=None)
    description_rus = Column(String, nullable=True)
    # description_en = Column(String, default=None)
    price = Column(Float, nullable=True)
    image = Column(
        String, nullable=False, default="/var/www/envelope_fastapi/media/caprese-salad.webp")
    wt = Column(Integer, default=None)
    unit = Column(Integer, ForeignKey("units.id"))
    kilocalories = Column(Integer, default=None)
    proteins = Column(Integer, default=None)
    fats = Column(Integer, default=None)
    carbohydrates = Column(Integer, default=None)
    availability = Column(Boolean, nullable=True, default=True)
    popular = Column(Boolean, default=False)
    type_delivery = Column(Boolean, default=True)
    type_takeaway = Column(Boolean, default=True)
    type_dinein = Column(Boolean, default=True)

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


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
