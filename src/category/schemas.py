from pydantic import BaseModel


class CategoryBase(BaseModel):
    name_rus: str = None
    name_en: str = None
    availability: bool = True
    shop_id: int


class CategoryCreate(CategoryBase):
    class Config:
        from_attributes = True


class CategoryUpdate(CategoryBase):
    pass


class CategoryModel(CategoryBase):
    id: int

    class Config:
        from_attributes = True
