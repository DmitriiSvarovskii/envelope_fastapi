from pydantic import BaseModel, ConfigDict


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    hashed_password: str


class TokenCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
