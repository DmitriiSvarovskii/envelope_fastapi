from pydantic import BaseModel


class CustomerBase(BaseModel):
    id: int
    tg_user_id: int
    first_name: str
    last_name: str
    username: str
    is_premium: bool
    query_id: str
    hash: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass
