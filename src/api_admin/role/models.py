from sqlalchemy import Column, func, DateTime, Integer, String, Boolean
from src.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now(), nullable=True)
    deleted_flag = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
