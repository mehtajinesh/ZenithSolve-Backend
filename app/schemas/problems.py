from pydantic import BaseModel
from typing import List
from schemas.real_world_examples import RealWorldExample
from schemas.solutions import Solution
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
        orm_mode = True
