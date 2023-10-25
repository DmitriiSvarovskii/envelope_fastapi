from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


class UserList(UserBase):
    user_id: int
    number_phone: Optional[int] = None
    employee_id: Optional[int] = None
    role_id: Optional[int] = 1
    # updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    hashed_password: str

    class Config:
        from_attribute = True


class UserUpdateData(UserBase):
    number_phone: int
    employee_id: Optional[int] = None
    role_id: Optional[int] = 1

    class Config:
        from_attribute = True


class UserUpdatePassword(BaseModel):
    old_password: str
    hashed_password: str

    class Config:
        from_attribute = True


class UserModel(UserBase):
    pass
