from datetime import datetime
from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

from src.database import *


from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


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
    is_premium: Mapped[bool] = mapped_column(server_default=text("false"))
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}

    __table_args__ = (
        UniqueConstraint('store_id', 'tg_user_id', name='uq_store_tg_user'),
    )

# class Customer(Base):
#     __tablename__ = "customers"
#     __table_args__ = {'schema': None}

#     id: Mapped[intpk]
#     store_id: Mapped[int | None] = mapped_column(
#         ForeignKey("stores.id", ondelete="CASCADE"))
#     tg_user_id: Mapped[int] = mapped_column(BIGINT)
#     first_name: Mapped[str | None]
#     last_name: Mapped[str | None]
#     username: Mapped[str | None]
#     is_premium: Mapped[bool] = mapped_column(server_default=text("false"))
#     # query_id: Mapped[str]
#     # hash: Mapped[str]
#     created_at: Mapped[created_at]

#     def __init__(self, schema):
#         super().__init__()
#         self.__table_args__ = {'schema': schema}

#     __table_args__ = (
#         UniqueConstraint('tg_user_id', name='uq_tg_user_id'),
#     )
