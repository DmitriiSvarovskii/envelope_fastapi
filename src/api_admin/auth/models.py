from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..user import User


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[intpk]
    access_token: Mapped[str_64] = mapped_column(unique=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))

    user: Mapped['User'] = relationship(back_populates="token")  # One-to-One

