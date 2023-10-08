from datetime import datetime
from pydantic import BaseModel
from typing import List


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    # hashed_password: str
    name: str
    availability: bool = True
    token_bot: str = None
    tg_group_id: int = None
    role_id: int = 2
    employee_id: int = None


class UserCreate(BaseModel):
    name: str
    username: str
    hashed_password: str

    class Config:
        from_attribute = True


class UserModel(UserBase):
    id: int

    class Config:
        from_attribute = True
