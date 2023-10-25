from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleDeleted(RoleBase):
    pass


class RoleModel(RoleBase):
    id: int

    class Config:
        from_attributes = True
