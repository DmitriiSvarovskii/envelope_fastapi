from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tg_user_id: int
    # first_name: str
    # last_name: str
    # username: str
    # is_premium: bool
    # query_id: str
    # hash: str


class CustomerCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tg_user_id: int
    # first_name: str
    # last_name: str
    # username: str
    # is_premium: bool
    # query_id: str
    # hash: str


class CustomerUpdate(CustomerCreate):
    pass
