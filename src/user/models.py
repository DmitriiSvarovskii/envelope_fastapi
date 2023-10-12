from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP, String, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


from src.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    name = Column(String, default=None)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    token_bot = Column(String, default=None)
    tg_group_id = Column(Integer, default=None)
    role_id = Column(Integer, ForeignKey("roles.id"), default=2)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    tokens = relationship('Token', back_populates='user')
