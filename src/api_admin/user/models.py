from datetime import datetime
from sqlalchemy import create_engine, Column, func, DateTime, Integer, BIGINT, TIMESTAMP, String, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now(), nullable=True)
    deleted_flag = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    user_data = relationship('UserData', back_populates='user')


class UserData(Base):
    __tablename__ = "user_datas"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String(length=1024), nullable=False)
    name = Column(String, nullable=True)
    number_phone = Column(BIGINT, unique=True, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)

    user = relationship('User', back_populates='user_data')
    employees = relationship('Employee', foreign_keys=[employee_id])
    # users = relationship('User', foreign_keys=[user_id])
    roles = relationship('Role', foreign_keys=[role_id])


class CategoryTest(Base):
    __tablename__ = "categories_test"

    id = Column(Integer, primary_key=True, index=True)
    availability = Column(Boolean, default=True)

    def __init__(self, schema_name, availability):
        self.id = Column(Integer, primary_key=True)
        self.availability = Column(Boolean, default=True)

        # Указываем схему
        __table_args__ = {"schema": schema_name}
