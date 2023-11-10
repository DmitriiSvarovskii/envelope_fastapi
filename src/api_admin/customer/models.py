from datetime import datetime
from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import *


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    is_premium: Mapped[bool] = mapped_column(server_default=text("false"))
    query_id: Mapped[str]
    hash: Mapped[str]
    created_at: Mapped[created_at]

    def __init__(self, schema):
            super().__init__()
            self.__table_args__ = {'schema': schema}