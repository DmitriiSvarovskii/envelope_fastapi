from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


class UserList(UserBase):
    model_config = ConfigDict(from_attributes=True)
    number_phone: Optional[int] = None
    employee_id: Optional[int] = None
    role_id: int
    id: int


class UserTgId(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_tg_id: Optional[int] = None

    # class Config:
    #     from_attributes = True


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    hashed_password: str


class UserUpdateData(UserBase):
    number_phone: int
    employee_id: Optional[int] = None
    role: str

    class Config:
        from_attribute = True


class UserUpdatePassword(BaseModel):
    old_password: str
    hashed_password: str

    class Config:
        from_attribute = True


class UserModel(UserBase):
    pass


class RolesBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class RolesList(RolesBase):
    id: int


class RolesCreate(RolesBase):
    pass


class RolesUpdate(RolesBase):
    pass


class RolesDelete(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
