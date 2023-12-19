from typing import List, TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.database import *


if TYPE_CHECKING:
    from ..category import Category
    from ..subcategory import Subcategory
    from ..user import User
    from ..product import Product
    from ..store import Store


class Mail(Base):
    __tablename__ = 'mails'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"))
    title: Mapped[str_256]
    mail_text: Mapped[str_4048]
    image_id: Mapped[int | None] = mapped_column(
        ForeignKey("mail_images.id", ondelete="CASCADE"))
    movie: Mapped[str | None]
    created_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    store: Mapped['Store'] = relationship(back_populates="mails")
    image: Mapped['MailImage'] = relationship(back_populates="mail")

    store: Mapped[List['Store']] = relationship(back_populates="mails")
    # mail_images: Mapped[List['MailImage']] = relationship(
    #     back_populates="image_mail")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}


class MailImage(Base):
    __tablename__ = 'mail_images'
    __table_args__ = {'schema': None}

    id: Mapped[intpk]
    image: Mapped[str | None]
    created_by: Mapped[int] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    deleted_flag: Mapped[deleted_flag]
    deleted_at: Mapped[deleted_at]
    deleted_by: Mapped[int | None] = mapped_column(
        ForeignKey("public.users.id", ondelete="CASCADE"))

    mail: Mapped['Mail'] = relationship(back_populates="image")
    # image_mail: Mapped['Mail'] = relationship(back_populates="mail_images")
    # mail_store: Mapped['Store'] = relationship(back_populates="mail")

    def __init__(self, schema):
        super().__init__()
        self.__table_args__ = {'schema': schema}
