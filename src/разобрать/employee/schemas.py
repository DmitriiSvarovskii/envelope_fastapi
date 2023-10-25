from pydantic import BaseModel


class EmployeeBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: int
    tg_user_id: int


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    phone: int
    tg_user_id: int


class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str
    phone: int
    tg_user_id: int


class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
