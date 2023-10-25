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


class UserBase(BaseModel):
    username: str
    name: str
    availability: Optional[bool] = True
    # token_bot: Optional[str] = None
    # tg_group_id: Optional[int] = None
    # role_id: Optional[int] = 2
    # employee_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    # name: str
    username: str
    hashed_password: str

    class Config:
        from_attribute = True


class UserModel(UserBase):
    id: int

    class Config:
        from_attribute = True
