from datetime import datetime
from sqlalchemy import create_engine, Column, BIGINT, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


from src.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(BIGINT)
    tg_user_id = Column(Integer)
