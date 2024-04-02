import datetime
from sqlalchemy import BIGINT, ForeignKey, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.database import (
    Base, intpk, created_at
)

if TYPE_CHECKING:
    from ..models import Store


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int | None] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(BIGINT)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    resourse: Mapped[str | None]
    birth_day: Mapped[datetime.datetime | None]
    is_premium: Mapped[bool] = mapped_column(server_default=text("false"))
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    store: Mapped['Store'] = relationship(back_populates="customers")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}

    __table_args__ = (
        UniqueConstraint('store_id', 'tg_user_id', name='uq_store_tg_user'),
    )
