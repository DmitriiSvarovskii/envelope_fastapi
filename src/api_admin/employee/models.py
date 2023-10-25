from sqlalchemy import Column, func, DateTime, Integer, BIGINT, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now(), nullable=True)
    deleted_flag = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)


class EmployeeData(Base):
    __tablename__ = "employee_datas"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(BIGINT, nullable=True)
    tg_user_id = Column(Integer, nullable=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    employees = relationship('Employee', foreign_keys=[employee_id])
