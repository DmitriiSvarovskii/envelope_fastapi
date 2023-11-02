from pydantic import BaseModel, ConfigDict


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str | None
    number_phone: int | None
    role_id: int


class TokenCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
