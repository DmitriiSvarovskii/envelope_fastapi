from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, BIGINT

from src.database import Base, intpk


class PaymentYookassa(Base):
    __tablename__ = 'payments_yookassa'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    api_id: Mapped[int] = mapped_column(BIGINT)
    api_key: Mapped[str]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
