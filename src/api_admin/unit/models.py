from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Integer, String
from sqlalchemy.orm import relationship


from src.database import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    products = relationship("Product", back_populates="unit")
