from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    hashed_password: str

    class Config:
        from_attribute = True


class TokenCreate(BaseModel):
    access_token: str

    class Config:
        from_attribute = True
