from pydantic import BaseModel
from typing import List
from app.schemas.real_world_examples import RealWorldExample
from app.schemas.solutions import Solution
class ProblemBase(BaseModel):
    title: str
    statement: str
    constraints: str
    examples: str
    category_id: int

class ProblemCreate(ProblemBase):
    pass

class Problem(ProblemBase):
    id: int
    real_world_examples: List[RealWorldExample] = []
    solutions: List[Solution] = []

    class Config:
        from_attributes = True
