from typing import List, TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped
from src.database import Base, intpk, str_64

if TYPE_CHECKING:
    from ..user import User


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    name: Mapped[str_64]

    users: Mapped[List['User']] = relationship(back_populates="role")
