# from sqlalchemy.orm import Session
# from sqlalchemy.event import listens_for
# import os
# from sqlalchemy import event
# from sqlalchemy.ext.asyncio import AsyncSession

# from datetime import datetime
# from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from PIL import Image as PILImage


# from src.database import Base, get_async_session
# from src.category.models import Category


# class Product(Base):
#     __tablename__ = 'products'

#     id = Column(Integer, primary_key=True, index=True)
#     category_id = Column(Integer, ForeignKey("categories.id"))
#     subcategory_id = Column(Integer, ForeignKey(
#         "subcategories.id"), default=None)
#     name = Column(String, nullable=True)
#     description = Column(String, nullable=True)
#     price = Column(Float, nullable=True)
#     wt = Column(Integer, default=None)
#     unit_id = Column(Integer, ForeignKey("units.id"))
#     kilocalories = Column(Integer, default=None)
#     proteins = Column(Integer, default=None)
#     fats = Column(Integer, default=None)
#     carbohydrates = Column(Integer, default=None)
#     availability = Column(Boolean)
#     popular = Column(Boolean)
#     delivery = Column(Boolean)
#     takeaway = Column(Boolean)
#     dinein = Column(Boolean)

#     category = relationship("Category", back_populates="products")
#     subcategory = relationship("Subcategory", back_populates="products")
#     unit = relationship("Unit", back_populates="products")


# # @event.listens_for(Category.availability, 'set')
# # async def on_category_availability_set(target, value, oldvalue, initiator):
# #     # Обновление availability продуктов внутри сессии
# #     async with get_async_session() as session:
# #         products = session.query(Product).filter_by(category=target).all()
# #         for product in products:
# #             if product.availability != value:
# #                 product.availability = value
# #         await session.commit()

#     # image = Column(
#     #     String, nullable=False, default="/var/www/envelope_fastapi/media/caprese-salad.webp")
#     # shop_id = Column(Integer, ForeignKey("users.id"))
#     # name_en = Column(String, default=None)
#     # description_en = Column(String, default=None)

#     # def save_image(self, image_path):
#     #     """
#     #     Обработка и сохранение изображения в формате webp.
#     #     """
#     #     media_directory = f"src/media/{self.shop_id}/"

#     #     os.makedirs(media_directory, exist_ok=True)

#     #     image = PILImage.open(image_path)

#     #     max_size = (800, 800)
#     #     image.thumbnail(max_size, PILImage.LANCZOS)

#     #     webp_path = os.path.splitext(image_path)[0] + ".webp"
#     #     webp_full_path = os.path.join(media_directory, webp_path)
#     #     image.save(webp_full_path, "WEBP")

#     #     webp_relative_path = os.path.join('', webp_path)
#     #     self.image = webp_relative_path


# class Unit(Base):
#     __tablename__ = "units"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     products = relationship("Product", back_populates="unit")
