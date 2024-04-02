from sqlalchemy.orm import Mapped, mapped_column
from src.database import (
    Base, intpk, str_64, is_active,
    created_at, deleted_flag, deleted_at,
    updated_at
)


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    first_name: Mapped[str_64]
    last_name: Mapped[str_64]
    number_phone: Mapped[int] = mapped_column(unique=True, nullable=True)
    tg_user_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    is_active: Mapped[is_active]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
