from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, BIGINT, TIMESTAMP, String, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(length=1024), nullable=False)
    name = Column(String, default=None)
    number_phone = Column(BIGINT, unique=True, default=None)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    tokens = relationship('Token', back_populates='user')


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class TokenBotTelegram(Base):
    __tablename__ = "tokens_bot_telegram"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    token_bot = Column(BIGINT, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class GroupTelegram(Base):
    __tablename__ = "groups_telegram"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    token_group_id = Column(BIGINT, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
