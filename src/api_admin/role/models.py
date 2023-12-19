from typing import List
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped
from typing import List, TYPE_CHECKING
from src.database import *

if TYPE_CHECKING:
    from ..category import Category
    from ..subcategory import Subcategory
    from ..user import User
    from ..role import Role
    from ..auth import Token
    from ..employee import Employee


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {'schema': 'public'}

    id: Mapped[intpk]
    name: Mapped[str_64]

    users: Mapped[List['User']] = relationship(back_populates="role")
