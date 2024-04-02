from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    availability: bool


class CategoryBaseStore(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CategoryList(CategoryBase):
    id: int
    name: str
    availability: bool


class CategoryCreate(CategoryBase):
    pass


class CategoryDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class CategoryUpdate(BaseModel):
    name: str


class CategoryModel(CategoryBase):
    id: int


class SubcategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    availability: bool
    parent_category_id: int


class SubcategoryList(SubcategoryBase):
    id: int
    name: str
    availability: bool
    parent_category_id: int


class SubcategoryCreate(SubcategoryBase):
    pass


class SubcategoryDeleted(BaseModel):
    deleted_at: bool
    deleted_flag: bool


class SubcategoryUpdate(BaseModel):
    name: str
    availability: bool
    parent_category_id: int


class SubcategoryModel(SubcategoryBase):
    id: int
