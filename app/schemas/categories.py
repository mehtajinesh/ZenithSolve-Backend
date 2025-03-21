from pydantic import BaseModel, Field


class CategoryIn(BaseModel):
    name: str = Field(..., max_length=100)
    
    class Config:
        from_attributes = True

class CategoryOut(CategoryIn):
    id: int
    
    class Config:
        from_attributes = True
