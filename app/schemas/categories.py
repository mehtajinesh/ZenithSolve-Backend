from pydantic import BaseModel, Field
from typing import List
from app.schemas.problems import Problem


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int = Field(..., ge=1)
    problems: List[Problem] = []

    class Config:
        from_attributes = True
