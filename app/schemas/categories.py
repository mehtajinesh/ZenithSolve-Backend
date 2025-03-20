from pydantic import BaseModel, Field
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int = Field(..., ge=1)
    
    class Config:
        from_attributes = True
