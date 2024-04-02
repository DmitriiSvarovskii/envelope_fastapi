from pydantic import BaseModel, ConfigDict


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
